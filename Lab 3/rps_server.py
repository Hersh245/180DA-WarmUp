import paho.mqtt.client as mqtt

# MQTT Client Setup
broker_address = "test.mosquitto.org"
server = mqtt.Client("RPS_Server")
server.connect(broker_address, 1883, 60)

players = {}
results_published = False


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("rps_game/#")


def on_message(client, userdata, msg):
    global results_published
    player_id = msg.topic.split("/")[-1]
    choice = msg.payload.decode()

    players[player_id] = choice

    if len(players) == 2 and not results_published:
        determine_winner()
        results_published = True


def determine_winner():
    player_ids = list(players.keys())
    choices = list(players.values())

    result = ""
    if choices[0] == choices[1]:
        result = "Draw"
    elif (
        (choices[0] == "Rock" and choices[1] == "Scissors")
        or (choices[0] == "Paper" and choices[1] == "Rock")
        or (choices[0] == "Scissors" and choices[1] == "Paper")
    ):
        result = f"{player_ids[0]} Wins!"
    else:
        result = f"{player_ids[1]} Wins!"

    # Publish results to both players
    for player_id in player_ids:
        server.publish(f"rps_game_result/{player_id}", result)


server.on_connect = on_connect
server.on_message = on_message

# Main Loop
server.loop_forever()
