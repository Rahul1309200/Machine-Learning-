import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib as mpl

# 1. Create Dummy Data (e.g., Training hours vs. Model Performance)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1) # Features must be 2D
y = np.array([45, 50, 55, 60, 68, 70, 80, 85, 88, 95])      # Target

# 2. Initialize and Train the Model
model = LinearRegression()
model.fit(X, y)

# 3. Make a Prediction
new_input = np.array([[11]]) 
prediction = model.predict(new_input)

# 4. View the "m" and "b"
print(f"Slope (m): {model.coef_[0]}")
print(f"Intercept (b): {model.intercept_}")
print(f"Prediction for 11 hours: {prediction[0]}")