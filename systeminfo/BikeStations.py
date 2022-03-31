import requests
import json
from pymysql import connect
class BikeStationsSpider:
    def __init__(self):
        self.url = "https://api.jcdecaux.com/vls/v1/stations/?contract=dublin&apiKey=834f2e1637837b203eb99c95d0452276a0d3e1e7"
    def parse_url(self):
        response = requests.get(self.url)
        content = json.loads(response.text)
        self.save_data(content)
    def save_data(self,content):
        conn = connect(host="database.c9wohqhfjk3g.eu-west-1.rds.amazonaws.com", port=3306, user="admin", password="a123456789", database="project",
                            charset="utf8")
        cs = conn.cursor()
        for i in range(0,len(content)):
            print(type(content[i]["number"]))
            value = "insert into bikestation values("
            value += str(content[i]["number"])
            value += ","
            value += "\"" + str(content[i]["contract_name"]) + "\""
            value += ","
            value += "\"" + str(content[i]["name"]) + "\""
            value += ","
            value += "\"" + str(content[i]["address"]) + "\""
            value += ","
            value += "\"" + str(content[i]["position"]["lat"]) + "\""
            value += ","
            value += "\"" + str(content[i]["position"]["lng"]) + "\""
            value += ","
            value += "\"" + str(content[i]["banking"]) + "\""
            value += ","
            value += "\"" + str(content[i]["bonus"]) + "\""
            value += ","
            value += str(content[i]["bike_stands"])
            value += ","
            value += str(content[i]["available_bike_stands"])
            value += ","
            value += str(content[i]["available_bikes"])
            value += ","
            value += "\"" + str(content[i]["status"]) + "\""
            value += ","
            value += "\"" + str(content[i]["last_update"]) + "\""
            value +=");"
            print(value)
            cs.execute(value)
            conn.commit()
        cs.close()
        conn.close()
    def run(self):
        self.parse_url()
if __name__ == "__main__":
    Bike = BikeStationsSpider()
    Bike.run()

