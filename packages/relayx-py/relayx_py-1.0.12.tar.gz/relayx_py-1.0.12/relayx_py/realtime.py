import time
import uuid
from datetime import datetime, timezone, timedelta
import asyncio
import tzlocal
import nats
from nats.aio.client import RawCredentials
import nats.js.api as nats_config
import json
import re
import inspect
import msgpack
import uuid
import numbers
import socket
from functools import wraps
import os
import re

class Realtime:
    __event_func = {}
    __topic_map = []

    CONNECTED = "CONNECTED"
    RECONNECT = "RECONNECT"
    MESSAGE_RESEND = "MESSAGE_RESEND"
    DISCONNECTED = "DISCONNECTED"

    # Private status messages
    __RECONNECTING = "RECONNECTING"
    __RECONNECTED = "RECONNECTED"
    __RECONN_FAIL = "RECONN_FAIL"

    __natsClient = None
    __jetstream = None
    __jsManager = None
    __consumerMap = {}

    __reconnected = False
    __disconnected = True
    __reconnecting = False
    __connected = False
    __reconnected_attempt = False
    __manual_disconnect = False

    __offline_message_buffer = []

    __latency = []
    __latency_push_task = None
    __is_sending_latency = False

    __disconnect_time = None

    def __init__(self, config=None):
        if config is not None:
            if type(config) is not dict:
                raise ValueError("Realtime($config). $config not object => {}")

            if "api_key" in config:
                self.api_key = config["api_key"]

                if type(self.api_key) is not str:
                    raise ValueError("api_key value must be a string")
                
                if self.api_key == "":
                    raise ValueError("api_key value must not be an empty string")
            else:
                raise ValueError("api_key value not found in config object")
            
            if "secret" in config:
                self.secret = config["secret"]

                if type(self.secret) is not str:
                    raise ValueError("secret value must be a string")
                
                if self.secret == "":
                    raise ValueError("secret value must not be an empty string")
            else:
                raise ValueError("secret value not found in config object")
        else:
            raise ValueError("Realtime($config). $config is None")

        self.__namespace = ""
        self.__topicHash = ""
        self.quit_event = asyncio.Event()
        

    def init(self, staging=False, opts=None):
        """
        Initializes library with configuration options.
        """

        self.staging = staging
        self.opts = opts

        if opts:
            if "debug" in opts:
                self.__debug = opts["debug"]
            else:
                self.__debug = False
        else:
            self.__debug = False

        proxy = os.getenv("PROXY", None)

        if proxy:
            self.__base_url = ["tls://api2.relay-x.io:8666"]
            self.__initDNSSpoof()
        else:
            self.__base_url = [
                "nats://0.0.0.0:4221",
                "nats://0.0.0.0:4222",
                "nats://0.0.0.0:4223"
            ] if staging else [
                "tls://api.relay-x.io:4221",
                "tls://api.relay-x.io:4222",
                "tls://api.relay-x.io:4223"
            ]
            

    async def __get_namespace(self):
        """
        Gets the __namespace of the user using a service
        """

        encoded = self.__encode_json({
            "api_key": self.api_key
        })

        response = None
        try:
            response = await self.__natsClient.request("accounts.user.get_namespace", encoded, timeout=5)
        except Exception as e:
            self.__log(f"Error getting namespace: {e}")
            response = None
        
        if response:
            resp_data = response.data.decode('utf-8')
            resp_data = json.loads(resp_data)
            
            if resp_data["status"] == "NAMESPACE_RETRIEVE_SUCCESS":
                self.__namespace = resp_data["data"]["namespace"]
                self.__topicHash = resp_data["data"]["hash"]
            else:
                raise ValueError("Namespace not found")
        else:
            raise ValueError("Namespace not found")
        
    async def __push_latency(self, data):
        """
        Gets the __namespace of the user using a service
        """
        self.__is_sending_latency = True

        encoded = self.__encode_json({
            "api_key": self.api_key,
            "payload": data
        })

        response = None
        try:
            response = await self.__natsClient.request("accounts.user.log_latency", encoded, timeout=5)
        except Exception as e:
            self.__log(f"Error getting namespace: {e}")
            response = None
        
        if response:
            resp_data = response.data.decode('utf-8')
            resp_data = json.loads(resp_data)

            self.__latency.clear()

            if self.__latency_push_task is not None:
                self.__latency_push_task.cancel()
                self.__latency_push_task = None
            
            self.__log(f"Latency push response: {resp_data}")
        else:
            self.__log("Repsonse is None")
        
        self.__is_sending_latency = False

    async def connect(self):
        async def __connect():
            options = {
                "servers": self.__base_url,
                "no_echo": True,
                "max_reconnect_attempts": 1200,
                "reconnect_time_wait": 1,
                "allow_reconnect": True,
                "token": self.api_key,
                "user_credentials": RawCredentials(self.__getCreds()),
                "reconnected_cb": self.__on_reconnect,
                "disconnected_cb": self.__on_disconnect,
                "error_cb": self.__on_error,
                "closed_cb": self.__on_closed
            }

            self.__natsClient = await nats.connect(**options)
            self.__jetstream = self.__natsClient.jetstream()
            self.__log("Connected to Relay!")

            self.__connected = True
            self.__disconnected = False

            await self.__get_namespace()

            await self.__subscribe_to_topics()

            # Call the callback function if present
            if self.CONNECTED in self.__event_func:
                if self.__event_func[self.CONNECTED]:
                    if inspect.iscoroutinefunction(self.__event_func[self.CONNECTED]):
                        await self.__event_func[self.CONNECTED]()
                    else:
                        self.__event_func[self.CONNECTED]()

            await self.quit_event.wait()

        await self.__run_in_background(__connect)

    async def __on_disconnect(self):
        self.__log("Disconnected from server")
        self.__disconnected = True
        self.__consumerMap.clear()
        self.__connected = False
        self.__disconnect_time = datetime.now(timezone.utc).isoformat();

        if self.DISCONNECTED in self.__event_func:
            if inspect.iscoroutinefunction(self.__event_func[self.DISCONNECTED]):
                await self.__event_func[self.DISCONNECTED]()
            else:
                self.__event_func[self.DISCONNECTED]()

        if not self.__manual_disconnect:
            # This was not a manual disconnect.
            # Reconnection attempts will be made
            if inspect.iscoroutinefunction(self.__on_reconnect_attempt):
                await self.__on_reconnect_attempt()
            else:
                self.__on_reconnect_attempt()

    async def __on_reconnect(self):
        self.__log("Reconnected!")
        self.__reconnecting = False
        self.__connected = True

        if self.RECONNECT in self.__event_func:
            if inspect.iscoroutinefunction(self.__event_func[self.RECONNECT]):
                await self.__event_func[self.RECONNECT](self.__RECONNECTED)
            else:
                self.__event_func[self.RECONNECT](self.__RECONNECTED)

        await self.__subscribe_to_topics()

        # Publish messages issued when client was in reconnection state
        output = await self.__publish_messages_on_reconnect()

        if len(output) > 0:
            if self.MESSAGE_RESEND in self.__event_func:
                if inspect.iscoroutinefunction(self.__event_func[self.MESSAGE_RESEND]):
                    await self.__event_func[self.MESSAGE_RESEND](output)
                else:
                    self.__event_func[self.MESSAGE_RESEND](output)

    async def __on_error(self, e):
        self.__log(f"There was an error: {e}")

        # Reconnecting error catch
        if str(e) == "":
            if self.RECONNECT in self.__event_func:
                if inspect.iscoroutinefunction(self.__event_func[self.RECONNECT]):
                    await self.__event_func[self.RECONNECT](self.__RECONNECTING)
                else:
                    self.__event_func[self.RECONNECT](self.__RECONNECTING)

    async def __on_closed(self):
        self.__log("Connection is closed")

        if self.__reconnected_attempt:
            self.__on_reconnect_failed()

        self.__offline_message_buffer.clear()
        self.__disconnect_time = None
        self.__connected = False

    async def __on_reconnect_attempt(self):
        self.__log(f"Reconnection attempt underway...")

        self.__connected = False
        self.__reconnected_attempt = True

        if self.RECONNECT in self.__event_func:
            if inspect.iscoroutinefunction(self.__event_func[self.RECONNECT]):
                await self.__event_func[self.RECONNECT](self.__RECONNECTING)
            else:
                self.__event_func[self.RECONNECT](self.__RECONNECTING)

    def __on_reconnect_failed(self):
        self.__log("Reconnection failed")

        self.__reconnected_attempt = False

        if self.RECONNECT in self.__event_func:
            self.__event_func[self.RECONNECT](self.__RECONN_FAIL)

    async def close(self):
        """
        Closes connection to server
        """
        if self.__natsClient != None:
            self.__reconnected = False
            self.__disconnected = True

            self.__manual_disconnect = True

            self.__offline_message_buffer.clear()

            await self.__natsClient.close()
            self.quit_event.set()
        else:
            self.__manual_disconnect = False

            self.__log("None / null socket object, cannot close connection")

    async def publish(self, topic, data):
        if topic == None:
            raise ValueError("$topic cannot be None.")
        
        if topic == "":
            raise ValueError("$topic cannot be an empty string.")
        
        if not isinstance(topic, str):
            raise ValueError("$topic must be a string.")
        
        if not self.is_topic_valid(topic):
            raise ValueError("$topic is not valid, use is_topic_valid($topic) to validate topic")
        
        self.__is_message_valid(data)

        if self.__connected:
            message_id = str(uuid.uuid4())

            message = {
                "client_id": self.__get_client_id(),
                "id": message_id,
                "room": topic,
                "message": data,
                "start": int(datetime.now(timezone.utc).timestamp())
            }

            # encoded = self.__encode_json(message)
            encoded = msgpack.packb(message)

            if topic not in self.__topic_map:
                self.__topic_map.append(topic)
            else:
                self.__log(f"{topic} exitsts locally, moving on...")

            topic = self.__get_stream_topic(topic)
            self.__log(f"Publishing to topic => {self.__get_stream_topic(topic)}")
            
            ack = await self.__jetstream.publish(topic, encoded)
            self.__log(f"Publish ack => {ack}")

            return ack != None
        else:
            self.__offline_message_buffer.append({
                "topic": topic,
                "message": data
            })

            return False

    async def on(self, topic, func):
        """
        Registers a callback function for a given topic or event.

        Args:
            topic (str): The topic or event name.
            func (callable): The callback function to execute.

        Returns:
            bool: True if successfully registered, False otherwise.
        """
        if topic == None:
            raise ValueError("$topic cannot be None.")
            
        if not isinstance(topic, str):
            raise ValueError("The topic must be a string.")
        
        if func == None:
            raise ValueError("$func cannot be None.")

        if not callable(func):
            raise ValueError("The callback must be a callable function.")
        
        if topic not in self.__event_func:
            self.__event_func[topic] = func
        else:
            return False

        __temp_topic_map = self.__topic_map.copy()
        __temp_topic_map += [self.CONNECTED, self.DISCONNECTED, self.RECONNECT, self.__RECONNECTED, 
                                self.__RECONNECTING, self.__RECONN_FAIL, self.MESSAGE_RESEND]

        if topic not in __temp_topic_map:
            if not self.is_topic_valid(topic):
                self.__event_func.pop(topic)
                raise ValueError("$topic is not valid, use is_topic_valid($topic) to validate topic")

            self.__topic_map.append(topic)

        if self.__connected:
            await self.__start_consumer(topic)
    
        return True  

    async def off(self, topic):
        """
        Unregisters a callback function for a given topic or event.

        Args:
            topic (str): The topic or event name.

        Returns:
            bool: True if successfully unregistered, False otherwise.
        """

        if topic == None:
            raise ValueError("$topic cannot be None.")
        
        if not isinstance(topic, str):
                raise ValueError("The topic must be a string.")
        
        if topic == "":
                raise ValueError("$topic can't be an empty string.")

        if topic in self.__event_func:
            self.__event_func.pop(topic)
            self.__topic_map.remove(topic)

            return await self.__delete_consumer(topic)
        else:
            return False

    async def history(self, topic, start=None, end=None):
        if topic == None:
            raise ValueError("$topic cannot be None.")

        if not isinstance(topic, str):
            raise ValueError("The topic must be a string.")
        
        if topic == "":
            raise ValueError("The topic must be NOT be an empty string.")
        
        if start == None:
            raise ValueError("$start cannot be None.")
        
        if not isinstance(start, datetime):
            raise ValueError("$start must be a datetime object")
        
        if end != None:
            if not isinstance(end, datetime):
                raise ValueError("$end must be a datetime object")
            
            if start > end:
                raise ValueError("$start > $end. $start must be lesser than $end")

        self.__log(f"TIMESTAMP => {start.isoformat()}")

        consumer = await self.__jetstream.subscribe(self.__get_stream_topic(topic), deliver_policy=nats_config.DeliverPolicy.BY_START_TIME, config=nats_config.ConsumerConfig(
            opt_start_time=start.isoformat(),
            ack_policy=nats_config.AckPolicy.EXPLICIT,
            name=f"{topic}_history_{uuid.uuid4()}"
        ))

        history = []

        while True:
            try:
                msg = await consumer.next_msg()

                if msg == None:
                    break

                dt_aware = msg.metadata.timestamp.timestamp()
                utc_timestamp = datetime.fromtimestamp(dt_aware, tz=timezone.utc)
                
                if end != None:
                    if utc_timestamp > end:
                        self.__log(f"{utc_timestamp.isoformat()} > {end.isoformat()}")
                        break

                # Decoding using msgpack
                data = msgpack.unpackb(msg.data, raw=False)

                history.append(data["message"])

                await msg.ack()
            except Exception as e:
                self.__log(e)
                break
        
        return history

    async def __delete_consumer(self, topic):
        if topic in self.__consumerMap:
            consumer = self.__consumerMap[topic]

            await consumer.unsubscribe()

            self.__consumerMap.pop(topic)

        return True

    async def __subscribe_to_topics(self):
        for topic in self.__topic_map:
            await self.__start_consumer(topic)

    async def __start_consumer(self, topic):
        self.__log(f"Starting consumer for {topic}")
        
        async def on_message(msg):
            now = datetime.now(timezone.utc).timestamp()
            
            data = msgpack.unpackb(msg.data, raw=False)
            self.__log(f"Received message => {data}")

            await msg.ack()

            if topic in self.__event_func and data["client_id"] != self.__get_client_id():
                if inspect.iscoroutinefunction(self.__event_func[topic]):
                    await self.__event_func[topic](data["message"])
                else:
                    self.__event_func[topic](data["message"])
            
            self.__log(f"Message processed for topic: {topic}")
            await self.__log_latency(now, data)

        startTime = datetime.now(timezone.utc).isoformat() if self.__disconnect_time is None else self.__disconnect_time

        consumer = await self.__jetstream.subscribe(self.__get_stream_topic(topic), 
                                                    stream=self.__get_stream_name(), 
                                                    cb=on_message,
                                                    config=nats_config.ConsumerConfig(
                                                        name=f"{topic}_consumer_{uuid.uuid4()}",
                                                        replay_policy=nats_config.ReplayPolicy.INSTANT,
                                                        deliver_policy=nats_config.DeliverPolicy.BY_START_TIME,
                                                        opt_start_time=startTime,
                                                        ack_policy=nats_config.AckPolicy.EXPLICIT
                                                    ))
        
        self.__consumerMap[topic] = consumer

    async def __log_latency(self, now, data):
        """
        Logs latency data to the server.
        """
        if data.get("client_id") == self.__get_client_id():
            self.__log("Skipping latency log for own message")
            return
        
        timezone = tzlocal.get_localzone().key
        self.__log(f"Timezone: {timezone}")

        latency = (now * 1000) - data.get("start")
        self.__log(now)
        self.__log(f"Latency => {latency}")

        self.__latency.append({
            "latency": latency,
            "timestamp": now
        })

        if self.__latency_push_task is None and self.__connected:
            self.__latency_push_task = asyncio.create_task(self.__delayed_latency_push(timezone))
        
        if len(self.__latency) >= 100 and not self.__is_sending_latency and self.__connected:
            self.__log(f"Push from Length Check: {len(self.__latency)}")

            await self.__push_latency({
                "timezone": timezone,
                "history": self.__latency.copy()
            })

    async def __delayed_latency_push(self, time_zone):
        await asyncio.sleep(30)
        self.__log("setTimeout called")

        if len(self.__latency) > 0:
            self.__log("Push from setTimeout")
            await self.__push_latency({
                "timezone": time_zone,
                "history": self.__latency.copy()
            })
        else:
            self.__log("No latency data to push")

        self.__latency_push_task = None

    # Utility functions
    def is_topic_valid(self, topic):
        if topic != None and isinstance(topic, str):
            array_check = topic not in [
                self.CONNECTED,
                self.RECONNECT,
                self.MESSAGE_RESEND,
                self.DISCONNECTED,
                self.__RECONNECTED,
                self.__RECONNECTING,
                self.__RECONN_FAIL
            ]

            TOPIC_REGEX = re.compile(r'^(?!\$)[A-Za-z0-9_,.*>$-]+$')

            space_star_check = " " not in topic and bool(TOPIC_REGEX.match(topic))

            return array_check and space_star_check
        else:
            return False
        
    def __get_client_id(self):
        return self.__natsClient.client_id
    
    def __retry_till_success(self, func, retries, delay, *args):
        method_output = None
        success = False

        for attempt in range(1, retries + 1):
            try:
                self.sleep(delay/1000)

                result = func(*args)

                method_output = result["output"]

                success = result["success"]

                if success:
                    self.__log(f"Successfully called {func.__name__}")
                    break
            except Exception as e:
                self.__log(f"Attempt {attempt} failed: {e}")
        
        if not success:
            self.__log(f"Failed to execute {func.__name__} after {retries} attempts")
    
        return method_output

    async def __publish_messages_on_reconnect(self):
        message_sent_status = []

        for message in self.__offline_message_buffer:
            output = await self.publish(message["topic"], message["message"])

            message_sent_status.append({
                "topic": message["topic"],
                "message": message["message"],
                "resent": output
            })

        self.__offline_message_buffer.clear()
        
        return message_sent_status
    
    def encode_json(self, data):
        return json.dumps(data).encode('utf-8')
    
    def __get_stream_name(self):
        if self.__namespace:
            return f"{self.__namespace}_stream"
        else:
            self.close()
            raise ValueError("$namespace is None, Cannot initialize program with None $namespace")
    
    def __get_stream_topic(self, topic):
        return f"{self.__topicHash}.{topic}"

    async def __run_in_background(self, func):
        task = asyncio.create_task(func())
        await task

    def __encode_json(self, data):
        try:
            return json.dumps(data).encode('utf-8')
        except Exception as e:
            raise ValueError(f"Error encoding JSON: {e}")

    def __log(self, msg):
        if self.__debug:
            print(msg)  # Replace with a logging system if necessary

    def __is_message_valid(self, msg):
        if msg == None:
            raise ValueError("$msg cannot be None.")
        
        if isinstance(msg, str):
            return True
        
        if isinstance(msg, numbers.Number):
            return True
        
        if isinstance(msg, dict):
            return True
        
        return False

    def sleep(self, seconds):
        time.sleep(seconds)

    def __getCreds(self):
        # To prevent \r\n from windows
        api_key = self.api_key.strip()
        secret = self.secret.strip()

        return f"""
-----BEGIN NATS USER JWT-----
{api_key}
------END NATS USER JWT------

************************* IMPORTANT *************************
NKEY Seed printed below can be used to sign and prove identity.
NKEYs are sensitive and should be treated as secrets.

-----BEGIN USER NKEY SEED-----
{secret}
------END USER NKEY SEED------

*************************************************************
""".strip()
    
    def __initDNSSpoof(self):
        self.__log("Init DNS Spoofing")
        _real_getaddrinfo = socket.getaddrinfo

        @wraps(_real_getaddrinfo)
        def patched_getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0):
            if host == "api2.relay-x.io":
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', port))]

            return _real_getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0)

        socket.getaddrinfo = patched_getaddrinfo