import requests
from time import strftime, localtime
import yagmail
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

"""
Library of all necessary classes and functions.
"""
def currency_data(time, units='days', display=False):
    """
    API call for historical crypto rates.
    
    'time' may be in units of 
    """
    data = requests.get(
        "https://api.coingecko.com/api/v3/coins/"
        + id
        + "/history"
    ).json()['data']['rates']


    if display:
        print('Trackable cryptocurrencies:')
        print(i for i in list(data.keys()))

    return data

def scrape_price(
    link: str, 
    driver_location: str, 
    filename: str = 'product'
) -> float:
    """
    Scrapes Amazon website product's current USD pricepoint.
    """
    
    driver = webdriver.Chrome(driver_location)
    driver.get(link)

    with open(
        "data\\"
        + filename
        + "_page.html",
        "w", encoding='utf-8'
    ) as f:
        f.write(driver.page_source)
    with open(
        "data\\"
        + filename
        + "_page.html",
        "rb"
    ) as f:
        soup=BeautifulSoup(f, 'lxml')
    price_usd=soup.find(
                        'span',
                        class_='a-offscreen'
                ).text.replace('$', '')
    return float(price_usd)

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
        dataframe: pd.DataFrame = None,
        name: str = 'product',
        driver_loc: str = "C:\\chromedriver.exe"
    ) -> None:
        
        
        self.product_link = product_link
        self.validate_connection()
        self.to_id()

    def to_id(self, currencies: list = None):
        """
        Ensures every currency in list is abbreviated to CoingGecko's 
        ID Format.
        
        Defaults to list of self if no other cryptocurrency list is 
        provided; self will change accordingly. 
        """
        
        if currencies is None:
            edit_self = True
            currencies = self.thresholds.keys()
        
        coingecko_options = requests.get(
            "https://api.coingecko.com/api/v3/indexes"
        ).json()
        
        for option in coingecko_options:
            for type_ in ["name", "market"]:
                for i, crypto in enumerate(currencies):
                    if crypto == option[type_]:
                        currencies[i] = option["id"] 
        
        if not edit_self:
            return currencies
        
        for name_new, name_prior in (
            currencies, 
            list(self.thresholds.keys()
            )
        ):
            if name_new != name_prior:
                self.thresholds.update({
                    name_new:
                    self.thresholds.pop(name_prior)
                }
                )
        return None   
         
    def validate_connection(self, link_product: str = None):
        """
        Ensures network connection is valid.
        """    
        try:
            if link_product is None:
                link_product = self.product_link
            requests.get(link_product)
        except:
            raise ConnectionError( "Product page not accessible.")
        
        try:
            options = requests.get(
            "https://api.coingecko.com/api/v3/ping"
            ).json()
        except:
                raise ConnectionError("CoinGecko API not accessible.")
        
    
    


        # Defaulted cryoptothresh is priciepoint exchange rates.
        if cryptothresh is None:
            price = scrape_price(
                self.product_link, 
                self.driver_loc,
                self.filename
            )
            self.cryptothresh = dict(
                                    zip(
                                        ['USD',*currencies], 
                                        [
                                            price, 
                                            *[price *currency_data()[i]
                                                for i in currencies
                                            ]
                                        ]
                                    )
            )
        else:
            self.cryptothresh = cryptothresh
        
        # Defaulted dataframe only contains thresholds.    
        if dataframe is None:
            self.df = pd.DataFrame(
                index=["Threshold"],
                columns=['USD',
                         *currencies
                ]
            )
        else:
            self.df = dataframe
            # Ensures dataframe incorporates all provided cryptothresholds.
            for i in list(
                set().union(
                    self.df.columns,
                    cryptothresh.keys()
                )
            ):
                self.df[i] = None
        # Registers delivering email and password.
        if password is not None:
            yagmail.register(email_sender, password)
        
    def update_df(self):
        """
        Appendss new row using present-value data.
        """
        pass
    
    def email_notify(self, title, content):
        """
        Notifies user through email.
        """
        title = "Amazon-Crypto Tracker:" + self.filename + time_present
        yagmail.SMTP(self.sender).send(self.recipient, title, content)
        return
    

        
    



    

