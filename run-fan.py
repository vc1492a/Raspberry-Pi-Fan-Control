import os
import re
from time import sleep
import RPi.GPIO as GPIO

pin = 18  # The pin ID, edit here to change it
maxTMP = 70  # The maximum temperature in Celsius after which we trigger the fan
stopTMP = maxTMP - 10


def setup() -> tuple:
    """
    Sets the mode and warnings for the GPIO setup.
    :return: An empty tuple.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    return ()


def get_cpu_temperature() -> float:
    """
    Retrieves the CPU temperature of the Raspberry Pi using vcgencmd.
    :return: A float value which indicates the CPU temperature.
    """
    res = os.popen("vcgencmd measure_temp").readline()
    temp = re.findall("\d+\.\d+", res)[0]
    print("temp is {0}".format(temp))  # Uncomment here for testing
    return temp


def fan_on() -> tuple:
    """
    Turns the fan on by setting the GPIO pin mode.
    :return: An empty tuple.
    """
    set_pin(True)
    return ()


def fan_off() -> tuple:
    """
    Turns the fan off by setting the GPIO pin mode.
    :return: An empty tuple.
    """
    set_pin(False)
    return ()


def get_temp() -> tuple:
    """
    Retrieves the CPU temperature of the Raspberry Pi and turns the fan
    on or off based on the read value.
    :return: An empty tuple.
    """
    cpu_temp = float(get_cpu_temperature())
    if cpu_temp > maxTMP:
        fan_on()
    elif cpu_temp < stopTMP:
        fan_off()
    return ()


def set_pin(mode: bool) -> tuple:  # A little redundant function but useful if you want to add logging
    """
    Sets the GPIO pin to the mode needed depending on the CPU temperature.
    :param mode: A boolean, True or False.
    :return: An empty tuple.
    """
    GPIO.output(pin, mode)
    return ()


try:
    setup()
    while True:
        get_temp()
        sleep(5)  # Read the temperature every 5 sec, increase or decrease this limit if you want
except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()  # resets all GPIO ports used by this program
