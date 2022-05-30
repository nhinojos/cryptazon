import requests
from time import strftime, localtime
import yagmail
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Present data & time.
time_present = strftime("%d-%b-%Y %H:%m", localtime())

# Retrieves real-time cryptocurrency data from Coinbase.
def currency_data(display=False):
    # API call for a dictionary of rates.
    data = requests.get(
        'https://api.coinbase.com/v2/exchange-rates'
    ).json()['data']['rates']

    # Prints cryptocurrency options to console.
    if display:
        print('Trackable cryptocurrencies:')
        print(i for i in list(data.keys()))

    return data

# Webscrapes price of Amazon product.


def scrape_price(link, driver_location, filename='product'):
    # Initiates Selenium Chrome driver.
    driver = webdriver.Chrome(driver_location)
    driver.get(link)

    # Retrieves price from HTML.
    with open("data\\"
              + filename
              + "_page.html",
              "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    with open("data\\"
              + filename
              + "_page.html",
              "rb") as f:
        soup = BeautifulSoup(f, 'lxml')
    price_usd = soup.find('span',
                          class_='a-offscreen').text.replace('$', '')

    return float(price_usd)


# Tracks products price history, notifies of changes.
class ProductTracker:
    def __init__(
            self,
            link,
            currencies: "list",
            email_recipient,
            email_sender,
            password=None,
            cryptothresh: "dict" = None,
            dataframe=None,
            filename='product',
            driver_loc="C:\\chromedriver.exe"):

        # Establishing required variables to self.
        self.filename = filename
        self.link = link
        self.email_sender = email_sender
        self.email_recipient = email_recipient
        self.driver_loc = driver_loc

        # Defaulted cryoptothresh is priciepoint exchange rates.
        if cryptothresh is None:
            price = scrape_price(self.link, 
                                 self.driver_loc,
                                 self.filename)
            self.cryptothresh = dict(zip(['USD',*currencies], 
                                  [price, 
                                   *[price * currency_data()[i]
                                     for i in currencies]]))
        else:
            self.cryptothresh = cryptothresh
        
        # Defaulted dataframe only contains thresholds.    
        if dataframe is None:
            self.df = pd.DataFrame(index=["Threshold"],
                                   columns=['USD',
                                            *currencies])
        else:
            self.df = dataframe
            # Ensures dataframe incorporates all provided cryptothresholds.
            for i in list(set().union(self.df.columns,
                                      cryptothresh.keys())):
                self.df[i] = None



        # Registers delivering email and password.
        if password is not None:
            yagmail.register(email_sender, password)

        return

    # Updates dataframe to include present value of .
    def update_df(self):
        pass

    # Notifies user through email.
    def email_notify(self, title, content):
        title = "Amazon-Crypto Tracker:" + self.filename + time_present
        yagmail.SMTP(self.sender).send(self.recipient, title, content)
        return
