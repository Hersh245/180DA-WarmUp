import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

counter = 0
client.publish("180DA/counter/topic", str(counter))
time.sleep(2)

client.disconnect()
