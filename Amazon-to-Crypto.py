import requests

#Requesting cryptocurrency prices form CoinBase. 
r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
crypto='BTC'
print(r['data']['rates'][crypto])

