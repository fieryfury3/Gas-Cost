import pandas as pd
import requests
from bs4 import BeautifulSoup
vehicle_df = pd.read_csv("https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip", low_memory=False)
vehicle_df = vehicle_df[["city08","comb08","fuelType","highway08","make", "model", "year"]]
vehicle_df["model"] = vehicle_df['model'].str.lower()
vehicle_df["model"] = vehicle_df['model'].str.replace(' ','')
vehicle_df = vehicle_df.set_index("model")
vehicle_df = vehicle_df.astype(str)   # Change all data types to string for ease of use
def questions():
    global year, make, model, city1, state1, city2, state2
    print("What year is your vehicle?")
    year = input().lower().replace(' ','')
    print("What make is your vehicle?")
    make = input().lower().replace(' ','')
    print("What model is your vehicle?")
    model = input().lower().replace(' ','')
    print("Starting City: ")
    city1 = str(input().replace(" ", "-").lower())
    print("Starting State Abbreviation: ")
    state1 = str(input().replace(" ", "-").lower())
    print("Destination City: ")
    city2 = str(input().replace(" ", "-").lower())
    print("Destination State Abbreviation: ")
    state2 = str(input().replace(" ", "-").lower())
def mileage():
    for index, row in vehicle_df.iterrows():
        if row["make"].lower().replace(' ','') == make and row["year"].lower().replace(' ','') == year and model in vehicle_df.index:
            return int(row[["comb08"]]) #Iterate through dataframe and return the combined mpg (highway + city)


def distance():
    site = ("https://www.distancebetweencities.net/" + city1 + "_" + state1 + "_" + "and" + "_" + city2 + "_" + state2)
    r = requests.get(site)
    soup = BeautifulSoup(r.text, 'html.parser')
    distance = soup.find("span", class_="data-driving-mile")
    distance = distance.text.replace("Miles", "")
    return int(distance) # return the distance between two cities

def gas_prices():
    site = "https://www.gasbuddy.com/USA"
    r = requests.get(site)
    soup = BeautifulSoup(r.text, 'html.parser')
    state1_price = soup.find("a", id=state1.upper())
    state2_price = soup.find("a", id=state2.upper())
    soup1 = state1_price
    soup2 = state2_price
    gas_price = soup1.find("div", class_="col-sm-2 col-xs-3 text-right")
    gas_price = gas_price.text
    gas_price1 = soup2.find("div", class_="col-sm-2 col-xs-3 text-right")
    gas_price1 = gas_price1.text
    return {'gas_price' : gas_price, 'gas_price1': gas_price1} # return average price of gas per gallon for each state
questions()
prices = list(gas_prices().values())
price1 = float(prices[0]) # avg price of state1's gas per gallon
price2 = float(prices[1]) # avg price of state2's gas per gallon
avg_price = ((price1 + price2)/2) #state1 and state2 combined avg price of gas
mpg = mileage()
miles = distance()
gallons_needed = float(miles/mpg)
cost = avg_price*gallons_needed
print("Gallons of gas needed: " + str(gallons_needed))
print("Calculated cost of gas for trip: $" + str(cost))


#Ideas : Could add stops needed to refill based on gas tank size of selected vehicle, average price of gas for all states traveled through to get a better average price.
