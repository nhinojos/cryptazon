## Necessary Libararies.
import requests # Request real-time crypotcurrency data from Coinbase.
from openpyxl import Workbook # Manipulating Excel Spreadsheet. Documentation: https://openpyxl.readthedocs.io/en/stable/.
import yagmail #Simplified Gmail Delivery. Documentation: https://github.com/kootenpv/yagmail.
import pickle # For saving python objects.


## Track products price history, tabulate cryptocurrency data, and email users. 
class productTracker:
    # Initialize generates new object properties:
        # self.link is the hyperlink to the Amazon product.
        # self.crypto_target is the set() of all cryptocurrencies being tracked.
        # self.workbook is the excel workbook where price data is stored and analyzed.
        # self.sender is the email delivering notifications.
        # self.recipient is the email being sent notifcations.
    def __init__(self,link=None, crypto_target=None,sender=None,recipient=None,password_registered=False,password=None):
        ## Asks and validates product's web location 
        self.link=link
        while True:
            try:
                requests.get(self.link)
            except:
                print('Link not valid.')
            else:
                break
            
            print("Please paste the link to the Amazon product you would like to track:")
            self.link=input()
            for i in range(3):
                print("")



        ## Determining what cryptocurrencies the user will track.
        # Asks and validates inputted cryptocurrenncies.
        self.crypto_target=crypto_target
        while True:
            #Conversts string to list to set.
            if self.crypto_target!=None:
                if type(self.crypto_target)==str: # Turns string to set.
                    self.crypto_target.upper()
                    self.crypto_target.replace(' ','')
                    self.crypto_target=set(self.crypto_target.split(','))
                
                if type(self.crypto_target)==set: # Is this set valid?
                    if self.crypto_target.issubset(self.currencyData().keys()):
                        break
    
                print('Error, inputted currency types are not available.')
            
            else:
                # Displaying cryptocurrency options.
                print('Here are the list of cryptocurrencies available to track:')
                crypto_options=''
                for i,crypto in enumerate(self.currencyData().keys()):
                    crypto_options+=crypto+(10-len(crypto))*' '
                    if i%16==0:
                        print(crypto_options)
                        crypto_options=''
            
            print('Please input the abbreviated cryptocurrencies you would like to track, separated by commas:')
            self.crypto_target=input()
            for i in range(3):
                print("")


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
        

        ## Registrating user emails.
        if None in [sender,recipient] or password_registered==False:
            print("Intializing Email registration.")
            print("If you would like to restart this process, type 'restart' into the command line.")
        
        while True:
            if recipient==None: # Validating recipient email.
                print('What email would you like to be nofitied?')
                self.recipient=input()
                self.recipient.replace(' ','')
                if self.recipient=='restart':
                    recipient=None
                    continue
            
            if sender==None: # Validating sender email.
                print("What email are you using to deliver notifications?")
                self.sender=input()
                self.sender.replace(' ','')
                if self.sender=='restart':
                    sender=None
                    continue

            if password_registered==False: #Validating and regisering password.
                if password==None:
                    print("What is the delivering emails' password?")
                    password=input() # Password will not be saved in object instance.
                    if password=='restart':
                        continue
                
                yagmail.register(self.sender,password) # Stores username and password in Python's secure storage keyring library.
            
            break
        
        return


    ## Notifies user through email.
    def emailNotification(self, title, content):
        yagmail.SMTP(self.sender).send(self.recipient,title,content)
        return


    ## Returns JSON of real-time cryptocurrency data from Coinbase.
    def currencyData(self):
        return requests.get('https://api.coinbase.com/v2/exchange-rates').json()['data']['rates']


    ## Saves workbook document to directory as Excel document. 
    def saveToDirectory(self,object_name='product_tracker'):
        self.workbook.save(object_name+'.xlsx')
        pickle.dump(self,open(object_name+'.pickle','wb'))
        return
    


converse_shoes={"Link":'https://www.amazon.com/Converse-Chuck-Taylor-Women-Black/dp/B07DXHF5RG/?_encoding=UTF8&pd_rd_w=BD1NM&pf_rd_p=067e8e18-34c5-4e6e-8c6c-a4d937ff3226&pf_rd_r=S68JT9VAS1J7V44QMCK0&pd_rd_r=f6bfb1dd-37af-4119-9ca4-6c98d4f35d65&pd_rd_wg=BzfRp&ref_=pd_gw_ci_mcx_mi'
                ,"Cryptocurrencies" : {'BTC','ETH'}
                ,"Sender":'kitten.in.superposition@gmail.com'
                ,"Recipient":'noah.hinojos@gmail.com'
                                    }

converseShoes=productTracker(converse_shoes['Link'],
                            converse_shoes['Cryptocurrencies'],
                            converse_shoes['Sender'],
                            converse_shoes['Recipient'],
                            True)
converseShoes.saveToDirectory()
