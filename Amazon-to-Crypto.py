## Necessary Libararies.
import requests # Request real-time crypotcurrency data from Coinbase
from openpyxl import Workbook # Manipulating Excel Spreadsheet. Documentation: https://openpyxl.readthedocs.io/en/stable/
import yagmail #Simplified Gmail Delivery. Documentation: https://github.com/kootenpv/yagmail
import pickle #For saving python objects

#Primary object to track product, tabulate cryptocurrency data, and email users
class productTracker:
    #Initialize generates new object properties:
        # self.link is the hyperlink to the Amazon product.
        # self.crypto_target is the set of all cryptocurrencies being tracked
            # This may be removed since the cryptocurrencies will also be stored in the workbook itself
        # self.workbook is the excel workbook where price data is stored and analyzed
        # self.sender is the email delivering notifications
        # self.recipient is the email being sent notifcations
    def __init__(self):
        # Asks and validates product's web location 
        valid=False
        while not valid:
            self.link=input('Please paste the link to the Amazon product you would like to track.')
            try:
                requests.get(self.link)
            except:
                print('Link not valid.')
            else:
                valid=True
        
        ## Determining what cryptocurrencies the user will track.
        # Displaying cryptocurrency options
        crypto_string=''
        print('Here are the list of cryptocurrencies available to track:')
        for i,crypto in enumerate(currencyData().keys()):
            crypto_string+=crypto+(10-len(crypto))*' '
            if i%16==0:
                print(crypto_string)
                crypto_string=''
    
        # Asks and validates user inputted cryptocurrenncies
        print('Please type the abbreviated cryptocurrencies you would like to track, separated by commas:')
        valid=False
        while not valid:
            self.crypto_target=input()
            if len(self.crypto_target)==0:
                continue
            
            #Conversts string to list to set
            self.crypto_target.upper()
            self.crypto_target.replace(' ','')
            self.crypto_target=set(self.crypto_target.split(','))
            valid=self.crypto_target.issubset(currencyData().keys())
            if not valid:
                print('Error, inputted currencies are either not available.')
                print('Please makes sure you only input abbreviated cryptocurrencies, separated by commas:')
            
            else:
                valid=True


        ## Generate new Excel workbook.
            # Includes two sheets, 'Data' and 'Analysis.'
            # 'Data' contains two columns labeled 'Currency' and 'Date.'
                # 'Date' will encompass all further columns from B onward. 
            # Appends target cryptocurrencies under 'Currency' column.
        self.workbook=Workbook() 
        workbook_data=self.workbook.active
        workbook_data.title = "Data" 
        workbook_data['A1']="Currency" 
        workbook_data['B1']="Date" 
        for i,crypto in enumerate(self.crypto_target):
            workbook_data['A'+str(i+2)]=crypto
        self.workbook.create_sheet("Analysis")
        self.workbook.save('product_history.xlsx')

        #Registrating user emails.
        self.recipient=input('What email would you like to be nofitied?')
        self.sender=input('What email are you using to deliver notifications?')
        password=input("What is the delivering emails' password?" ) # Password will not be saved in object instance.
        yagmail.register(self.sender,password) # Stores username and password in Python's secure storage keyring library.
        return

    # Notifies user through email
    def emailNotification(self, title, content):
        yagmail.SMTP(self.sender).send(self.recipient,title,content)
        return

    # Returns JSON of current cryptocurrency data from Coinbase
    def currencyData():
        return requests.get('https://api.coinbase.com/v2/exchange-rates').json()['data']['rates']

