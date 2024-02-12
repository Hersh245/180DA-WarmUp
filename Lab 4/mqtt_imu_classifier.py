import paho.mqtt.client as mqtt

# MQTT Broker settings
mqttServer = "mqtt.eclipseprojects.io"
mqttPort = 1883
mqttTopic = "180DA/imu/data"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqttTopic)


last_imu_values = None


def classify_action(current_values, last_values):
    # Thresholds for detecting motion and determining action
    acc_change_threshold = 0.2  # Adjust based on sensitivity needed
    gyro_change_threshold = 20  # Adjust based on sensitivity needed

    if last_values is None:
        # If no previous data, can't calculate change; might be idle or unknown
        return "Unknown or Idle"

    # Calculate the change in accelerometer and gyroscope values
    acc_change = [
        abs(curr - last) for curr, last in zip(current_values[:3], last_values[:3])
    ]
    gyro_change = [
        abs(curr - last) for curr, last in zip(current_values[3:], last_values[3:])
    ]

    acc_change_magnitude = sum(acc_change)
    gyro_change_magnitude = sum(gyro_change)

    # Classify based on the change in IMU readings
    if (
        acc_change_magnitude < acc_change_threshold
        and gyro_change_magnitude < gyro_change_threshold
    ):
        return "Idle"
    elif acc_change[0] > acc_change_threshold:  # Significant change in X-axis
        return "Forward Push"
    elif acc_change[2] > acc_change_threshold:  # Significant change in Z-axis
        return "Upward Lift"
    elif gyro_change_magnitude > gyro_change_threshold:
        return "Circular Rotation"
    else:
        return "Unknown"


def on_message(client, userdata, msg):
    global last_imu_values
    # Example payload: "Acc: 0.07, 0.01, -0.03, Gyro: 1.2, 0.5, -0.4"
    # Splitting the payload into components and extracting only the numeric values
    data_str = msg.payload.decode()
    try:
        # Extracting numeric values assuming the format includes labels 'Acc:' and 'Gyro:'
        parts = data_str.replace("Acc: ", "").replace("Gyro: ", "").split(", ")
        data = [float(x) for x in parts]

        # Now 'data' will be [0.07, 0.01, -0.03, 1.2, 0.5, -0.4]
        action = classify_action(data, last_imu_values)
        print(f"Action: {action}")
        last_imu_values = data
    except ValueError as e:
        print(f"Error processing message '{data_str}': {e}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttServer, mqttPort, 60)  # Connect to MQTT broker
client.loop_forever()  # Start processing MQTT messages
