import network
import socket

def connect():
    conn = network.WLAN(network.STA_IF)

    if not conn.isconnected():
        print('connecting to wifi...')
        conn.active(True)
        conn.connect('ssid', 'pass')
        while not conn.isconnected():
            pass
        print('network config:', conn.ifconfig())

def post(data, url):
    _, _, host, path = url.split('/', 3)
    address = socket.getaddrinfo(host, 8000)[0][-1]
    s = socket.socket()
    s.connect(address)
    
    header = 'POST /%s HTTP/1.0\r\nHost: %s'%(path, host)
    payload = ''

    s.send(bytes('%s%s'%(header,payload), 'utf-8'))
    s.close()