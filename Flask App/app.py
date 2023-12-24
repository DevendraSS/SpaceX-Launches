from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',launches=launches)

@app.template_filter("date_only")
def date_only_filter(s):
    date_obj = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_obj.date()


def fetch_launches():
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []



def categorize_launches(launches):
    successful = list(filter( lambda x: x["success"] and not x["upcoming"],launches))
    failed = list(filter( lambda x: not x["success"] and not x["upcoming"],launches))
    upcoming = list(filter( lambda x: x["upcoming"],launches))

    return {
        "successful": successful,
        "failed": failed,
        "upcoming": upcoming
    }



launches = categorize_launches(fetch_launches())


if __name__ == '__main__':
    app.run(debug=True,port=4400,host='0.0.0.0')
