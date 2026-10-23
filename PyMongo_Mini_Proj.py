import pymongo
import requests


def get_starships():
    # Request the first page of starships
    response = requests.get("https://swapi.dev/api/starships/", timeout=10)

    # Check that the request succeeded
    response.raise_for_status()

    # Return the response as Python data
    return response.json()


# Connect to the local MongoDB server
client = pymongo.MongoClient()

# Select the StarWars database
db = client["StarWars"]

# Fetch the data and display the first starship - Results show CR90 Corvette fetched
data = get_starships()
print(data["results"][0])

