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


## Track products price history, tabulate cryptocurrency data, and email users. 
class ProductTracker:
    # Initialize generates new object properties:
        # self.filename is the user-decided name for file writing.
        # self.link is the hyperlink to the Amazon product.
        # self.cryptocurrencies is the list of all target cryptos. 
        # self.sender is the email delivering notifications.
        # self.recipient is the email being sent notifcations.
        # self.password is the sender email's password.
        # self.driver_location is the file location of your chrome driver. 
            # The default is the C:\ drive. 
    def __init__(
            self, filename, link, cryptocurrencies,
            email_recipient, email_sender,  
            threshold=None, password=None,
            driver_location="C:\chromedriver.exe"):

        self.filename=filename
        self.link=link
        self.cryptocurrencies=cryptocurrencies
        self.email_sender=email_sender
        self.email_recipient=email_recipient
        self.driver_location=driver_location

        ## Generate new Excel workbook.
        # Creates two new sheets: "Data" and "Analysis"
        workbook=Workbook() 
        workbook.active.title="Data"
        workbook.create_sheet("Analysis") 
        ws_data=workbook["Data"]
        # Appends currency types in column headers
        ws_data['B1'].value='USD'
        i=0
        for col in ws_data.iter_cols(min_row=1,max_row=1,min_col=3,
                                    max_col=2+len(self.cryptocurrencies)):
            for cell in col:
                cell.value=self.cryptocurrencies[i]
                i+=1
        # Appends threshold rates under column headers
        ws_data['A2']="Threshold"
        if threshold==None:
            threshold=self.get_price()
        self.threshold=float(threshold)
        ws_data['B2']=threshold
        crypto_rates=[]
        for crypto in cryptocurrencies:
            crypto_rates.append(float(currency_data()[crypto])*self.threshold)
        
        for row in ws_data.iter_rows(min_row=2,max_row=2,min_col=3,
                                    max_col=2+len(cryptocurrencies)):
            for i,cell in enumerate(row):
                cell.value=crypto_rates[i]
            
        self.workbook=workbook

        ## Registers delivering email and password,
        ## if not done so already.
        if password!=None:
            yagmail.register(email_sender,password)
        
        return 


    ## Delivers email notification to user.
    def email_notification(self, title, content):
        date=time.strftime("%d %b %y, %H:%M%p",time.localtime())
        title="Amazon-Crypto Tracker:"+self.filename+date
        yagmail.SMTP(self.sender).send(self.recipient,title,content)
        return None

    # Edits threshold for notification. 
    def new_threshold(self,threshold):
        self.threshold=threshold
        return

    ## Saves excel workbook to directory. 
        # May be combined with below function save_object. 
    def save_workbook(self): 
        self.workbook.save(self.filename+'.xlsx')
        return
    
    ## Saves pickeled object to directory. 
    def save_object(self):
        pickle.dump(self,open(self.filename+'.pickle','wb'))
        return

    ## Retrieves price through webscraping.
    def get_price(self,in_usd=True):
        # Executes Selenium Chrome driver. 
        driver=webdriver.Chrome(self.driver_location) 
        driver.get(self.link)
        # Writes entire HTML to a document
        with open("product_page.html", "w",encoding='utf-8') as f:
            f.write(driver.page_source)
        # Retrieves price from HTML document. 
        with open("product_page.html", "rb") as f:
            soup=BeautifulSoup(f,'lxml')
        price_usd=soup.find('span',class_='a-offscreen').text.replace('$','')
        return float(price_usd)
            

    # Adds prices to workbook
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

        






