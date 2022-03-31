from sklearn.model_selection import train_test_split,GridSearchCV
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import joblib
bike_station = pd.read_csv("./machine_learning_dataset.csv")
print(bike_station)
x = bike_station[["number","hour","weekday","temp","humidity"]]
y = bike_station["available_bikes"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25)
td = DecisionTreeClassifier()
td.fit(x_train,y_train)
y_predict = td.predict(x_test)
print(td.score(x_test,y_test))
joblib.dump(td,"./bikestation_forecast_model.pkl")
