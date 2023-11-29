from flask import Flask, request, jsonify
import requests

END_POINT = "https://www.gov.uk/bank-holidays.json"

app = Flask(__name__)

def fetch_holiday_data():
    response = requests.get(END_POINT)
    return response.json()

@app.route("/uk/bank-holidays")
def all_holidays():
    response = requests.get(END_POINT)
    data = fetch_holiday_data()
    print(type(data))
    return jsonify(data)

@app.route("/uk/country/<string:c_name>")
def get_country_holidays(c_name):
    response_data = fetch_holiday_data()
    if c_name in response_data:
        return jsonify(data=response_data[c_name])
    return jsonify( error={"Not Found": "The country you entred doesn't exist."}), 404

@app.route("/uk/bank-holidays/search-by-name")
def search_by_name():
    holiday_name = request.args.get('holiday-name')
    if holiday_name:
        data = {}
        response_data = fetch_holiday_data()
        for country in response_data:
            for event in response_data[country]["events"]:
                if holiday_name == event["title"]:
                    data[country] = {"event": event}
        if data:
           return jsonify(data=data)

        return jsonify({"Not Found": f"There's no holiday with this title {holiday_name}"}), 404
    return jsonify({"message": "No holiday name provided"}), 400

@app.route("/uk/bank-holidays/search-by-date")
def search_by_date():
    holiday_date = request.args.get('holiday-date')
    if holiday_date:
        data = {}
        response_data = fetch_holiday_data()
        for country in response_data:
            for event in response_data[country]["events"]:
                if holiday_date == event["date"]:
                    data[country] = {"event": event}
        if data:
           return jsonify(data=data)

        return jsonify({"Not Found": f"There's no holiday in this {holiday_date} date."}), 404
    return jsonify({"message": "No holiday date provided"}), 400

if __name__ == "__main__":
  app.run(debug=True)                          
