# transmit temperature data to serial port

from machine import Pin, ADC
import sys, time

# declaring external sensor pin
sensor = ADC(Pin(39, Pin.IN))

# defining voltage out (VDD)
power = Pin(2, Pin.OUT)
power.value(1)

# configurations
sensor.atten(ADC.ATTN_6DB)
sensor.width(ADC.WIDTH_12BIT)

# define list of values to obtain mean
values = list()

# run forever
while 1:
    # retrieving value from sensor
    value = sensor.read()

    # append each value
    values.append(float(value))

    # get the mean of 100 values
    if len(values) >= 100:

        # calculate mean
        mean_value = sum(values)/len(values)

        # write to serial port
        sys.stdout.write('{}'.format(round(mean_value)))

        # reset list
        values = list()