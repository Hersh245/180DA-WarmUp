import paho.mqtt.client as mqtt


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    counter = int(msg.payload.decode())
    print(f"Received count: {counter}")
    counter += 1
    client.publish("180DA/counter/topic", str(counter))


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("180DA/counter/topic")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()
