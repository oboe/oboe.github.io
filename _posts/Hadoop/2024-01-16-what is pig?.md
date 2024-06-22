---
layout: post
tags: [Hadoop]
---
MapReduce is great to process large data but in use often you need to carefully craft multiple MapReduce stages to do preprocessing etc. Pig helps you do this. Two pieces
- Language to do this: Pig Latin
- Execution environment to run Pig Latin.

#### Running Pig
A simple client application.
#### Example
Kinda looks like SQL. Just simple verb commands. Also provides an illustrate command to generate dummy datasets, which is super nice to have.
#### Comparison with Databases
Pig is a data flow language not a declarative programming language. 
- Hive is more like RDBMs than pig. It has a query lang called HiveQL.
- Hive also needs all data to be stored in tables with schema under its management.
#### Pig Latin
Provides a bunch of statement operators! ngl makes it so much easier to do mapreduce.
#### User-Defined Functions
Escape hatch to use your own code in pig.