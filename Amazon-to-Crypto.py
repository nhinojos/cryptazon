## Necessary Python Libararies.
# Requesting Cryptocurrency Data form Coinbase.
import requests
# Manipulating Excel Documents.
from openpyxl import Workbook
import os.path 
import time
# Email Delivery.
import smtplib



## Webscraping Amazon Price using.



## Tracking Information in Excel Document.
# Generates new Excel workbook.
def generateWorkbook(crypto_list):
    # Creating workbook object and data worksheet sub-object.
    wb=Workbook()
    ws_data=wb.active
    ws_data.title = "Data"
    ws_data['A1']="Currency"
    ws_data['B1']="Date" # Should range B1:n1, where B to n are the dates recorded.
    
    for i,crypto in enumerate(crypto_list):
        ws_data['A'+str(i+2)]=crypto
    
    wb.create_sheet("Analysis")
    wb.save('product_history.xlsx')
    return wb


## Intializes new workbook if there is not one already in the directory. 
if not os.path.exists('product_history.xlsx'):
    print('No workbook found in directory.')
    print('Initializing workbook generation.')
    product_link=input('Please provide a link to the amazon product:')
    
    print('Now, here are a list of cryptocurrencies available to track')
    r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
    crypto_options=r['data']['rates'].keys()
    crypto_string=''
    for i,crypto in enumerate(crypto_options):
        crypto_string+=crypto+(10-len(crypto))*' '
        if i%16==0:
            print(crypto_string)
            crypto_string=''
    
    print('Please type the abbreviated cryptocurrencies you would like to track, separated by commas:')
    crypto_list=input()
    crypto_list.upper()
    crypto_list.replace(' ','')
    crypto_list.split(',')
    generateWorkbook(crypto_list)


## Requesting current cryptocurrency prices from CoinBase. 
r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
cryptolist=['BTC','ETH','LTC'] # Can be any list of crypto.
current_hour_minute=time.strftime("%H:%M",time.localtime())
"""print(r['data']['rates']['BTC])"""


#Generating test workbook
wb=generateWorkbook('product_history',cryptolist)



## Email Delivery.
# Defining relevant variables.
email_sender="kitten.in.superposition@gmail.com"
password='hinojos123'
subject='This is a test written by me. Thanks for reading!'
email_receiver='noah.hinojos@gmail.com'

# SMTP connection and email delivery.
smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_obj.login(email_sender, password)
#smtp_obj.sendmail(email_sender,email_receiver,subject)

# Ending SMTP Connection.
smtp_obj.quit()
