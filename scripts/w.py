import network, socket, time
from machine import Pin, I2C

def conv(data:bytes):
    return (data[0]<<8 | data[1])

def connect(ssid:str, passw:str):
    conn = network.WLAN(network.STA_IF)

    if not conn.isconnected():
        print('connecting to wifi...')
        conn.active(True)
        conn.connect(ssid, passw)
        while not conn.isconnected():
            pass
        print('network config:', conn.ifconfig())
    
    return conn

def post(payload, url, port):
    s = socket.socket()
    s.connect((url,port))
    req = "POST /store/public HTTP/1.1\r\nHost: " + url +":"+ str(port) +"\r\nConnection: close\r\nContent-Length: " + str(len(bytes(payload, 'utf-8'))) + "\r\nContent-Type: text/csv\r\n\r\n"
    s.send(bytes(req, 'utf-8'))
    s.send(bytes(payload, 'utf-8'))
    s.close()
    print('sent payload:', payload)

connection = connect('HomeBox-5C00_2.4G', '5g5gb64ha')

i2c = I2C(-1, scl=Pin(4), sda=Pin(5))
i2c.scan()
i2c.writeto(0x23, bytes([0x00])) # off
i2c.writeto(0x23, bytes([0x01])) # on
i2c.writeto(0x23, bytes([0x07])) # reset
i2c.writeto(0x23, bytes([0x01])) # on
i2c.writeto(0x23, bytes([0x13])) # highres

i = 0

while True:

    if not connection.isconnected():
        connection = connect('HomeBox-5C00_2.4G', '5g5gb64ha')
        
    l_data = i2c.readfrom(0x23, 2)
    t_data = i2c.readfrom(0x5F, 2)

    payload = str(time.time()) + ',' + str(conv(l_data) / (1.2 * 2.0)) + ','+ str(conv(t_data)) + ',' + str(i)
    post(payload, '83.93.57.32', 8000)

    i+=1

    time.sleep(2)