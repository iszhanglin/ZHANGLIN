import json
import time
import paho.mqtt.client as mqtt
from MqttSign import AuthIfo
import threading


latitude = 0
longitude = 0


# set the device info, include product key, device name, and device secret
productKey = "jjq59Qh4oGa"
deviceName = "connect1"
deviceSecret = "e41ffd18b065afb229a9cdf640a557bc"

# set timestamp, clientid, subscribe topic and publish topic
timeStamp = str((int(round(time.time() * 1000))))
clientId = "192.168.****"
subTopic = "/" + productKey + "/" + deviceName + "/user/get"
pubTopic = "/" + productKey + "/" + deviceName + "/user/update"
pubTopic1 = "/" + productKey + "/" + deviceName + "/user/go"

# set host, port
host = productKey + ".iot-as-mqtt.cn-shanghai.aliyuncs.com"
# instanceId = "***"
# host = instanceId + ".mqtt.iothub.aliyuncs.com"
port = 1883

# set tls crt, keepalive
tls_crt = "root.crt"
keepAlive = 300

# calculate the login auth info, and set it into the connection options
m = AuthIfo()
m.calculate_sign_time(productKey, deviceName, deviceSecret, clientId, timeStamp)
client = mqtt.Client(m.mqttClientId)
client.username_pw_set(username=m.mqttUsername, password=m.mqttPassword)
client.tls_set(tls_crt)

data = {
    "CMD": 3,
    "Temper": 2,
    "Hum": 2

}
payload = json.dumps(data)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect aliyun IoT Cloud Sucess")
    else:
        print("Connect failed...  error code is:" + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    payloads = msg.payload.decode()
    print("receive message ---------- topic is : " + topic)
    print("receive message ---------- payloads is : " + payloads)
    payloads = json.loads(payloads)
    if "纬度" in payloads:
        global latitude, longitude
        latitude = payloads["纬度"]
        longitude = payloads["经度"]

    if ("thing/service/property/set" in topic):
        on_thing_prop_changed(client, msg.topic, msg.payload)


"""
def get_latitude_longitude():
    global latitude, longitude
    print(latitude, longitude)
    return latitude, longitude
"""


def on_thing_prop_changed(client, topic, payload):
    post_topic = topic.replace("service", "event")
    post_topic = post_topic.replace("set", "post")
    Msg = json.loads(payload)
    params = Msg['params']
    post_payload = "{\"params\":" + json.dumps(params) + "}"
    print("reveice property_set command, need to post ---------- topic is: " + post_topic)
    print("reveice property_set command, need to post ---------- payload is: " + post_payload)
    client.publish(post_topic, post_payload)


def connect_mqtt():
    client.connect(host, port, keepAlive)
    return client


def publish_message():
    # publish 5 messages to pubTopic("/a1LhUsK****/python***/user/update")
    client.publish(pubTopic1, payload)
    print(111)
    time.sleep(2)


def subscribe_topic():
    # subscribe to subTopic("/a1LhUsK****/python***/user/get") and request messages to be delivered
    client.subscribe(subTopic)
    print("subscribe topic: " + subTopic)


client.on_connect = on_connect
client.on_message = on_message
client = connect_mqtt()
client.loop_start()
time.sleep(0)

subscribe_topic()
publish_message()

def long_run():
    while not stop_event.is_set():
        time.sleep(10)
        #publish_message()

def stop():
    stop_event.set()

def to_stop():
    stop()
    thred.join()


thred = threading.Thread(target=long_run)
thred.daemon = False
stop_event = threading.Event()
thred.start()







"""
class LongRunThread(threading.Thread):
    def __init__(self):
        super(LongRunThread, self).__init__()
        self.stop_event = threading.Event()
        self.run()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(10)
            publish_message()

    def stop(self):
        self.stop_event.set()


# 创建并启动线程
thred = LongRunThread()
thred.start()

# 在关闭应用程序时停止线程
thred.stop()
thred.join()

"""