## Necessary Libararies.
import requests # Request real-time crypotcurrency data from Coinbase.
from openpyxl import Workbook # Manipulating Excel Spreadsheet. https://openpyxl.readthedocs.io/en/stable/.
import yagmail # Simplified Gmail Delivery. https://github.com/kootenpv/yagmail.
import pickle # To serialize python objects. https://docs.python.org/3/library/pickle.html
from bs4 import BeautifulSoup # For parsing HTML: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from selenium import webdriver # Temporary driver to load HTML: https://selenium-python.readthedocs.io/
import time # Records date

## Retrieves real-time cryptocurrency data from Coinbase.
    # If display _types is True, then the currency 
    # types available will be displayed in the console. 
def currency_data(display_types=False):
    # Coinbase API call.
    data=requests.get(
            'https://api.coinbase.com/v2/exchange-rates'
            ).json()['data']['rates']
    # Displays cryptoccurrency keys neatly to user.
    if display_types:
        print('Here is a list of trackable cryptocurrencies:')
        crypto_options=''
        for i,crypto in enumerate(data.keys()):
            crypto_options+=crypto+(10-len(crypto))*' '
            if i%16==0:
                print(crypto_options)
                crypto_options=''
        return None
    else:
        return data

## Return booleans for input equality. 
## Edits inputs beforehand based on inputted condition.
    # 'l'  : Lowercase strings.
    # 's'  : Remove spaces in strings.
    # Strings variables can be combined for multiconditional edits.
        # Example,  'ls' : Lowercase and Remove Spaces. 
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
        # self.cryptocurrencies is the list of all target cryptos. 
        # self.sender is the email delivering notifications.
        # self.recipient is the email being sent notifcations.
        # self.password is the sender email's password.
    def __init__(
            self, filename=None, link=None,
            cryptocurrencies=None, threshold=None,
            sender=None, recipient=None,
            password=None,):


        ## Asks for a name for file naming.
        while filename is None:
            filename=input('Please provide a filename, without any file suffix:')
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
                currency_data(display_types=True)
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
        workbook=Workbook() 
        workbook.active.title="Data" 
        ws_data=workbook["Data"]
        ws_data['B1'].value='USD'
        # Appends cryptocurrency choices to workbook
        i=0
        for col in ws_data.iter_cols(min_row=1,max_row=1,min_col=3,
                                    max_col=2+len(self.cryptocurrencies)):
            for cell in col:
                cell.value=self.cryptocurrencies[i]
                i+=1
        ws_data['A2']="Threshold"
        if threshold=None:
            threshold=
        workbook.create_sheet("Analysis")
        self.workbook=workbook

        ## Establishes user emails.
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
        date=time.strftime("%d %b %y, %H:%M%p",time.localtime())
        title="Amazon-Crypto Tracker:"+self.filename+date
        yagmail.SMTP(self.sender).send(self.recipient,title,content)
        return None

    # Establishes threshold. 
    def set_threshold(self):
        return


    ## Saves excel workbook to directory. 
    def save_workbook(self): 
        self.workbook.save(self.filename+'.xlsx')
        return
    
    ## Saves pickeled object to directory. 
    def save_object(self):
        pickle.dump(self,open(self.filename+'.pickle','wb'))
        return

    ## Appends price data to excel workbook
    def get_price(self,in_usd=True):
        ## Webscrapes price through Selenium Chrome driver. 
        driver=webdriver.Chrome("C:\chromedriver.exe") # LOCATION MUST CHANGE TO WHEREVER YOU STORE YOUR SELENIUM DRIVER
        driver.get(self.link)
        
        with open("product_page.html", "w",encoding='utf-8') as f:
            f.write(driver.page_source)
        with open("product_page.html", "rb") as f:
            soup=BeautifulSoup(f,'lxml')
        price_usd =soup.find('span',class_='a-offscreen').text.replace('$','')
        
        #Reutrns in terms of USD
        if in_usd==True:
            return price_usd
        # Returns in terms of self.crypticurrencies
        else:
            # Converts price to cryptocurrency
            price_crypto=[]
            for crypto in self.cryptocurrencies:
                price_crypto.append(price_usd*currency_data[crypto])
            return price_crypto
            

        
        
        
    #Adds prices to workbook
    def update_workbook(self,prices):
        ws_data=self.workbook["Data"]
        # Date in left-most cell
        ws_data['A'+str(ws_data.max_row+1)]=time.strftime("%d %b %y, %H:%M%p",time.localtime())
        # Then, usd price
        ws_data['B'+str(ws_data.max_row)]=self.get_price()
        # Finally, crypto prices
        i=0
        for col in ws_data.iter_rows(min_row=ws_data.max_row,
                                    max_row=ws_data.max_row,
                                    min_col=3, max_col=2+len(self.cryptocurrencies)):
            
            for cell in col:
                cell.value=prices[i]
                i+=1

        return None    

        






