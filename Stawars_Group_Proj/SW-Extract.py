import pymongo
from pprint import pprint
import pandas as pd

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"]

print("Collections:", db.list_collection_names()) # list of collections

print("\n--- CHARACTER EXAMPLE ---")
pprint(db["characters"].find_one())

print("\n--- STARSHIP EXAMPLE ---")
pprint(db["starships"].find_one())

print("\n--- DOCUMENT COUNTS ---")
print("Characters:", db["characters"].count_documents({}))
print("Starships:", db["starships"].count_documents({}))

client.close()


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"]
characters = list(db["characters"].find()) # loading documents into Python lists
starships = list(db["starships"].find())

print("Characters loaded:", len(characters))
print("Starships loaded:", len(starships))

# Convert the documents into DataFrames
characters_df = pd.DataFrame(characters)
starships_df = pd.DataFrame(starships)

# Inspect the structure
print("\nCHARACTERS")
print(characters_df.head())
print("\nCharacter columns:")
print(characters_df.columns.tolist())

print("\nSTARSHIPS")
print(starships_df.head())
print("\nStarship columns:")
print(starships_df.columns.tolist())

client.close()



from sqlalchemy import create_engine, text

# Create a connection to a local SQLite database
engine = create_engine("sqlite:///starwars.db")

# Test the connection
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("SQL connection successful!")
    print("Test result:", result.scalar())

