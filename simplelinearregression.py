import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
df = pd.read_csv("Placement.csv")
print(df.head())

X=df.iloc[:,1:2]
Y=df.iloc[:, -1]
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)

lr=LinearRegression()
lr.fit(X_train,Y_train)
print(X_test)
print(Y_test)
Y_pred = lr.predict(X_test.iloc[1].values.reshape(1,1))
print(Y_pred)
