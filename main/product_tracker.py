import requests
from time import strftime, localtime
import yagmail
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


class ProductTracker:
    """
    Tracks products price history, notifies of changes.
    """
    def __init__(
        self,
        product_link: str,
        email_recipient: str,
        email_sender: str,
        password: str = None,
        thresholds: dict = None,
        filename: str = 'product',
        driver_loc: str = "C:\\chromedriver.exe",
        csv_loc: str = None
    ) -> None:
        
        self.product_link = product_link
        self._validate_connection()
        self.email_recipient = email_recipient
        self.email_sender = email_sender
        
        # Registers password if not so done already.
        if password is not None:
            yagmail.register(email_sender, password)
        
        self.driver_loc = driver_loc
        self.filename = filename
        self.tresholds = thresholds
        self._to_id()
        
        # Assigns empty threshold values to corresponding product price
        # in terms of currency exchange rate.
        for key,val in zip(self.thresholds.keys(), self.tresholds.values()):
            if val == None:
                self.tresholds[key] = self.exchange_rate_usd(key)
        
        if csv_loc is None:
            self.df = pd.DataFrame(columns=['USD',*self.thresholds.keys()])
            self.update_df()
        else:
            self.df = pd.read_csv(csv_loc)
        
    @staticmethod
    def present_date(include_time: bool = False) -> str:
        date = strftime("%d-%m-%Y", localtime())
        if include_time:
            date += " " + strftime("%H:%M", localtime())
        return date


    def currency_history(
        id: str, date: str, display: bool = False
    ) -> dict:
        """
        API call for historical cryptocurrency rates.
        """
        
        data = requests.get(
            "https://api.coingecko.com/api/v3/coins/" 
            + id 
            + "/history" 
            + date
        ).json()['market_data']['current_price']
        if display:
            print('Trackable cryptocurrencies:')
            for i in list(data.keys()):
                print(i)
        return data


    def scrape_price(
        link: str, driver_loc: str, filename: str = 'product'
    ) -> float:
        """
        Scrapes Amazon's productpage for current USD pricepoint.
        """
        
        driver = webdriver.Chrome(driver_loc)
        driver.get(link)
        with open( "data\\"+ filename + "_page.html", "w", encoding='utf-8') as f:
            f.write(driver.page_source)
        with open("data\\"+ filename + "_page.html","rb") as f:
            soup=BeautifulSoup(f, 'lxml')
        return float(
            soup.find("span", class_="a-offscreen").text.replace("$", "")
        )


    def update_df(self):
        """
        Scrapes for a new pricepoint and adds it to Dataframe.
        """
        usd_price = self.scrape_price()
        pd.df[self.present_date()] = [
            usd_price,
            *[usd_price ]
            ]
        return
        
    def email_notify(self, title, content):
        """
        Notifies user through email.
        """
        title = "Amazon-Crypto Tracker:" + self.filename + strftime()
        yagmail.SMTP(self.sender).send(self.recipient, title, content)
        return
    
    
    def exchange_rate_usd(self, coin_id):
        return self.scrape_price(
            self.product_link, 
            self.driver_loc,
            self.filename
        ) / requests.get(
            "https://api.coingecko.com/api/v3/coins/" + coin_id
        ).json()["market_data"]["current_price"]["usd"]
    
    def _to_id(self) -> None:
        """
        Standardizes every currency key to CoingGecko's ID Format. 
        """
        coingecko_options = requests.get(
            "https://api.coingecko.com/api/v3/indexes"
        ).json()
        
        # 
        for term_old in self.thresholds.keys():
            if type(term_old) != str:
                raise TypeError(str(term_old) + "must be type str")
                
            found = False
            for option in coingecko_options:
                if term_old in list(option.values())[:3]:
                    term_new = option['id']
                    found = True
                    break
            if not found:        
                raise NameError(
                    term_old + "not found for CoinGecko's API"
                    "Please ensure" + term_old + "is spelled correctly" 
                )
    
        self.tresholds.update(term_new, self.tresholds.pop(term_old))
        return       
         
         
    def _validate_connection(self):
        """
        Ensures network connection is valid.
        """    
        try:
            requests.get(self.product_link)
        except ConnectionError:
            raise ConnectionError( "Product page not accessible.")
        
        try:
            requests.get(
                "https://api.coingecko.com/api/v3/ping"
            ).json()
        except ConnectionError:
            raise ConnectionError("CoinGecko API not accessible.")
        

    

    

        
    



    

