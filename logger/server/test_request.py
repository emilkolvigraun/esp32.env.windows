import requests

payload = '123456789,12,23,1'
url = 'http://locahost:8000/store/local'
requests.post(url, data=payload)