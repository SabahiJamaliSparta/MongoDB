# NoSQL and MongoDB: Foundations and Practical Guide

Beginner revision notes covering database concepts, common commands and basic CRUD operations in `mongosh`.

## 1. What is NoSQL?

**NoSQL** describes databases that organise data using models other than traditional relational tables. The term is often explained as **“Not Only SQL.”**

NoSQL is a category of databases, not one product or one query language. Different NoSQL databases suit different tasks. [1]

## 2. Types of NoSQL databases

| Type | How it stores data | Example | Typical use |
|---|---|---|---|
| Document | Documents containing fields and values | MongoDB | Product catalogues and customer profiles |
| Key-value | A unique key linked to a value | Redis | Caching and login sessions |
| Wide-column | Rows whose columns can vary, grouped into column families | Apache Cassandra | Large volumes of event data |
| Graph | Nodes and the relationships between them | Neo4j | Social networks and connected-data searches |

These are four common categories; some databases support more than one model. [1]

## 3. What is MongoDB?

**MongoDB is a document database.** It stores records as BSON documents: a binary representation of JSON-like data that also supports types such as dates and ObjectIds. [2]

| Term | Simple definition |
|---|---|
| Database | A container for collections |
| Collection | A group of documents |
| Document | One record containing fields and values |
| Field | A named piece of information |
| Value | The information stored in a field |
| `_id` | A document's unique identifier within its collection |
| Nested document | A document stored inside another document |
| Array | A list of values |
| Filter | Conditions used to select documents |
| Schema | The intended structure and rules for data |

### MongoDB, Compass and mongosh

| Tool | Purpose |
|---|---|
| MongoDB Community Server | Stores data and processes database operations |
| `mongod` | The program that runs the database server |
| MongoDB Compass | A visual application for working with MongoDB |
| `mongosh` | A JavaScript-based shell for typing database commands |
| MongoDB Atlas | A managed cloud service for running MongoDB |

Compass and mongosh connect to a server; opening Compass alone does not start your local server.

## 4. MongoDB compared with a relational database

| Feature | MongoDB | Relational database, such as SQL Server |
|---|---|---|
| Records | Documents in collections | Rows in tables |
| Structure | Documents can have different fields | Tables define columns and their types |
| Related information | Can be embedded or referenced | Commonly linked through keys and joins |
| Queries | MongoDB Query Language | SQL |
| Data rules | Supports schema validation and unique indexes | Supports constraints such as foreign keys and unique keys |
| Common fit | Nested data and records with varying attributes | Closely related data requiring strong relational rules |

These are general differences, not absolute boundaries. Relational databases can support JSON, and MongoDB can combine collection data using `$lookup`.

MongoDB supports ACID transactions. A single-document write is atomic: it succeeds as a whole or does not apply. Multi-document transactions require a replica set or sharded cluster; they are not available on a standalone server like this basic local setup. [3]

## 5. Advantages and disadvantages

| Advantages | What this means |
|---|---|
| Flexible document structure | Different records can hold different fields. |
| Nested data | Related details can be stored together. |
| Incremental development | The data model can evolve as requirements change. |
| Indexing | Suitable indexes can speed up searches. |
| Scaling options | Sharding can distribute data across servers. |
| Availability options | Replica sets maintain copies of data on multiple servers. |

| Disadvantages or trade-offs | What to consider |
|---|---|
| Inconsistent data | Flexible fields need naming conventions and validation. |
| Duplicated information | Embedding repeated details can make updates harder. |
| Complex relationships | Some workloads are easier to model with relational tables. |
| Operational complexity | Replication, sharding and backups require planning. |
| Document size limit | A BSON document is limited to 16 MiB; avoid endlessly growing documents. |

**Flexible schema does not mean no design is needed.** Choose a model around how the application reads and changes information. MongoDB is not automatically faster or more suitable than SQL. [2][3][4]

## 6. Use cases for MongoDB

The following are illustrative uses, rather than claims about particular companies.

| Use case | Information stored | Why the document model can help |
|---|---|---|
| Online shopping | Product names, prices and specifications | Clothes and laptops need different attributes. |
| Gaming | Player profiles, achievements and preferences | Related player details can be kept together. |
| Content management | Articles, videos, tags and authors | Different content types need different fields. |
| Delivery tracking | Parcel details and delivery events | Supports storing and querying changing delivery information. |
| Sentiment analysis | Reviews or headlines alongside model results | Keeps source text and its analysis together. |
| Image management | Image links, descriptions and tags | Keeps searchable image information with related records. |

MongoDB stores and retrieves information. A separate application or AI model performs tasks such as sentiment classification. Images are commonly stored in external file storage, with their links in MongoDB; GridFS is another option for storing large files in MongoDB. [5]

**Published company example:** Bosch used MongoDB to store and analyse connected-device data, helping engineers understand how vehicle technology behaved in real conditions. The case study describes the need to handle large volumes of varied data and make it available for analysis quickly. [6]

## 7. Installation on a Mac

Run installation and server startup commands in **Mac Terminal**, not in mongosh. This guide uses Homebrew; install Homebrew first if `brew --version` is unavailable. [7][8]

```bash
brew --version
brew tap mongodb/brew
brew install mongodb-community
brew install --cask mongodb-compass
```

If Homebrew reports an untrusted formula, follow the specific trust instruction printed in its error, then retry installation. During this setup, these were required:

```bash
brew trust --formula mongodb/brew/mongodb-community
brew trust --formula mongodb/brew/mongodb-database-tools
```

### Starting the server

The standard Homebrew service command is:

```bash
brew services start mongodb/brew/mongodb-community
```

Check it with:

```bash
brew services list
```

**The manual method that worked in this session:** on this Apple Silicon Mac, run the following commands one at a time. This uses a separate data folder in your home directory. [9]

```bash
mkdir -p "$HOME/mongodb-data"
```

```bash
/opt/homebrew/opt/mongodb-community/bin/mongod --dbpath "$HOME/mongodb-data" --bind_ip 127.0.0.1 --port 27017
```

Use one startup method at a time. Keep this Terminal window open while using the manually started server. Press **Control+C** there to stop it. After restarting the Mac, rerun the manual startup command using the same folder to access the same data.

In Compass, connect using:

```text
mongodb://127.0.0.1:27017
```

`127.0.0.1` means your own computer; `27017` is the port used here. `ECONNREFUSED` usually means no server is accepting connections at that address and port.

## 8. Basic syntax and command reference

The remaining commands run in **mongosh**, including Compass's embedded mongosh panel. [10][11]

General pattern:

```javascript
db.collectionName.method(arguments)
```

| Syntax | Meaning |
|---|---|
| `db` | The currently selected database |
| `.` | Accesses a collection, method or nested field |
| `()` | Contains arguments passed to a method |
| `{}` | Defines a document; an empty filter matches all documents |
| `[]` | Defines an array |
| `:` | Separates a field from its value |
| `,` | Separates fields or arguments |
| `"text"` | A string value |
| `25`, `true`, `false` | Number and Boolean values, without quotes |
| `//` | Starts a single-line comment |

### Database and collection commands

| Command | Definition |
|---|---|
| `show dbs` | Lists available databases. |
| `use databaseName` | Selects a database. |
| `db` | Shows the current database. |
| `show collections` | Lists collections in the current database. |
| `db.createCollection("name")` | Creates a collection explicitly. |
| `db.collectionName.drop()` | Deletes a collection and its documents. |

### Document methods

| Method | Definition |
|---|---|
| `insertOne()` | Adds one document. |
| `insertMany()` | Adds several documents. |
| `find()` | Retrieves documents matching a filter. |
| `findOne()` | Retrieves one matching document. |
| `updateOne()` | Updates the first matching document. |
| `updateMany()` | Updates all matching documents. |
| `replaceOne()` | Replaces one matching document, preserving its `_id`. |
| `deleteOne()` | Deletes the first matching document. |
| `deleteMany()` | Deletes all matching documents. |
| `countDocuments()` | Counts matching documents. |

### Update and comparison operators

| Operator | Definition |
|---|---|
| `$set` | Adds a field or changes its value. |
| `$unset` | Removes a field. |
| `$inc` | Increases or decreases a numeric value. |
| `$push` | Adds an item to an array. |
| `$pull` | Removes matching items from an array. |
| `$gt` / `$gte` | Greater than / greater than or equal to. |
| `$lt` / `$lte` | Less than / less than or equal to. |
| `$ne` | Not equal to. |

Update operators describe changes; comparison operators describe conditions in filters. [12][13]

## 9. Guided practice: creating a database and collection

Use a separate practice database to keep these exercises apart from existing coursework. Run commands individually and in order.

```javascript
use mongodb_practice
```

This selects the database. Selecting a new name does not create stored data yet. Creating its first collection, explicitly or through an insert, creates the database.

```javascript
db.createCollection("students")
```

```javascript
show collections
```

Alternatively, inserting into a collection that does not exist creates it automatically. Use lowercase collection and field names consistently in this practice. `Institute` and `institute` are different collection names.

## 10. CRUD examples

**CRUD = Create, Read, Update and Delete.** These operations work on documents. [11]

### C — Create

```javascript
db.students.insertOne({
  name: "Luke",
  course: "Data",
  age: 25,
  trainer: { name: "Tommy", expertise: "Data" },
  skills: ["Python", "SQL"]
})
```

`trainer` is a nested document; `skills` is an array. MongoDB adds an `_id` if you do not supply one.

```javascript
db.students.insertMany([
  { name: "Amira", course: "Data", age: 24 },
  { name: "Ben", course: "DevOps", age: 27 }
])
```

Run inserts once: rerunning these commands adds more documents with new identifiers.

### R — Read

```javascript
// View every document
db.students.find()

// Find students on the Data course
db.students.find({ course: "Data" })

// Find one student
db.students.findOne({ name: "Luke" })

// Find students older than 24
db.students.find({ age: { $gt: 24 } })

// Search inside a nested document
db.students.find({ "trainer.name": "Tommy" })

// Count students on the Data course
db.students.countDocuments({ course: "Data" })
```

`"trainer.name"` is dot notation for a field inside `trainer`.

### U — Update

```javascript
// Change one student's course
db.students.updateOne(
  { name: "Luke" },
  { $set: { course: "DevOps" } }
)

// Add a status to every student still on the Data course
db.students.updateMany(
  { course: "Data" },
  { $set: { status: "Active" } }
)

// Change a nested field without replacing the whole trainer document
db.students.updateOne(
  { name: "Luke" },
  { $set: { "trainer.name": "Jessica" } }
)
```

The first argument is the **filter**; the second describes the **change**. `$set` keeps other fields unchanged. Use `_id` when a name could match several people. [12][14]

### D — Delete

Check the matching document first:

```javascript
db.students.find({ name: "Ben" })
```

Then remove one matching document:

```javascript
db.students.deleteOne({ name: "Ben" })
```

Removing only a field is an update, not a document deletion:

```javascript
db.students.updateOne(
  { name: "Amira" },
  { $unset: { status: "" } }
)
```

**Important:** an empty filter `{}` matches every document. In particular, `deleteMany({})` deletes all documents in a collection. [15]

### Reading the results

| Result field | Meaning |
|---|---|
| `acknowledged: true` | The server acknowledged the write; check the other fields to see its effect. |
| `insertedId` / `insertedIds` | Identifiers assigned to inserted documents. |
| `matchedCount` | Number of documents matching an update's filter. |
| `modifiedCount` | Number actually changed by the update. |
| `deletedCount` | Number of documents removed. |

An update can match a document but change nothing if it already contains the requested value.

## References

Official documentation and the published case study used to guide these notes. Accessed 22 October 2026. The practice examples are illustrative.

1. [MongoDB — NoSQL explained](https://www.mongodb.com/resources/basics/databases/nosql-explained)
2. [MongoDB — Data modelling](https://www.mongodb.com/docs/manual/data-modeling/)
3. [MongoDB — Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
4. [MongoDB — Limits and thresholds](https://www.mongodb.com/docs/manual/reference/limits/)
5. [MongoDB — GridFS](https://www.mongodb.com/docs/manual/core/gridfs/)
6. [MongoDB — Bosch customer case study](https://www.mongodb.com/solutions/customer-case-studies/bosch)
7. [MongoDB — Official Homebrew tap](https://github.com/mongodb/homebrew-brew)
8. [Homebrew — MongoDB Compass](https://formulae.brew.sh/cask/mongodb-compass)
9. [MongoDB — Run MongoDB manually](https://www.mongodb.com/docs/manual/administration/run-mongodb-manual/)
10. [MongoDB — mongosh help](https://www.mongodb.com/docs/mongodb-shell/reference/access-mdb-shell-help/)
11. [MongoDB — CRUD operations in mongosh](https://www.mongodb.com/docs/mongodb-shell/crud/)
12. [MongoDB — Update operators](https://www.mongodb.com/docs/manual/reference/operator/update/)
13. [MongoDB — Query predicates](https://www.mongodb.com/docs/manual/reference/operator/query/)
14. [MongoDB — updateMany()](https://www.mongodb.com/docs/manual/reference/method/db.collection.updateMany/)
15. [MongoDB — Delete documents](https://www.mongodb.com/docs/mongodb-shell/crud/delete/)
