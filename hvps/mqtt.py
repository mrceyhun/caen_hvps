#!/usr/bin/env python3

#     MacOS mosquitto simple service run
#
#     Install:
#       brew install mosquitto
#       /usr/local/opt/mosquitto/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
#
#     Terminal 1: pub
#       from hvps import mqtt as mymqtt
#       mymqtt.publish(topic="test", msg="test message 1")
#
#     Terminal 2: sub
#       from hvps import mqtt as mymqtt
#       mymqtt.subscribe(topic="test")
#
#     How to subscribe "test" topic via mosquitto cli
#       mosquitto_sub -d -t test

import time
from paho.mqtt import client as mqtt_client

mqtt_host = "127.0.0.1"  # os.environ["MQTT_HOST"]
mqtt_port = 1883


def get_client():
    """Get mqtt connection client"""
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(mqtt_host, mqtt_port)
    return client


def on_connect(client, userdata, flags, rc):
    """Mqtt client on connect method"""
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def subscribe(topic):
    """Subscribes to mqtt topic and follow forever"""
    client = get_client()  # connect and get client

    def on_message(client, userdata, msg):
        """Subscribed topic on message action"""
        print("recv", msg.topic, msg.payload)  # You can read message here and do anything you want

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    client.subscribe(topic)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()


def publish(topic, msg):
    client = get_client()  # connect and get client
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
