import paho.mqtt.client as mqtt
import ssl as ssl_module
import time
from threading import Lock

class MQTTClient:
    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0, 
                 ssl=False, ssl_params=None):
        """初始化MQTT客户端"""
        self.client_id = client_id
        self.server = server
        self.port = port or (8883 if ssl else 1883)
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.ssl = ssl
        self.ssl_params = ssl_params or {}
        self.connected = False
        self.topic_callback = {}
        self.lock = Lock()
        
        # 创建paho-mqtt客户端
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
        
        # 设置回调
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        # 设置认证
        if user:
            self.client.username_pw_set(user, password)
            
        # 设置SSL
        if ssl:
            if "ca_certs" in self.ssl_params:
                self.client.tls_set(
                    ca_certs=self.ssl_params.get("ca_certs"),
                    certfile=self.ssl_params.get("certfile"),
                    keyfile=self.ssl_params.get("keyfile"),
                    cert_reqs=ssl_module.CERT_REQUIRED,
                    tls_version=ssl_module.PROTOCOL_TLS,
                )
            else:
                self.client.tls_set(
                    cert_reqs=ssl_module.CERT_REQUIRED,
                    tls_version=ssl_module.PROTOCOL_TLS,
                )
                
            if "server_hostname" in self.ssl_params:
                self.client.tls_insecure_set(True)
    
    def _on_connect(self, client, userdata, flags, rc):
        """连接回调"""
        self.connected = rc == 0
        if self.connected:
            # 重新订阅所有主题
            with self.lock:
                for topic, (callback, qos) in self.topic_callback.items():
                    self.client.subscribe(topic, qos)
    
    def _on_message(self, client, userdata, msg):
        """消息回调"""
        with self.lock:
            if msg.topic in self.topic_callback:
                callback, _ = self.topic_callback[msg.topic]
                # 与micropython兼容的回调格式：(topic, msg)
                callback((msg.topic, msg.payload))
    
    def _on_disconnect(self, client, userdata, rc):
        """断开连接回调"""
        self.connected = False
    
    def connect(self, clean_session=True):
        """连接到MQTT服务器"""
        self.client.connect(self.server, self.port, self.keepalive)
        self.client.loop_start()  # 在后台启动消息循环
        return True
    
    def disconnect(self):
        """断开连接"""
        self.client.disconnect()
        self.client.loop_stop()
        return True
    
    def subscribe(self, topic, callback, qos=0):
        """订阅主题"""
        with self.lock:
            self.topic_callback[topic] = (callback, qos)
            if self.connected:
                self.client.subscribe(topic, qos)
        return True
    
    def unsubscribe(self, topic):
        """取消订阅"""
        with self.lock:
            if topic in self.topic_callback:
                del self.topic_callback[topic]
                if self.connected:
                    self.client.unsubscribe(topic)
        return True
    
    def publish(self, topic, msg, retain=False, qos=0):
        """发布消息"""
        self.client.publish(topic, msg, qos=qos, retain=retain)
        return True
    
    def check_msg(self):
        """检查消息 - 在micropython中需要手动调用处理消息
           在CPython实现中，由于使用了loop_start()，这个方法实际上不需要做什么
        """
        # paho-mqtt的loop_start()已经在后台处理消息
        pass