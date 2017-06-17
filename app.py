from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
from flask import Flask
import json

messages = {}


def register_message(msg):
    messages[msg.mid] = msg.data


usbtin = USBtin()
usbtin.connect("/dev/ttyACM0")
usbtin.add_message_listener(register_message)
usbtin.open_can_channel(125000, USBtin.ACTIVE)

app = Flask(__name__)


@app.route("/", methods="GET")
def get_messages():
    return json.dumps(messages)


@app.route("/<int: message_id>", methods="GET")
def get_message(message_id):
    return json.dumps(messages[message_id])

