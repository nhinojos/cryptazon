## Necessary Python Libararies.
# Requesting Cryptocurrency Data form Coinbase.
import requests
# Manipulating Excel Documents.
from openpyxl import Workbook
import time
# Email Delivery.
import smtplib


## Initial Prompt to either use same workbook or generate new workbook.


## Webscraping Amazon Price using.


## Tracking Information in Excel Document.
#Generates new Excel workbook.
def generateWorkbook(filename,cryptolist):
    # Creating workbook object and data worksheet sub-object.
    wb=Workbook()
    ws_data=wb.active
    ws_data.title = "Data"
    # Labeling headers.
    ws_data['A1']="Currency"
    ws_data['B1']="Date" # Should range B1:n1, where B to n are the dates recorded.
    # Labeling cryptos of choice in the left-most column.
    for i,crypto in enumerate(cryptolist):
        ws_data['A'+str(i+2)]=crypto
    #Creating separet worksheet analyze data
    ws_analysis=wb.create_sheet("Analysis")
    #Saving workbook
    wb.save(filename+'.xlsx')
    return wb

# Requesting current cryptocurrency prices from CoinBase. 
r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
cryptolist=['BTC','ETH','LTC'] # Can be any list of crypto.
current_hour_minute=time.strftime("%H:%M",time.localtime())
"""print(r['data']['rates']['BTC])"""

#Generating test workbook
wb=generateWorkbook('testworkbook',cryptolist)



## Email Delivery.
# Defining relevant variables.
email_sender="kitten.in.superposition@gmail.com"
password='hinojos123'
subject='This is a test written by me. Thanks for reading!'
email_receiver='noah.hinojos@gmail.com'

# SMTP connection and email delivery.
smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_obj.login(email_sender, password)
smtp_obj.sendmail(email_sender,email_receiver,subject)

# Ending SMTP Connection.
smtp_obj.quit()
