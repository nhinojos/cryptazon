# Amazon-Product-Cryptocurrency-Tracker
### Background
There are a plentiful amount of apps to track amazon products for price changes. Similarliy, you can use apps or view websites that track the price changes of every modern cryptocurrency. I am interested in conjoining both fields here, tracking who the value of an amazon product in terms of chosen cryptocurrencies.  
### Goal
Track the price of a given Amazon product in multiple cryptocurrencies. Notifies user when pricepoint is below a specificed threshold.  
### Criteria
- Tracks Amazon product's price through webscraping.
- Displays the costs in any cryptocurrency of choice using realtime data from Coinbase API.
- Stores data in .xlsx document.
- Emails users routinely of current price of item in crypto. Emphasizes significant price drops. 
### Method
I used Coinbase API for cryptocurrency ecxchange rates since they provide free, realtime data without any need for API authentication. Data is stored in an excel document for users to easily access and view from any device, including their cell phone. 