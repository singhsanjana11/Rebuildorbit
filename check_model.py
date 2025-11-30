import pickle

obj = pickle.load(open("churn_model.pkl", "rb"))
print("TYPE =", type(obj))
print("CONTENT =", obj)
