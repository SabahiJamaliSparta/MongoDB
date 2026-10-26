# PyMongo Mini Project: Starships and Pilots

## Project aim

Retrieve all available starships from [SWAPI](https://swapi.dev/), replace their pilot URLs with existing character ObjectIds, and save the transformed starships in MongoDB.

The project follows **Extract → Transform → Load (ETL)**:

- **Extract:** download starships from every API page.
- **Transform:** match each pilot to the existing `Characters` collection.
- **Load:** store the starships in a separate `Starships` collection.

## 1. Set up Python and MongoDB

Install the packages in the project's Python environment:

```bash
python -m pip install pymongo requests
```

Import the packages and connect to the local database:

```python
import pymongo
import requests

# Connect to MongoDB and select the database
client = pymongo.MongoClient()
db = client["StarWars"]
characters = db["Characters"]
```

`pymongo` communicates with MongoDB; `requests` retrieves API data. The local MongoDB server must be running.

## 2. Check the first starship

I first requested `https://swapi.dev/api/starships/` and printed the first item in `results`.

The first record was **CR90 corvette**, with `pilots: []`. An empty list means no pilots are listed for that ship and should remain empty.

The API response contains `results` for the current page and `next` for the following page's URL.

## 3. Extract all starships

I used a function to follow the pages until `next` became `None`:

```python
def get_starships():
    # Set the starting URL and create an empty list
    url = "https://swapi.dev/api/starships/"
    starships = []

    # Repeat while another page is available
    while url:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Add the results and move to the next page
        starships.extend(data["results"])
        url = data["next"]

    return starships
```

`extend()` combines the pages into one list. The observed result was:

```text
Starships fetched: 36
```

## 4. Match a pilot to an existing ObjectId

The character record inspected contained `_id` and `name`, but no original API URL. I therefore followed each pilot URL to retrieve the name, then searched for that name in MongoDB.

```python
def get_pilot_id(pilot_url, characters):
    # Request the pilot's details and check for errors
    response = requests.get(pilot_url, timeout=10)
    response.raise_for_status()
    pilot = response.json()

    # Find the matching character
    character = characters.find_one({"name": pilot["name"]})

    # Stop if no matching character exists
    if character is None:
        raise ValueError("Pilot not found: " + pilot["name"])

    # Return the existing ObjectId
    return character["_id"]
```

I tested this using Luke Skywalker's API URL. It returned an existing character ObjectId successfully.

**The API number is not a MongoDB ObjectId.** The solution retrieves the stored `_id`; it does not generate a new identifier. Name matching assumes each pilot name identifies one character.

## 5. Transform every pilot list

```python
def transform_pilots(starships, characters):
    # Go through each starship
    for starship in starships:
        pilot_ids = []

        # Match each pilot URL to a character ObjectId
        for pilot_url in starship["pilots"]:
            pilot_id = get_pilot_id(pilot_url, characters)
            pilot_ids.append(pilot_id)

        # Replace the URLs with ObjectIds
        starship["pilots"] = pilot_ids

    return starships
```

Each ship keeps a list because it may have several pilots. Ships with no pilots keep `[]`.

I printed the first ship with pilots. **Millennium Falcon** had four `ObjectId(...)` values, confirming that its URLs had been replaced.

## 6. Load the transformed starships

```python
def save_starships(starships, collection):
    # Save each ship using its API URL as the match
    for starship in starships:
        collection.replace_one(
            {"url": starship["url"]}, starship, upsert=True
        )
```

- `replace_one()` replaces a document matching the ship's URL.
- `upsert=True` inserts the ship when no match exists.
- Matching by URL avoids adding another copy during normal sequential reruns. It does not remove duplicates that already exist.

## 7. Run the functions in order

In the Python file, place the imports first, then all four function definitions, followed by this execution code:

```python
# Connect to MongoDB and select the collections
client = pymongo.MongoClient()
db = client["StarWars"]
characters = db["Characters"]
starships_collection = db["Starships"]

# Extract all starships
starships = get_starships()
print("Starships fetched:", len(starships))

# Transform the pilot URLs into ObjectIds
starships = transform_pilots(starships, characters)

# Load the transformed documents
save_starships(starships, starships_collection)
print("Starships stored:", starships_collection.count_documents({}))

# Close the connection
client.close()
```

The connection snippet in Step 1 explains setup; use the execution block above once, rather than repeating both connection blocks. Run the whole file to fetch fresh URLs before transforming them.

## 8. Results and remaining checks

| Check | Observed result |
|---|---|
| Fetch all API pages | 36 starships retrieved |
| Match a single pilot | Luke's existing ObjectId returned |
| Transform pilot lists | Four ObjectIds displayed for Millennium Falcon |
| Count stored documents | 37 documents reported |

**The count discrepancy remains unresolved:** 36 ships were fetched, while the collection contained 37 documents. `count_documents({})` counts the entire collection, including previous records. The extra document needs checking before any deletion.

The script includes pseudocode-style comments, functions, request timeouts, HTTP status checks and an error for an unmatched pilot. **Retry logic and `$lookup` relationship checks have not yet been implemented.** The lookup bonus should confirm that every stored pilot reference resolves to a character; displaying ObjectIds alone does not prove all relationships are valid.

## References

- [SWAPI documentation — resources and starships](https://swapi.dev/documentation)
- [PyMongo — Connect to MongoDB](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/)
- [PyMongo — Find documents](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/)
- [PyMongo — Replace documents and upsert](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/)
- [Requests — Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
