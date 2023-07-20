import paho.mqtt.client as mqtt
import iothub_client
from iothub_client import IoTHubModuleClient

def print_message(message):
    print(message)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("my/topic")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def init_module():
    module_client = IoTHubModuleClient.create_from_edge_environment()
    module_client.set_module_twin_callback(print_message, None)
    module_client.set_connection_status_callback(print_message, None)
    print("IoT Hub module client initialized.")
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883)
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