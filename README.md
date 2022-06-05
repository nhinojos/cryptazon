# Amazon-Product-Cryptocurrency-Tracker
### Background
Many applications allow users to track amazon products for price changes. Similarliy, you can use apps or view websites that track the price changes of every modern cryptocurrency. I am interested in conjoining both functions, tracking both the value of an amazon product in terms of target cryptocurrencies.  
### Goal
Track the price of a given Amazon product in multiple cryptocurrencies.
### Criteria
- Tracks Amazon product's price through webscraping.
- Tracks specified cryptocurrency highs and lows.
- Stores data in pandas Dataframe object.
- Also, no tokenization. 
### Method
Of all cryptocurrrency API's, CoinGecko seemed best-fitted to for the job. The API requires no sign-up token, and, any currency's price history can be called over any timesspan. 

Selenium chrome dirvers are used for webscraping. Just ensure [the the proper path to the chromedriver executable is setup before usage. 

Originally, this program was supposed to also email users when prices as low. Early-on this was setup using Yagmail which, at the time, was supposed to simplify SMTP for apprentice-level programmers like myself. However, Google's ToS recently changed making this issue extensively more complicated. Therefore this email-nofitifcation funcitonality has been discontinued. 

### Results
This program is constructed as a Python object that both a) Stores all relevant information, such as the Amazon product link, focal cryptocurrencies, etc. b) Can scrape the product pricepoint, retreive currency history, save infomation in pandas dataframe. 