from machine import ADC, Pin
import time, UART

class exttempsensor:

    def __init__(self):
        self.pin_in = 12
        self.pin_out = 13 

        self.t_sensor_adc = ADC(Pin(self.pin_in, Pin.IN))
        self.t_sensor_pow = Pin(self.pin_out, Pin.OUT)

        self.t_sensor_adc.atten(ADC.ATTN_6DB)
        self.t_sensor_adc.width(ADC.WIDTH_12BIT)

        self.connection = UART(1, 115200)                         # init with given baudrate
        self.connection.init(115200, bits=8, parity=None, stop=1) # init with given parameter

    def run(self):
        while True:
            value = self.t_sensor_adc.read()
            self.connection.write('%s,%s'%(str(time.time()), str(value)))

        self.connection.deinit()