import requests

payload = '123456789,12,23,1'
url = 'http://83.93.57.32:8000/store/local'
r = requests.post(url, data=payload)
print(r)