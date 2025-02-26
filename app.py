import datetime
import json
import os
import re
import urllib
from urllib.request import Request
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')

def check_ooni() -> int:
    url = "https://ooni.com/products/ooni-koda-16?variant=40170656432225"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    price_box = soup.find("div", attrs={"class": "price"})
    if price_box is None:
        print("Error: price_box was not found on the page")
        exit(1)
    price_string = re.search(r'\$\d\d\d.\d\d', price_box.get_text())
    price = round(float(price_string.group()[1:]))

    sale_price_box = soup.find("span", attrs={"class": "price__item price__item--sale price__item--last text-ml"})
    sale_price = None
    if sale_price_box is not None:
        sale_price_string = re.search(r'\$\d\d\d.\d\d', sale_price_box.get_text())
        sale_price = round(float(sale_price_string.group()[1:]))

    return sale_price if sale_price is not None else price

def send_message(message: str):
    message = {"text": f"{message}"}
    message_json = json.dumps(message)
    result = requests.post(slack_webhook_url, data=message_json)
    return json.dumps({"status": result.status_code})

if __name__ == "__main__":
    if check_ooni() < 599:
        send_message(f"Check for the Koda 16 price on https://ooni.com/products/ooni-koda-16?variant=40170656432225. Looks like the price is {check_ooni()}")
    else:
        send_message(message=f"No sales right now! Last checked at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
