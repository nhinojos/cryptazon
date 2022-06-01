import requests
from time import strftime, localtime
import yagmail
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
        driver_path: str = "C:\\chromedriver.exe",
        csv_path: str = None
    ) -> None:
        
        self.product_link = product_link
        self._validate_connection()
        self.email_recipient = email_recipient
        self.email_sender = email_sender
        # Registers password if not so done already.
        if password is not None:
            yagmail.register(email_sender, password)
        self.driver_path = driver_path
        self.filename = filename
        self.thresholds = thresholds
        self._to_id()
        # Assigns empty threshold values to corresponding product price
        # in terms of currency exchange rate.
        update_data = True
        for key,val in zip(self.thresholds.keys(), self.thresholds.values()):
            if val == None:
                if key == "usd":
                    self.thresholds[key] = self.scrape_price()
                    update_data = False
                
                else:
                    self.thresholds[key] = (
                        self.thresholds["usd"] 
                        / self.coins_per_usd(key)
                    )
        
        if csv_path is None:
            self.df = pd.DataFrame(columns=self.thresholds.keys())
            if update_data:
                self.update_df()
        
        else:
            self.df = pd.read_csv(csv_path)
        
        
    @staticmethod
    def present_date(include_time: bool = False) -> str:
        """
        Returns the present date is DD-MM-YYYY Format. May include 
        24-hour time as well, formatted as HH:MM.
        """
        date = strftime("%d-%m-%Y", localtime())
        if include_time:
            date += " " + strftime("%H:%M", localtime())
        return date


    def currency_history(
        id: str, 
        date: str,
        display: bool = False
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


    def scrape_price(self) -> float:
        """
        Scrapes Amazon's productpage for current USD pricepoint.
        """
        driver = webdriver.Chrome(self.driver_path)
        driver.get(self.product_link)
        with open( 
            "data\\" + self.filename + "_page.html", 
            "w", 
            encoding='utf-8'
        ) as f:
            f.write(driver.page_source)
        with open("data\\"+ self.filename + "_page.html","rb") as f:
            soup=BeautifulSoup(f, 'lxml')
        return float(
            soup.find("span", class_="a-offscreen").text.replace("$", "")
        )


    def update_df(self):
        """
        Scrapes for a new pricepoint and adds it to Dataframe.
        """
        price_usd = self.scrape_price()
        new_row = [price_usd]
        for currency in list(self.thresholds.keys()):
            if currency == 'usd':
                continue
            else:
                new_row.append(price_usd * self.coins_per_usd(currency))
        self.df.loc[len(self.df.index)] = new_row
        return
        
        
    def email_notify(self, title, content):
        """
        Delivers email notification to user.
        """
        title = "Amazon-Crypto Tracker:" + self.filename + strftime()
        yagmail.SMTP(self.sender).send(self.recipient, title, content)
        return
    
    
    def coins_per_usd(self, coin_id):
        """
        Current USD exchange rate for specified cryptocurrency. 
        """
        return 1 / requests.get(
            "https://api.coingecko.com/api/v3/coins/" + coin_id
        ).json()["market_data"]["current_price"]["usd"]
    
    
    def _to_id(self) -> None:
        """
        Standardizes every currency key to CoingGecko's ID Format. 
        """
        coingecko_options = requests.get(
            "https://api.coingecko.com/api/v3/coins/list"
        ).json()
        
        for term_old in self.thresholds.keys():
            if term_old == "usd":
                continue
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
                    "'" + term_old + "' not found in CoinGecko's API."
                    " Please ensure '" + term_old + "' is spelled correctly" 
                )
    
        self.thresholds.update({term_new: self.thresholds.pop(term_old)})
        return       
         
         
    def _validate_connection(self):
        """
        Ensures network connection is valid.
        """    
        try:
            requests.get(
                "https://api.coingecko.com/api/v3/ping"
            ).json()
        except ConnectionError:
            raise ConnectionError("CoinGecko API not accessible.")
