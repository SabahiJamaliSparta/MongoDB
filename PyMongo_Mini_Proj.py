import pymongo
import requests

def get_pilot_id(pilot_url, characters):
    # Request the pilot's details and check for errors
    response = requests.get(pilot_url, timeout=10)
    response.raise_for_status()
    pilot = response.json()

    # Find the pilot in the existing characters collection
    character = characters.find_one({"name": pilot["name"]})

    # Stop if the pilot cannot be matched
    if character is None:
        raise ValueError("Pilot not found: " + pilot["name"])

    # Return the character's existing ObjectId
    return character["_id"]

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

# Test matching Luke Skywalker's API record to his ObjectId
pilot_id = get_pilot_id("https://swapi.dev/api/people/1/", characters)
print("Pilot ObjectId:", pilot_id)

# Close the MongoDB connection
client.close()

