import requests
import openpyxl

#Webscraping Amazon Price using


#Requesting cryptocurrency prices form CoinBase. 
r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
crypto='BTC'
#print(r['data']['rates'][crypto])

#Tracking Information in Excel Document
xbook=openpyxl.load_workbook('Amazon-Crypto-Data.xlsx')
print(xbook)
