## Necessary Libararies.
import requests 
from openpyxl import Workbook # Manipulating Excel Spreadsheet. Documentation: https://openpyxl.readthedocs.io/en/stable/
import os.path
import yagmail #Simplified Gmail Delivery. Documentation: https://github.com/kootenpv/yagmail

##Function Creation
#Delivering with Gmail easily using yagmail
def emailMessage(title,content,receiver,sender):
    """ 
    If you haven't done so already, register your email 
    and password using python's secure  library 
    'keyring.' Then, run the following command:
    yagmail.register(gmailusername,mygmailpassword)
    
    You may also need to confirm 3rd party access to 
    your Gmail account in order to run this program. 
    """
    yagmail.SMTP(sender).send(receiver,title,content)
    return

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
    print("No workbook titled 'product_history.xlsx' found in directory.")
    while True:
        response=input('Would you like to generate a new workbook?(y/n)')
        response.lower()
        response.strip()
        if response in {'y','n','yes','no'}:
            if response in {'n','no'}:
                print("Please ensure a valid workbook titled 'product_history.xlsx' exists before restarting.")
                quit()
            break
        else:
            print('That is not a valid response.')
    print('Initializing workbook generation.')

    product_link=input('Please provide a link to the amazon product:')
    
    #Requesting Coinbase Data
    print('Here are the list of cryptocurrencies available to track')
    r=requests.get('https://api.coinbase.com/v2/exchange-rates').json()
    crypto_options=r['data']['rates'].keys()
    crypto_string=''
    for i,crypto in enumerate(crypto_options):
        crypto_string+=crypto+(10-len(crypto))*' '
        if i%16==0:
            print(crypto_string)
            crypto_string=''

    #Tracking proper currencies. 
    print('Please type the abbreviated cryptocurrencies you would like to track, separated by commas:')
    crypto_list=input()
    crypto_list.upper()
    crypto_list.replace(' ','')
    crypto_list.split(',')
    generateWorkbook(crypto_list)

#Tabulates data to excel workbook. 



