import pymongo
import requests


def get_starships():
    # Set the starting URL and create an empty list
    url = "https://swapi.dev/api/starships/"
    starships = []

    # Repeat while another page is available
    while url:
        # Request the current page and check for errors
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Add the current page's starships to the list
        starships.extend(data["results"])

        # Get the next page's URL
        url = data["next"]

    # Return all starships
    return starships


# Connect to the local MongoDB server
client = pymongo.MongoClient()

# Select the StarWars database
db = client["StarWars"]

# Fetch all starships and display the total
starships = get_starships()
print("Starships fetched:", len(starships))

#Check how we can match pilots to your characters.

# Select the existing characters collection
characters = db["Characters"]

# Display one character's identifier, name and API URL
print(characters.find_one({}, {"_id": 1, "name": 1, "url": 1}))

# Close the MongoDB connection
client.close()

