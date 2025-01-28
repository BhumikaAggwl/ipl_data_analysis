# -*- coding: utf-8 -*-
"""cfa_data_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11_qMMtapOUY6p6Sb380r8gtCEydzcZnn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

file_path = '/content/final_dataset.csv'
df = pd.read_csv(file_path)

"""Cleaning data

"""

#dropping the irrelvant column
df_cleaned = df.drop(columns=['Unnamed: 0'])

df_cleaned['Winning bid']=pd.to_numeric(df_cleaned['Winning bid'], errors='coerce')   #convert to numeric

# Removing rows with missing 'Winning bid'
df_cleaned = df_cleaned.dropna(subset=['Winning bid'])

df.head()

"""Performing EDA

"""

# Step 2: Performing Exploratory Data Analysis (EDA)
# Graphing the distribution of Base price and Winning bid
plt.figure(figsize=(12, 5))
sns.histplot(df_cleaned['Base price'], kde=True, bins=30, color='blue', label='Base Price')
sns.histplot(df_cleaned['Winning bid'], kde=True, bins=30, color='orange', label='Winning Bid')
plt.legend()
plt.title("Distribution of Base Price and Winning Bid")
plt.show()

team_bids=df_cleaned.groupby('Team')['Winning bid'].sum().sort_values(ascending=False).head(10)

team_bids.plot(kind='bar', color='green', title='Top 10 Teams by Winning Bids')
plt.show()

"""FEATURE ENGINEERING

"""

#encodeing the categorical coulumn
#like country,player ,team
label_encoder={}
for col in ['Country','Player','Team']:
  le =LabelEncoder()
  df_cleaned[col]=le.fit_transform(df_cleaned[col])
  label_encoder[col]=le

#applying basic regression model
#to predict "winning bid" on other feautres
X=df_cleaned[['Country','Player','Team','Base price','Year']]
y=df_cleaned['Winning bid']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training  a Random Forest Regressor
regressor = RandomForestRegressor(random_state=42, n_estimators=100)
regressor.fit(X_train, y_train)

#evaluation of the model
y_pred = regressor.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"Regression Model Performance:")
print(f"RMSE: {rmse}")
print(f"R² Score: {r2}")

# Feature importance
feature_importance = pd.Series(regressor.feature_importances_, index=X.columns)
feature_importance.plot(kind='bar', title='Feature Importance')
plt.show()

# Step 5: Machine Learning - Classification (Optional)
# Create a binary target: High vs. Low bid (threshold: median)
df_cleaned['High Bid'] = (df_cleaned['Winning bid'] > df_cleaned['Winning bid'].median()).astype(int)
X = df_cleaned[['Country', 'Player', 'Team', 'Base price', 'Year']]
y = df_cleaned['High Bid']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#training a random forest classiefier to generate accuraxy score etc
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

classifier = RandomForestClassifier(random_state=45, n_estimators=1000)
classifier.fit(X_train, y_train)



#evaluate the classfieri
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Classification Model Performance:")
print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_report(y_test, y_pred))