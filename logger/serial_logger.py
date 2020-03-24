import serial, time

input = serial.Serial('COM5', 115200)

file = open('log.txt', 'a')
try:
    while True:
        value = input.read(4).decode('utf-8')
        print(value)
        file.write('%s,%s\n'%(str(time.time()), str(value)))
except KeyboardInterrupt:
    file.close()
    exit('see log.txt')
