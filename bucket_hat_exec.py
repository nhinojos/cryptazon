# Run this file to update the worksheet
import pickle
import time

# Opens test bucket_hat object. 
with open("data\\bucket_hat.pickle","r+b") as f:
    bucket_hat = pickle.load(f)
    f.close()
 
# Updates a new row three times. 
for i in range(1):
    print("Commencing Iteration:",i + 1)
    bucket_hat.update_xl()
bucket_hat.save_pickle()
