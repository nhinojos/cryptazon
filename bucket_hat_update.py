import pickle
# 
with open("bucket_hat.pickle","r+b") as f:
    bucket_hat=pickle.load(f)
    f.close()
 
# Updates a new row three times. 
for i in range(1):
    print("Commencing Iteration:",i+1)
    bucket_hat.update_data()
bucket_hat.update_pickle()
