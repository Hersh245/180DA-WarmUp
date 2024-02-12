import paho.mqtt.client as mqtt

# MQTT Broker settings
mqttServer = "mqtt.eclipseprojects.io"
mqttPort = 1883
mqttTopic = "180DA/imu/data"


# Callback when connecting to the MQTT server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqttTopic)


# Callback when receiving a message from the MQTT server
def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttServer, mqttPort, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()
