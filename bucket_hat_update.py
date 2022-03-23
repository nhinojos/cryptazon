import pickle

bucket_hat=pickle.load(open("bucket_hat.pickle","rb"))
print('Success!')
bucket_hat.update_data()