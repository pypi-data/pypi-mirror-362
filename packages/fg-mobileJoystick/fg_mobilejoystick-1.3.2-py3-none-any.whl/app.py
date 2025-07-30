#!/usr/bin/env python3

from flask import Flask, render_template
from flask_cors import CORS
from flightgear_python.fg_if import CtrlsConnection

# Load config
from config_load import (
    RX_HOST,
    RX_PORT,
    TX_HOST,
    TX_PORT,
    DEBUG,
    RUDDER_ENABLED,
    WEB_HOST,
    WEB_PORT,
)


app = Flask(__name__)
CORS(app)

neutralOrientation = (0, 0, 0)  # First init it to disable some warnings
currentOrientation = (0, 0, 0)


"""
    first Data: used by function data()
    first group of orientation data will be set as neutral position
"""
firstData = True


global previousCtrl
previousCtrl = [0, 0, 0]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data/<a>/<b>/<g>")  # Motion data Alpha Beta Gamma
def data(a, b, g):
    global firstData, neutralOrientation, currentOrientation
    a, b, g = float(a), float(b), float(g)

    if firstData:
        neutralOrientation = [a, b, g]
        if DEBUG:
            print("FD")
        firstData = False
    currentOrientation = [a, b, g]
    global ctrlsEventPipe
    global previousCtrl

    aileron = 0
    elevator = 0

    differenceA = currentOrientation[0] - neutralOrientation[0]
    differenceB = currentOrientation[1] - neutralOrientation[1]
    differenceG = currentOrientation[2] - neutralOrientation[2]

    # Normalize the difference to the range of -180 to 180 degrees
    differenceA = (differenceA + 180) % 360 - 180
    differenceB = (differenceB + 180) % 360 - 180
    differenceG = (differenceG + 180) % 360 - 180

    if -90 <= differenceB <= 90:
        aileron = differenceB / 90.0  # Scale to -1 to 1
    else:
        # Clamp to -1 or 1 if outside ±90 degrees
        aileron = -1 if differenceB < -90 else 1

    if -90 <= differenceG <= 90:
        elevator = differenceG / 90.0  # Scale to -1 to 1
    else:
        # Clamp to -1 or 1 if outside ±60 degrees
        elevator = -1 if differenceG < -90 else 1

    rudder = differenceB

    control = [aileron, rudder, elevator]
    ctrlsEventPipe.parent_send(control)
    previousCtrl = control
    return " "


def ctrlSend(ctrlsData, eventPipe):
    global previousCtrl
    if eventPipe.child_poll():
        orientation = eventPipe.child_recv()
        previousCtrl = orientation
    else:
        orientation = previousCtrl
    ctrlsData.aileron = orientation[0]
    ctrlsData.elevator = orientation[2]

    if RUDDER_ENABLED:
        ctrlsData.rudder = orientation[1]

    return ctrlsData


def appStart():
    app.run(WEB_HOST, WEB_PORT, debug=DEBUG)


ctrlsConn = CtrlsConnection()
ctrlsEventPipe = ctrlsConn.connect_rx(RX_HOST, RX_PORT, ctrlSend)
ctrlsConn.connect_tx(TX_HOST, TX_PORT)
ctrlsConn.start()
