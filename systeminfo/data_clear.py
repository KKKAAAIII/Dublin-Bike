#!/usr/bin/env python
# coding: utf-8

# In[12]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
bike_station = pd.read_csv("./bike_station.csv")
bike_station = bike_station[["number","last_update","available_bikes"]]
time = pd.DatetimeIndex(bike_station["last_update"])
bike_station["day"] = time.day
bike_station["hour"] = time.hour
bike_station["weekday"] = time.weekday
bike_station = bike_station.drop(["last_update"],axis=1)
bike_station.to_csv("./bike.csv")
print(bike_station)


# In[17]:


weather = pd.read_csv("./weather.csv")
time_value = pd.to_datetime(weather["dt"],unit="s")
time_value = pd.DatetimeIndex(time_value)
weather["day"] = time_value.day
weather["hour"] = time_value.hour
weather["weekday"] = time_value.weekday
weather = weather.drop(["dt"],axis=1)
weather.to_csv("./weathers.csv")
print(weather)


# In[ ]:




