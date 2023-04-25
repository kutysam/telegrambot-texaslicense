import datetime
import os

import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
chat_id = "610479895"

json_data = {
    'TypeId': 71,
    'ZipCode': '75206',
    'CityName': '',
    'PreferredDay': 0,
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://public.txdpsscheduler.com'
}


response = requests.post(
    'https://publicapi.txdpsscheduler.com/api/AvailableLocation', json=json_data, headers=headers)
locations = response.json()

format_str = '%m/%d/%Y'  # The format


smaller_date = []
for location in locations:
    proper_date = datetime.datetime.strptime(
        location['NextAvailableDate'], format_str)
    date_smaller = proper_date < datetime.datetime(2023, 5, 20)
    print(f"{location['Name']} - {proper_date.date()} - {date_smaller}")
    if date_smaller == True:
        smaller_date.append(f"{location['Name']} - {proper_date.date()}")

if len(smaller_date) != 0:
    msg = ""
    for i in smaller_date:
        msg += i + "\n"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=Markdown&disable_web_page_preview=True"
    print(requests.get(url).json())
