---
layout: post
tags: [Hadoop]
---
Parquet is columnar storage format that can efficiently store nested data.
- Columnar files are usually more efficient because column values are stored next to each other which means that you can do better encoding.
- Columnar files are better for read heavy workloads as queries are usually faster. As all values of a column are stored together. (Relational DBs prefer rows as usually their workload is like editing customers shopping cart)

Key strength of parquet is ability to store nested data well.
- Great as often data has deeply nested structure.
- Takes technique introduced in Google Dremel.
- Enabling nested fields to be read without reading the other nested field. Kinda crazy!

Smart of engineers to also enable using different data models to read parquet files.

#### Data Model
Parquet files has a schema of primitive types, with a root `message` with the fields.
- Primitives are required, optional or repeated
- No strings
- Nesting is with `groups`
- More complex structures are built with these primitives. e.g lists, maps, strings, dates, etc.

Parquet uses encoding from Dremel where every primitive type field in schema is stored in separate column. Damn must make encoding super efficient.
- This encoding enables us to read map keys without reading the corresponding map values 😎

#### Parquet File Format

```
File:
Header -> Block -> Block -> Footer
```

Header
- Just contains a magic number identifying the file as parquet 

Footer
- Contains all the metadata 
- Format version
- Schema
- Extra Key value pairs
- Metadata for all file blocks
- And 4 byte field encoding the length of footer
- And the parquet magic number

What does the structure mean?
- Means that we need to SEEK to read the footer metadata length
- Then
- Seek by that length to read the footer metadata
- before we can actually read the data in the blocks

Avro just has metadata in header and sync markers between blocks but Parquet just needs a footer read to get all this info.

```
Block: aka Row Group
Col chunk -> Col chunk -> Col Chunk

Col chunk
page -> page -> page
```

Each page has all values from same column.

Parquet will choose the best encoding depending on the column type.
#### Parquet Configuration
You can choose the block size. Dont make the block size above the HDFS block size.