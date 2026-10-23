# NoSQL and MongoDB: Foundations and Practical Guide

A general reference covering NoSQL, MongoDB and relational databases, with basic commands and examples.

## 1. What is NoSQL?

**SQL (Structured Query Language)** is used to work with relational databases, which organise records into rows and columns. SQL Server, PostgreSQL and MySQL are examples of relational database systems.


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

**MongoDB is a document-oriented NoSQL database.** It stores records as documents containing field–value pairs, rather than rows in tables. Documents can contain text, numbers, arrays and nested documents. [12]

MongoDB stores documents in **BSON**, a binary format supporting JSON-like structures and additional types such as dates and ObjectIds. [2]

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

### A simple document

```javascript
{
  name: "Notebook",
  price: 4.50,
  details: { colour: "Blue", pages: 100 },
  tags: ["stationery", "paper"]
}
```

`details` is a nested document; `tags` is an array. Related information can be retrieved together as part of one record.

## 4. MongoDB compared with a relational database

SQL is a language; MongoDB is a database system. The comparison below concerns MongoDB and relational database systems.


| Feature | MongoDB | Relational database, such as SQL Server |
|---|---|---|
| Records | Documents in collections | Rows in tables |
| Structure | Documents can have different fields | Tables define columns and their types |
| Related information | Can be embedded or referenced | Commonly linked through keys and joins |
| Queries | MongoDB Query Language | SQL |
| Data rules | Supports schema validation and unique indexes | Supports constraints such as foreign keys and unique keys |
| Common fit | Nested data and records with varying attributes | Closely related data requiring strong relational rules |

These are general differences, not absolute boundaries. Relational databases can support JSON, and MongoDB can combine collection data using `$lookup`.

MongoDB supports ACID transactions. A single-document write is atomic: it succeeds as a whole or does not apply. Multi-document transactions require a replica set or sharded cluster; they are not available on standalone servers. [3]

### Scaling: handling more data or users

**Vertical scaling — scale up**

- Make one server more powerful by increasing RAM, CPU or storage.
- Often a straightforward starting point for relational databases, including transaction-heavy applications.
- Simpler infrastructure, but limited by the capacity of one server.

**Horizontal scaling — scale out**

- Add servers and distribute the data and workload.
- Common in NoSQL systems supporting large datasets and high demand.
- MongoDB uses **sharding** to divide data between servers.
- More capacity, but greater coordination and management complexity.

Both database types can use either approach. **Replication** maintains copies of data for availability; **sharding** divides data across servers. [13]

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

## 6. Three common use cases

1. **Product catalogues:** store products with different attributes, such as clothing sizes and laptop specifications.
2. **Content management:** organise articles, videos, tags and author details with different structures.
3. **Connected devices:** store sensor readings and device information for monitoring and analysis.

These are illustrative applications of the document model, rather than a claim that MongoDB is always the best choice. [2][12]

## 7. Installation and tools

On a Mac with Homebrew installed, run these commands individually in Terminal: [5][6]

```bash
brew tap mongodb/brew
brew install mongodb-community
brew install --cask mongodb-compass
brew services start mongodb/brew/mongodb-community
```

If Homebrew requests trust for a formula, follow its displayed instruction and retry. Installation requirements depend on the operating system and package version.

Connect locally using `mongodb://localhost:27017/`.

| Tool | Purpose |
|---|---|
| MongoDB Community Server | Stores data and processes queries. |
| `mongod` | Runs the database server. |
| Compass | Provides a visual interface for MongoDB. |
| `mongosh` | Runs MongoDB commands interactively. |
| Atlas | Provides MongoDB as a managed cloud service. |

The server must be running before Compass, mongosh or Python can connect to it.

## 8. Basic syntax and command reference

The remaining commands run in **mongosh**, including Compass's embedded mongosh panel. [7][8]

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

Update operators describe changes; comparison operators describe conditions in filters. [9][10]

## 9. Creating a database and collection

In mongosh:

```javascript
use shop
db.createCollection("products")
show collections
```

`use shop` selects the database. Creating the first collection creates the database if it does not exist. Inserting a document can also create its collection automatically. Keep collection and field names consistent: `products` and `Products` are different names.

## 10. Basic CRUD operations

**CRUD** means Create, Read, Update and Delete. The examples below use the `products` collection in the `shop` database. [8]

```javascript
use shop
```

**Create — add one document**

```javascript
db.products.insertOne({ name: "Notebook", price: 4.50 })
```

**Read — find matching documents**

```javascript
db.products.find({ name: "Notebook" })
```

**Update — change a field**

```javascript
db.products.updateOne({ name: "Notebook" }, { $set: { price: 5.00 } })
```

The first argument selects the document; `$set` changes the specified field.

**Delete — remove one matching document**

```javascript
db.products.deleteOne({ name: "Notebook" })
```

| Method | Meaning |
|---|---|
| `insertOne()` / `insertMany()` | Adds one / several documents. |
| `find()` / `findOne()` | Retrieves matching documents / one matching document. |
| `updateOne()` / `updateMany()` | Updates the first / all matching documents. |
| `deleteOne()` / `deleteMany()` | Deletes the first / all matching documents. |

A **filter** specifies which documents to act on. An empty filter `{}` matches every document. Names need not be unique; use `_id` to target a particular record reliably.

### Reading write results

| Result field | Meaning |
|---|---|
| `acknowledged: true` | The server acknowledged the write. |
| `insertedId` / `insertedIds` | Identifiers of inserted documents. |
| `matchedCount` | Documents matching an update filter. |
| `modifiedCount` | Documents actually changed. |
| `deletedCount` | Documents removed. |

An update can match a document but change nothing if it already contains the requested value.

## 11. Validation: controlling document structure

**Schema validation** checks required fields, data types and allowed values. Rules can be managed in a collection’s **Validation** tab in Compass. [14]

| Keyword | Purpose |
|---|---|
| `required` | Lists fields that must exist. |
| `bsonType` | Specifies a stored data type, such as `string`, `int`, `double` or `object`. |
| `minimum` / `maximum` | Sets inclusive numeric limits. |
| `enum` | Lists allowed values. |
| `properties` | Defines rules for individual fields, including nested fields. |
| `description` | Explains a rule without enforcing it itself. |

**Error** rejects invalid writes; **Strict** applies validation to all inserts and updates. Changing validation does not automatically correct or remove existing documents. Validation is specific to the collection where it is applied.

## 12. PyMongo: MongoDB from Python

**PyMongo** is the official Python driver for MongoDB. It lets Python applications connect to a server and work with documents. [15][16]

Install it in the project’s Python environment:

```bash
python -m pip install pymongo
```

A basic connection and read query:

```python
from pymongo import MongoClient

with MongoClient("mongodb://localhost:27017/") as client:
    client.admin.command("ping")
    db = client["shop"]
    print(db["products"].find_one({"name": "Notebook"}))
```

`ping` checks that the server responds. `find_one()` returns one matching document, or `None` if no match exists. The `with` block closes the client automatically when it ends. This read example assumes a matching product already exists. [15][16]

## 13. Aggregation: summarising data

An **aggregation pipeline** passes documents through ordered stages to filter, group, calculate or reshape information. [17]

| Operator | Meaning |
|---|---|
| `$match` | Keeps documents meeting conditions. |
| `$group` | Combines documents sharing a group key. |
| `$sum` | Adds values; `$sum: 1` counts documents. |
| `$avg` | Calculates the average of numeric values. |
| `$max` | Returns the greatest value. |
| `$sort` | Orders results: `1` ascending, `-1` descending. |
| `$project` | Selects or reshapes output fields. |
| `$toDouble` | Converts a supported value to a double. |
| `$nin` | Excludes listed values. |

In an expression, `"$price"` refers to a field, while `"price"` alone is literal text. In `$group`, `_id` holds the group key. Convert numeric text before calculating numerical results; `$convert` can also handle invalid or missing values. [18]

## References

Definitions and examples are adapted from the sources below. MongoDB’s official documentation guides technical behaviour; the Everpure article provides introductory context. Reviewed 22–23 October 2026.

1. [MongoDB — NoSQL explained](https://www.mongodb.com/resources/basics/databases/nosql-explained)
2. [MongoDB — Data modelling](https://www.mongodb.com/docs/manual/data-modeling/)
3. [MongoDB — Transactions](https://www.mongodb.com/docs/manual/core/transactions/)
4. [MongoDB — Limits and thresholds](https://www.mongodb.com/docs/manual/reference/limits/)
5. [MongoDB — Official Homebrew tap](https://github.com/mongodb/homebrew-brew)
6. [Homebrew — MongoDB Compass](https://formulae.brew.sh/cask/mongodb-compass)
7. [MongoDB — mongosh help](https://www.mongodb.com/docs/mongodb-shell/reference/access-mdb-shell-help/)
8. [MongoDB — CRUD operations in mongosh](https://www.mongodb.com/docs/mongodb-shell/crud/)
9. [MongoDB — Update operators](https://www.mongodb.com/docs/manual/reference/operator/update/)
10. [MongoDB — Query predicates](https://www.mongodb.com/docs/manual/reference/operator/query/)
11. [MongoDB — updateMany()](https://www.mongodb.com/docs/manual/reference/method/db.collection.updateMany/)
12. [Everpure — What Is MongoDB?](https://www.everpuredata.com/uk/knowledge/what-is-mongodb.html)
13. [MongoDB — Sharding and scaling](https://www.mongodb.com/docs/manual/sharding/)
14. [MongoDB Compass — Validation](https://www.mongodb.com/docs/compass/validation/)
15. [MongoDB — Connect with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/)
16. [MongoDB — Find documents with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/)
17. [MongoDB — Aggregation with PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/)
18. [MongoDB — $convert](https://www.mongodb.com/docs/manual/reference/operator/aggregation/convert/)
