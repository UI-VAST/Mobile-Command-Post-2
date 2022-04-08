# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=wrong-import-position
import time
from Logger import Logger
from adafruit_rockblock import RockBlock

import serial

debug = True
tsym = 'F'
port = "/dev/serial0"
baud = 19200
logger = Logger("RockBlock", debug)
# uart = serial.Serial("/dev/serial0", 19200)
uart = serial.Serial(port, baud)
# uart = board.UART()
# uart.baudrate = 19200

# via USB cable
# import serial
# uart = serial.Serial("/dev/ttyUSB0", 19200)

logger.log("Initiating Rock Block on port " + str(port) + ", with baud rate " + str(baud) + ", and debugging " + "True" if debug else "False")
rb = RockBlock(uart)
logger.log("Model: ", str(rb.model))
logger.log("System Time: ", str(rb.system_time))
logger.log("Signal Quality: ", str(rb.signal_quality))

time.sleep(8)
status = (-1, 0, 0)
retry = 0
counter = 0
data = ()
while 1:
    # set the text
    print(rb.signal_quality)
    # if rb.ring_indication[1] == '001':
    if status[0] == -1 and counter % 180 == 0:
        # try a satellite Short Burst Data transfer
        status = rb.satellite_transfer()
        logger.log("Talking to satellite... ", str(status))  # loop as needed

    if status[0] > 8 and counter % 10 == 0:
        status = rb.satellite_transfer()
        logger.log(str(retry), str(status))
        logger.log("Signal Quality: ", str(rb.signal_quality))
        retry += 1

    if 8 >= status[0] > -1:
        data = rb.text_in
        logger.log("Getting Text... ", data)
        logger.log("Received!")
        status = (-1, 0, 0, 0, 0, 0)
        retry = 0
        counter = 0
    counter += 1

    time.sleep(5)  # Sleep for 1 second

