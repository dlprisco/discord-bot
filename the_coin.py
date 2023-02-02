from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/bitcoin'
#parameters = {
#  'start':'1',
#  'limit':'5000',
#  'convert':'USD'
#}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '4d9d9591-bba7-4c45-9db1-25ce9d62a69c',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url)#, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  
