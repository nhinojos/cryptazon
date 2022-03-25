# Test object as Bucket Hat from Amazon
from amazoncrypto import ProductTracker


## Testing object with bucket hat product.
bucket_hat_data={"Link":'https://www.amazon.com/VIVICMW-Breathable-Bordered-Outdoor-Fishing/dp/B07PP5X1R2/ref=sr_1_15?crid=BZPV1QMESPUD&keywords=bucket+hat&qid=1646709505&sprefix=bucket+hat%2Caps%2C123&sr=8-15'
            ,"Cryptocurrencies" : ['BTC','ETH']
            ,"Sender":'kitten.in.superposition@gmail.com' # Inputs sender email here. 
            ,"Recipient":'noah.hinojos@gmail.com' # Input recipient email here
                                    }

bucket_hat=ProductTracker('bucket_hat',
                        bucket_hat_data['Link'],
                        bucket_hat_data['Cryptocurrencies'],
                        bucket_hat_data['Sender'],
                        bucket_hat_data['Recipient'])


bucket_hat.update_pickle()