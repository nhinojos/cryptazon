## Necessary Libararies.
import requests # Request real-time crypotcurrency data from Coinbase.
from openpyxl import Workbook # Manipulating Excel Spreadsheet. https://openpyxl.readthedocs.io/en/stable/.
import yagmail # Simplified Gmail Delivery. https://github.com/kootenpv/yagmail.
import pickle # To serialize python objects. https://docs.python.org/3/library/pickle.html
from bs4 import BeautifulSoup # For parsing HTML: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from selenium import webdriver # Temporary driver to load HTML: https://selenium-python.readthedocs.io/
import time # Records date

## Retrieves real-time cryptocurrency data from Coinbase.
def currency_data():
    return requests.get(
            'https://api.coinbase.com/v2/exchange-rates'
            ).json()['data']['rates']


## Return booleans for input equality. 
## Edits inputs beforehand based on inputted condition.
    # 'l'  : Lowercase strings.
    # 's'  : Remove spaces in strings.
    # Strings variables can be combined for multiconditional edits.
        # Example,  'ls' : Lowercase and Remove Spaces. 
## ***** Remove condition if this is only used for email verification.
def string_confirm(prompt,condition):
    valid=False
    while not valid:
        print(prompt)
        string_initial=input()
        print('Please type again to confirm.')
        string_confirm=input()
        if 'l' in condition:
            string_initial.lower()
            string_confirm.lower()
        if 's' in condition:
            string_initial.replace(' ','')
            string_confirm.replace(' ','')
        if string_initial == string_confirm:
            valid=True
        else:
            print('Inputs do not match.')
    return string_initial

## Track products price history, tabulate cryptocurrency data, and email users. 
class ProductTracker:
    # Initialize generates new object properties:
        # self.filename is the user-decided name for file writing.
        # self.link is the hyperlink to the Amazon product.
        # self.cryptocurrencies is the set() of all cryptocurrencies being tracked.
        # self.sender is the email delivering notifications.
        # self.recipient is the email being sent notifcations.
        # self.password is the sender email's password.
    def __init__(
            self, filename=None, link=None,
            cryptocurrencies=None,
            sender=None, recipient=None,
            password=None,):


        ## Asks for a name for file naming.
        while filename is None:
            filename=input(
                    'Please provide a filename, without any file suffix:')
        self.filename=filename
        print('Filename: ',self.filename)
        print('')

        ## Asks and validates product's web location.
        valid=False
        while not valid:
            try:
                requests.get(link)
            except requests.exceptions.MissingSchema:
                if link is not None:
                    print('Dysfuntional link inputted.')
                print("Please paste the link to the Amazon product:")
                link=input()
            else:
                valid=True
        self.link=link
        print('Link: ',link)
        print('')


        ## Determining what cryptocurrencies the user will track.
            # Permits list, str, and None inputs.
        valid=False
        while not valid:
            # Asks for users to input crypotcurrencies if not already done. 
            if cryptocurrencies is None:
                print('Here are the list of trackable cryptocurrencies:')
                crypto_options=''
                # Displays cryptoccurrency keys neatly to user.
                for i,crypto in enumerate(currency_data().keys()):
                    crypto_options+=crypto+(10-len(crypto))*' '
                    if i%16==0:
                        print(crypto_options)
                        crypto_options=''
                print('Please input the abbreviated cryptocurrencies') 
                print('you would like to track, separated by commas:')
                cryptocurrencies=input()
            if type(cryptocurrencies) is str: # Turns string to list.
                cryptocurrencies.upper()
                cryptocurrencies.replace(' ','')
                cryptocurrencies=cryptocurrencies.split(',')
            if type(cryptocurrencies) is list: # Checks availability.
                valid=set(cryptocurrencies).issubset(currency_data().keys())
                if valid==False:
                    print('Inputted cryptocurrencies are not available.')
                    cryptocurrencies=None
        self.cryptocurrencies=cryptocurrencies
        print('Cryptocurrencies: ',cryptocurrencies)
        print('')


        ## Generate new Excel workbook.
            # Includes two sheets, 'Data' and 'Analysis.'
        self.workbook=Workbook() 
        self.workbook.active.title="Data" 
        for i,crypto in enumerate(cryptocurrencies):
            self.workbook["Data"]['A'+str(i+2)]=crypto
        self.workbook.create_sheet("Analysis")
        

        ## Determine's user emails.
        if None in {recipient,sender,password}:
            print("Intializing Email registration.")
            if recipient is None: # Validating recipient email.
                recipient=string_confirm('Please input recipient email:','ls')
            if sender is None:
               sender=string_confirm('Please input sender email:','ls')
            if password is None: # Validating and registering password
                print('No password registered.')
                valid=False
                while not valid:
                    print("Is the sender email already registered?(y/n)")
                    response=input()
                    if response.lower() not in {'y','yes','n','no'}:
                        print('That is not a proper response.')
                    elif response.lower() in {'n','no'}:
                        print("What is the delivering email's password?")
                        # Password will not be saved within object instance.
                        password=string_confirm(
                            "Please enter sender email's password:") 
        # Registration can be skipped if 
        # password is initially marked True.
        if password!=True:
            # Stores username and password in Python's
            # secure storage keyring library.
            yagmail.register(sender,password) 
        self.sender=sender
        print('Sender Email: ', self.sender)
        print('')
        self.recipient=recipient
        print('Recipient Email: ', self.recipient)
        print('')
        return 


    ## Notifies user through email.
    def email_notification(self, title, content):
        date=time.strftime("%d %b %y, %H:%M",time.gmtime())
        title='Amazon-Crypto Tracker: '
        yagmail.SMTP(self.sender).send(self.recipient,title,content)
        return None


    ## Saves object and excel workbook to directory 
    def save_to_directory(self,filetype): 
        #Subject to change since it saves both object and excel data. 
        self.workbook.save(self.filename+'.xlsx')
        pickle.dump(self,open(self.filename+'.pickle','wb'))
        return None
    

    ## Appends price data to excel workbook
    def append_price(self):
        ## Webscrapes price through Selenium Chrome driver. 
        driver=webdriver.Chrome("C:\chromedriver.exe") # LOCATION MUST CHANGE TO WHEREVER YOU STORE YOUR SELENIUM DRIVER
        driver.get(self.link)
        with open("product_page.html", "w",encoding='utf-8') as f:
            f.write(driver.page_source)
        with open("product_page.html", "rb") as f:
            soup=BeautifulSoup(f,'lxml')
        price_usd=soup.find('span',class_='a-offscreen').text.replace('$','')
        
        # Converts price to cryptocurrency
        price_crypto=[]
        for crypto in self.cryptocurrencies:
            price_crypto.append(price_usd*currency_data[crypto])
        # Appends to workbook
        ws_data=self.workbook["Data"]
        for row in ws_data.iter_rows(min_col=1, max_col=1):
            pass

        time=time.strftime("%d %b %y, %H:%M",time.gmtime())
        return None    

        





