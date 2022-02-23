## Necessary Python Libararies
# Requesting Cryptocurrency Data form Coinbase
import requests
# Manipulating Excel Documents
import openpyxl
import time
# Email Delivery
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

## Webscraping Amazon Price using


# Requesting cryptocurrency prices form CoinBase. 
r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
crypto='BTC'
#print(r['data']['rates'][crypto])


## Tracking Information in Excel Document
#Excel Manipulation
xbook=openpyxl.load_workbook('Amazon-Crypto-Data.xlsx')
current_hour_minute=time.strftime("%H:%M",time.localtime())


## Email Delivery.
# Defining relevant variables.
email_sender="kitten.in.superposition@gmail.com"
password='hinojos123'
subject='This is a test written by me. Thanks for reading!'
email_receiver='noah.hinojos@gmail.com'

# SMTP connection and email delivery
smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtp_obj.login(email_sender, password)
smtp_obj.sendmail(email_sender,email_receiver,subject)

# Ending SMTP Connection.
smtp_obj.quit()
