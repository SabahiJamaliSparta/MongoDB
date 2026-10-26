import mongomock

def test_find_pilot():
    #Create a mock database
    client = mongomock.MongoClient() #Creates a database in memory for testing.
    db = client ["StarWars"]

    # Add a character
    db.Characters.insert_one({"name": "Luke Skywalker"})

    # Find the character
    pilot = db.Characters.find_one({"name": "Luke Skywalker"}) #Finds one matching document.

    # Check the character was found
    assert pilot is not None #Checks that something is true. The test fails if it is false.
    assert pilot["name"] == "Luke Skywalker"

    # Close the connection
    client.close()