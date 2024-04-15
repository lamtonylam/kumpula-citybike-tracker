import requests
import sys
from os import getenv
import json

from flask import Flask
from flask import render_template

url = "https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql"
headers = {
    "digitransit-subscription-key": getenv("digitransit_key"),
    "Content-Type": "application/json",
}

query = """
{
	bikeRentalStation(id:"204") {
		stationId
		name
		bikesAvailable
		capacity
		lat
		lon
		allowDropoff
  }
}
"""

response = requests.post(url, json={"query": query}, headers=headers)
print(response.json())
print(response.json()["data"]["bikeRentalStation"]["bikesAvailable"])

kumpulan_aseman_nimi = response.json()["data"]["bikeRentalStation"]["name"]
pyorien_maara = response.json()["data"]["bikeRentalStation"]["bikesAvailable"]
maksimi_pyorien_maara = response.json()["data"]["bikeRentalStation"]["capacity"]
lat = response.json()["data"]["bikeRentalStation"]["lat"]
lon = response.json()["data"]["bikeRentalStation"]["lon"]

app = Flask(__name__)


@app.route("/")
def index():
    if pyorien_maara > 0:
        viesti = "Kyllä!"
    else:
        viesti = "Ei :("
    return render_template("index.html", 
    viesti=viesti, 
    pyorien_maara=pyorien_maara,
    kumpulan_aseman_nimi=kumpulan_aseman_nimi,
    maksimi_pyorien_maara=maksimi_pyorien_maara,
    lat=lat,
    lon=lon
    )
