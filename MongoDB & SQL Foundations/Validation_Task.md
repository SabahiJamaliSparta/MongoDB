# MongoDB Validation Task

Validation rules for the `students` collection in the `sparta` database, added through **Compass → Validation** with **Action: Error** and **Level: Strict**.

## 1. Name: required and a string

Add `"name"` to `required`.

```json
"name": {
  "bsonType": "string",
  "description": "Name is required and must be a string."
}
```

## 2. Year: required, an integer and within a realistic range

Add `"year"` to `required`. I used **2000–2100 inclusive**, treating year as the course year.

```json
"year": {
  "bsonType": "int",
  "minimum": 2000,
  "maximum": 2100,
  "description": "Year is required and must be an integer between 2000 and 2100."
}
```

## 3. Score: required and a double

Add `"score"` to `required`.

```json
"score": {
  "bsonType": "double",
  "description": "Score is required and must be a double."
}
```

## 4. Course: required and restricted to Data, DevOps or Test

Add `"course"` to `required`.

```json
"course": {
  "bsonType": "string",
  "enum": ["Data", "DevOps", "Test"],
  "description": "Course is required and must be Data, DevOps or Test."
}
```

## 5. Address: required and an object containing city and street

Add `"address"` to the main `required` array. The nested `required` array makes city and street compulsory inside address.

```json
"address": {
  "bsonType": "object",
  "required": ["city", "street"],
  "description": "Address is required and must contain city and street.",
  "properties": {
    "city": {
      "bsonType": "string",
      "description": "City is required and must be a string."
    },
    "street": {
      "bsonType": "string",
      "description": "Street is required and must be a string."
    }
  }
}
```

## 6. Add a description to each property

Each rule above includes a `description`, including the nested city and street properties.

The completed main required list is:

```json
"required": ["name", "year", "score", "course", "address"]
```

These are schema excerpts, not standalone validators. They sit inside the existing `$jsonSchema` structure, with commas between adjacent property rules.

## Syntax used

| Keyword | Simple meaning | Example from this task |
|---|---|---|
| `$jsonSchema` | Defines the structure and validation rules for documents. | Contains all the student validation rules. |
| `bsonType` | Specifies the MongoDB data type a value must have. | `"bsonType": "string"` requires text. |
| `required` | Lists fields that must be present. | `"required": ["name", "year"]` makes both fields compulsory. |
| `properties` | Contains the validation rules for individual fields. | Holds the rules for name, year and the other fields. |
| `enum` | Lists the only values a field is allowed to contain. | `"enum": ["Data", "DevOps", "Test"]` restricts the course choices. |
| `minimum` | Sets the lowest allowed numeric value, including that value. | `"minimum": 2000` allows 2000 or higher. |
| `maximum` | Sets the highest allowed numeric value, including that value. | `"maximum": 2100` allows 2100 or lower. |
| `description` | Explains a rule; it does not enforce the rule itself. | `"Name is required and must be a string."` |

**BSON** is the binary document format MongoDB uses to store data. The types used here are `string` (text), `int` (a 32-bit integer), `double` (a floating-point number that supports decimals) and `object` (a nested document containing fields).

**Remember:** `required` checks that a field exists; `bsonType` checks its type. A field needs both rules when it must be present and have a particular type.

## Reference

[MongoDB documentation — Specify JSON Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/)
