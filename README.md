# Amazon-Product-Cryptocurrency-Tracker
### Background
Many applications allow users to track amazon products for price changes. Similarliy, you can use apps or view websites that track the price changes of every modern cryptocurrency. I am interested in conjoining both functions, tracking both the value of an amazon product in terms of target cryptocurrencies.  
### Goal
Track the price of a given Amazon product in multiple cryptocurrencies. Notifies user when Amazon product AND cryptocurrency pricepoint is below specificed thresholds.  
### Criteria
- Tracks Amazon product's price through webscraping.
- Displays the costs in any cryptocurrency of choice using realtime data from Coinbase API.
- Stores data in .xlsx document.
- Emails users routinely of current price of item in crypto. Emphasizes significant price drops. 
### Method
I used Coinbase API for cryptocurrency ecxchange rates since they provide free, realtime data without any need for API authentication. Data is stored in an excel document for users to easily access and view from any device. The Amazon page is scraped through a Selenium driver. This is because Amazon does not allow simple HTML requests from 3rd-party programs as Amazon strongly encourages users to request data through AWS. This is over-the-top since the goal is to merely request the product's advertized price, nothing more. Therefore, a temporary Chrome driver is created to download the HTML. 

All datapoints are saved in an individual productTracker object, which is then pickled for easy transfer and alteration. 
