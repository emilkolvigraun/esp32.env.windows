print('- loading external temperature sensor')
from external_temp import exttempsensor

print('- init external temperature sensor')
sensor = exttempsensor()

print('- starting sensor data collection')
sensor.run()






