pip install paho-mqtt

import paho.mqtt.client as mqtt

# On-Premises HiveMQ configuration
hivemq_broker = "YOUR_HIVEMQ_BROKER_IP"
hivemq_port = 1883
hivemq_topic = "your/onprem/topic"

# Cloud-based MQTT broker configuration (Azure IoT Hub)
cloud_broker = "YOUR_CLOUD_BROKER_IP"
cloud_port = 8883
cloud_topic = "your/cloud/topic"

# Callback when the client connects to the on-premises HiveMQ
def on_connect(client, userdata, flags, rc):
    print("Connected to HiveMQ with result code: " + str(rc))
    client.subscribe(hivemq_topic)

# Callback when a message is received from the on-premises HiveMQ
def on_message(client, userdata, msg):
    # Process the message (if necessary) before sending it to the cloud
    processed_message = msg.payload

    # Publish the processed message to the cloud-based MQTT broker
    cloud_client.publish(cloud_topic, processed_message)

# Setup the cloud MQTT client
cloud_client = mqtt.Client()
cloud_client.connect(cloud_broker, cloud_port)

# Setup the on-premises HiveMQ MQTT client
hivemq_client = mqtt.Client()
hivemq_client.on_connect = on_connect
hivemq_client.on_message = on_message
hivemq_client.connect(hivemq_broker, hivemq_port)

# Start the on-premises HiveMQ MQTT client loop
hivemq_client.loop_start()

# Loop indefinitely to maintain the connection
while True:
    pass