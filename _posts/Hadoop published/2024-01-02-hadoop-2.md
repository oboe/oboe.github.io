Today we're having a look at MapReduce a programming model you can use on Hadoop!

Demo
1. Input: (A,B,C,1), (A,B,C,2)
2. Map, to get values
3. (B,1),(B,2),(B,3)
4. Shuffle these mapped values
5. (B, [1,2,3])
6. Reduce
7. Output: (B,3)

If feels like the shuffle step is very hard. How does Hadoop get the right data to the right machines? Is it just hashed? I'm not too sure. 🤔

`hadoop MyClass input.txt outputdir` command runs Hadoop.
- output dir cannot exist before running job
- `HADOOP_CLASSPATH` env var can be used to add application classes to classpath

1. Hadoop tries its best to run a map on a node where input data resides in
2. Map tasks write to local disk not to HDFS, as map output is just intermediate output
3. All this intermediate output is sent to the reduce task
4. Reduce task write to HDFS

You can optionally have a combiner function that combines map outputs. For example you could find the max temperature for the map output of a single split. Combine functions are not guaranteed to be ran. And they can save a lot of unnecessary data transfer!

The other way you can use Hadoop is with streaming scripts! All you need to provide is a mapper and reducer program that eats from stdin and outputs to stdout! You can simply test it with unix pipes for sanity checks. Thats pretty beautiful!