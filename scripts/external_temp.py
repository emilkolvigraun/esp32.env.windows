# transmit temperature data to serial port with 2hz

from machine import Pin, ADC
import sys, time

# declaring external sensor pin
sensor = ADC(Pin(39, Pin.IN))

# defining voltage out
power = Pin(2, Pin.OUT)
power.value(1)

# configurations
sensor.atten(ADC.ATTN_6DB)
sensor.width(ADC.WIDTH_12BIT)

# run forever
while 1:
  
  # retrieving value from sensor
  value = sensor.read()
  voltage_conversion=((value.read()*2)/4096)
  value = ((voltage_conversion-0.5)/0.01)

  # write to serial port
  sys.stdout.write('{}'.format(round(value)))

  # sleet half a second
  time.sleep(0.5)