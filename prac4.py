import busio
import threading
import datetime
import time
import RPi.GPIO as GPIO
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

timeA = 1
global startTime
global temp
global chan


def timeBtn(a):
    global timeA
    if timeA == 1:
        timeA = 5
    elif timeA == 5:
        timeA = 10
    elif timeA == 10:
        timeA = 1
    print("Sampling time set to: " + str(timeA))


def setup():
    time_Btn = 17
    global chan
    global startTime
    global temp
    GPIO.setup(time_Btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(time_Btn, GPIO.FALLING,
                          callback=timeBtn, bouncetime=200)

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    # create an analog input channel on pin 0
    temp = AnalogIn(mcp, MCP.P1)
    # create an analog input channel on pin 1
    chan = AnalogIn(mcp, MCP.P2)
    # startTime = datetime.datetime.now()
    startTime = datetime.datetime.today().timestamp()

# def round_seconds(obj: datetime.datetime) -> datetime.datetime:
#     if obj.microsecond >= 500_000:
#         obj += datetime.timedelta(seconds=1)
#     return obj.replace(microsecond=0)
# rounded_down_datetime = raw_datetime.replace(microsecond=0)

# def round_seconds(date_time_object):
#     new_date_time = date_time_object
#     if new_date_time.microsecond >= 500000:
#         new_date_time = new_date_time + datetime.timedelta(seconds=1)
#     return new_date_time.replace(microsecond=0)


def get_value():
    global startTime
    global chan
    global temp
    ambTemp = (temp.voltage - 0.5) * 100
    timeOut = (str((int(round(datetime.datetime.today().timestamp(), 0))
                    ) - int(round(startTime, 0))) + "            ")[0:13]
    tempOut = (str(temp.value) + "               ")[0:17]
    ambOut = (str(round(ambTemp))+"            ")[0:12]
    lightOut = str(chan.value)
    print(timeOut+tempOut+ambOut+lightOut)


def print_time_thread():
    """
    This function prints the time to the screen every five seconds
    """
    thread = threading.Timer(timeA, print_time_thread)
    thread.daemon = True
    thread.start()
    get_value()
    secs = time


if __name__ == "__main__":
    # print_time_thread() # call it once to start the thread
    setup()
    print("Runtime      Temp Reading     Temp        Light Reading")
    # get_value()
    print_time_thread()
    # Tell our program to run indefinitely
    while True:
        pass
