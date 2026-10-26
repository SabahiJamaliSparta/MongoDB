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

    def test_starship_pilot_id():
        # Create a mock database
        client = mongomock.MongoClient()
        db = client["StarWars"]

        # Add a character and keep their ObjectId
        pilot_id = db.Characters.insert_one(
            {"name": "Luke Skywalker"}
        ).inserted_id

        # Add a starship using the pilot's ObjectId
        db.Starships.insert_one({
            "name": "X-wing",               #The name of a fictional Star Wars starship. It is sample data, like
            "pilots": [pilot_id]
        })

        # Find the starship
        starship = db.Starships.find_one({"name": "X-wing"}) #Finds one document whose name is "X-wing"

        # Check the starship exists and references the correct pilot
        assert starship is not None                        #Checks that a starship was found.
        assert starship["pilots"] == [pilot_id]            #Checks that its pilots list contains the expected character’s _id.

        # Close the connection
        client.close()