import paho.mqtt.client as mqtt
from iothub_client import IoTHubModuleClient, IoTHubMessage, IoTHubMessageDispositionResult

# On-Premises HiveMQ configuration
hivemq_broker = "YOUR_HIVEMQ_BROKER_IP"
hivemq_port = 1883
hivemq_topic = "your/onprem/topic"

# Azure IoT Hub connection string
iothub_connection_string = "YOUR_IOTHUB_CONNECTION_STRING"
iothub_module_id = "YOUR_MODULE_ID"  # This is the name of your Azure IoT Edge module

# Callback when the client connects to the on-premises HiveMQ
def on_connect(client, userdata, flags, rc):
    print("Connected to HiveMQ with result code: " + str(rc))
    client.subscribe(hivemq_topic)

# Callback when a message is received from the on-premises HiveMQ
def on_message(client, userdata, msg):
    # Process the message (if necessary) before sending it to Azure IoT Hub
    processed_message = msg.payload

    # Create an IoTHubMessage and send it to Azure IoT Hub
    message = IoTHubMessage(processed_message)
    iothub_client.send_event_async(message, send_confirmation_callback, 0)

# Callback for send confirmation from Azure IoT Hub
def send_confirmation_callback(message, result, user_context):
    print("Message sent to Azure IoT Hub with result: " + str(result))

# Setup the on-premises HiveMQ MQTT client
hivemq_client = mqtt.Client()
hivemq_client.on_connect = on_connect
hivemq_client.on_message = on_message
hivemq_client.connect(hivemq_broker, hivemq_port)

# Setup the Azure IoT Hub client
iothub_client = IoTHubModuleClient.create_from_connection_string(iothub_connection_string)
iothub_client.connect()

# Start the on-premises HiveMQ MQTT client loop
hivemq_client.loop_start()

# Loop indefinitely to maintain the connection
while True:
    pass
