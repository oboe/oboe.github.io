Avro is a language neutral data serialization system tackling the issue of Hadoop `Writables` not being language portable. 
- Code generation is optional in Avro, unlike Protocol Buffers.
- Usually schema written in JSON and encoded binary
- Avro datafiles has metadata section where schema is stored.
- Also support compression and are splittable

#### Avro Data Types and Schemas
Java can do
- Dynamic mapping of the schema (generic). Field names are referred with string value.
- Code generation
- Even Reflect mapping, using reflection to infer the Avro types

#### In-Memory Serialization and Deserialization
Can use Maven or Ant to create Java code for a schema.
#### Avro Datafiles
Datafiles have a metadata header, a sync marker and a set of blocks.
#### Schema Resolution
Strategy Avro does is having a reader and writer schemas that you use to read and write.
#### Avro MapReduce
Avro provides number of classes to make it easy to run MapReduce programs.

