import paho.mqtt.client as mqtt # pip install paho-mqtt
import iothub_client # pip install azure-iot-hub, pip install azure-iot-device
from iothub_client import IoTHubModuleClient, IoTHubMessage

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
    print(msg.topic+" "+str(msg.payload))
    # Process the message (if necessary) before sending it to the cloud
    processed_message = msg.payload
    # Create an IoTHubMessage and send it to Azure IoT Hub
    message = IoTHubMessage(processed_message)
    iothub_client.send_event_async(message, send_confirmation_callback, 0)

# Callback for send confirmation from Azure IoT Hub
def send_confirmation_callback(message, result, user_context):
    print("Message sent to Azure IoT Hub with result: " + str(result))

def init_module():
    # Setup the Azure IoT Hub connection
    iothub_client = IoTHubModuleClient.create_from_connection_string(iothub_connection_string)
    iothub_client.connect()
    print("IoT Hub module client initialized.")
    # Setup the on-premises HiveMQ MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(hivemq_broker, hivemq_port)
    # Start the on-premises HiveMQ MQTT client loop
    mqtt_client.loop_forever()

def exit_module():
    print("Exiting...")

if __name__ == "__main__":
    try:
        init_module()
        while True:
            pass
    except KeyboardInterrupt:
        exit_module()