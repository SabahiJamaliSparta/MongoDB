import pymongo
import requests

def get_pilot_id(pilot_url, characters):
    try:
        # Request the pilot's details and check for errors
        response = requests.get(pilot_url, timeout=10)
        response.raise_for_status()
        pilot = response.json()

    except requests.RequestException as error:
        # Report the request error and stop
        print("Unable to fetch pilot:", error)
        raise

    # Find the pilot in the existing characters collection
    character = characters.find_one({"name": pilot["name"]})

    # Stop if the pilot cannot be matched
    if character is None:
        raise ValueError("Pilot not found: " + pilot["name"])

    # Return the character's existing ObjectId
    return character["_id"]

def transform_pilots(starships, characters):
    # Go through every starship
    for starship in starships:
        pilot_ids = []

        # Find the existing ObjectId for each pilot URL
        for pilot_url in starship["pilots"]:
            pilot_id = get_pilot_id(pilot_url, characters)
            pilot_ids.append(pilot_id)

        # Replace the URLs with the list of ObjectIds
        starship["pilots"] = pilot_ids

    # Return the transformed starships
    return starships

def get_starships():
    # Set the starting URL and create an empty list
    url = "https://swapi.dev/api/starships/"
    starships = []

    # Repeat to retrieve data from additional pages
    while url:
        try:
            # Request the current page and check for errors
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as error:
            # Report the request error and stop
            print("Unable to fetch starships:", error)
            raise

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

# Replace pilot URLs with character ObjectIds
starships = transform_pilots(starships, characters)

# Display one ship with pilots to check the transformation
for starship in starships:
    if starship["pilots"]:
        print(starship["name"], starship["pilots"])
        break

def save_starships(starships, collection):
    # Go through each transformed starship
    for starship in starships:
        # Replace an existing ship or insert it if not found
        collection.replace_one(
            {"url": starship["url"]}, starship, upsert=True
        )
# Select the starships collection
starships_collection = db["Starships"]

# Save the transformed starships
save_starships(starships, starships_collection)

# Display the number of stored starships
print("Starships stored:", starships_collection.count_documents({}))

# Close the MongoDB connection
client.close()





