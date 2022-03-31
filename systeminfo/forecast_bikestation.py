from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
import joblib
from pymysql import connect
import time
def bikestation_model(data):
    td = joblib.load("./bikestation_forecast_model.pkl")
    t = pd.DatetimeIndex(data["dt"])
    data["hour"] = t.hour
    data["weekday"] = t.weekday
    x_test = data[["number","hour","weekday","temp","humidity"]]
    print(x_test)
    y_train = data["available_bikes"]
    print(y_train)
    y_predict = td.predict(x_test)
    # std_x = StandardScaler()
    # x_test = std_x.fit_transform(x_test)
    # std_y = StandardScaler()
    # y_train = std_y.fit_transform(y_train.values.reshape((len(y_train),1)))
    # y_predict= std_y.inverse_transform(sgd.predict(x_test))
    print(y_predict)
    return y_predict
def bikestation_data_catch():
    now = int(time.time())
    print(now)
    li = list()
    li_1 = list()
    catch_list = [now - i for i in range(0,18001,3600)]
    print(catch_list)
    conn = connect(host="database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com", port=3306, user="admin", password="a123456789", database="project",charset="utf8")
    cs = conn.cursor()
    for i in range(0,5):
        for j in range(2,118):
            value = ""
            value = "select available_bikes from bikestation where number="
            value += str(j)
            value += " and last_update<"
            value += str(catch_list[i])
            value += "000"
            value += " and last_update>"
            value += str(catch_list[i+1])
            value += "000"
            value += ";"
            print(value)
            cs.execute(value)
            data = cs.fetchone()
            if data is None :
                data = 15
            else:
                data = data[0]
            print(data)
            li.append(data)
    print(li_1)
    for i in range(0,5):
        for j in range(2,118):
            value = ""
            value = "select number from bikestation where number="
            value += str(j)
            value += " and last_update<"
            value += str(catch_list[i])
            value += "000"
            value += " and last_update>"
            value += str(catch_list[i+1])
            value += "000"
            value += ";"
            print(value)
            cs.execute(value)
            data = cs.fetchone()
            if data is None :
                data = 0
            else:
                data = data[0]
            print(data)
            li_1.append(data)
    print(li_1)
    cs.close()
    conn.close()
    return li,li_1
def weather_data_catch():
    now = int(time.time())
    print(now)
    wi = list()
    wi_1 = list()
    wi_2 = list()
    catch_list = [now - i for i in range(0,18001,3600)]
    print(catch_list)
    conn = connect(host="database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com", port=3306, user="admin", password="a123456789", database="project",charset="utf8")
    cs = conn.cursor()
    for i in range(0,5):
        value = ""
        value = "select temp from weather where dt<"
        value += str(catch_list[i])
        value += " and dt>"
        value += str(catch_list[i+1])
        value += ";"
        print(value)
        cs.execute(value)
        data = cs.fetchone()
        if data is None :
            data = 300
        else:
            data = data[0]
            print(data)
        for j in range(2,118):
            wi.append(data)
    print(wi)
    for i in range(0,5):
        value = ""
        value = "select humidity from weather where dt<"
        value += str(catch_list[i])
        value += " and dt>"
        value += str(catch_list[i+1])
        value += ";"
        print(value)
        cs.execute(value)
        data = cs.fetchone()
        if data is None :
            data = 25
        else:
            data = data[0]
        print(data)
        for j in range(2,118):
            wi_1.append(data)
    print(wi_1)
    for i in range(0,5):
        value = ""
        value = "select dt from weather where dt<"
        value += str(catch_list[i])
        value += " and dt>"
        value += str(catch_list[i+1])
        value += ";"
        print(value)
        cs.execute(value)
        data = cs.fetchone()
        if data is None :
            data = 0
        else:
            data = data[0]
        print(data)
        for j in range(2,118):
            wi_2.append(data)
    print(wi_2)
    cs.close()
    conn.close()
    return wi,wi_1,wi_2
def data_all(li,li_1,wi,wi_1,wi_2):
    data_dic = {"number" : li_1,
                "dt" : wi_2,
                "temp" : wi,
                "humidity" : wi_1,
                "available_bikes" : li
                }
    data = pd.DataFrame(data_dic)
    print(data)
    return data
def write_to_sql(y):
    arr = []
    arr_1 = []
    arr_2 = []
    for i in range(1,6):
        for j in range(2,118):
            arr.append(i)
            arr_1.append(j)
    for row in y:
        arr_2.append(row)
    # y_dic = {
    #             "available_bikes" : y
    #             }
    # y_predict = pd.DataFrame(y_dic)
    # y_predict["lastupdate"] = arr
    # y_predict["number"] = arr_1
    conn = connect(host="database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com", port=3306, user="admin", password="a123456789", database="project",
                            charset="utf8")
    cs = conn.cursor()
    cs.execute("truncate table bikestation_predict")
    conn.commit()
    for k in range(0,len(arr_1)):
        value = "insert into bikestation_predict values("
        value += str(arr_1[k])
        value += ","
        value += str(arr[k])
        value += ","
        value += str(arr_2[k])
        value += ");"
        print(value)
        cs.execute(value)
        conn.commit()
    cs.close()
    conn.close()
if __name__ == "__main__":
    li,li_1 = bikestation_data_catch()
    wi,wi_1,wi_2 = weather_data_catch()
    print(len(li))
    print(len(li_1))
    print(len(wi))
    print(len(wi_1))
    print(len(wi_2))
    data = data_all(li,li_1,wi,wi_1,wi_2)
    print(li)
    y_predict = bikestation_model(data)
    print(len(y_predict))
    print(type(y_predict))
    write_to_sql(y_predict)