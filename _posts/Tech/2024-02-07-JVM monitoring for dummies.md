I've always relied on these cool snazzy dashboarding and metric services like Cloudwatch and Grafana to do all the heavy lifting of knowing what the hell is happening to my hosts. Now when I don't have any of these tools setup I'm fucked. This post aims to help make me less fucked.

My high level mental model is that ideally we can solve all our issues at the application level (Java). Before I start having to dip into OS.
## JVM profiling runbook

Basic process
1. Get a heap dump, with `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp`
2. Copy the dump
3. Intellj does have a profiler tool but apparently
4.<<https://www.jetbrains.com/help/idea/2021.2/open-an-external-profiling-report.htm>>


What kind of out of memory error is it?
-<<https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/memleaks002.html>>

## JVM profiling commands

### `jinfo`
What were the system properties?
```
jinfo --pid 12345
```
### `jsnap`
Java metrics and statistics. Like threads started!
### `jps`
What java processes are running?
### `jstack`
Get JVM info, deadlocks and all the thread stacks!
```
jstack --pid 72640
```
### `jmap`

Get a heap dump of a running process.
```
jmap -dump:format=b,file=snapshot.jmap pid
```

Get a heap histogram of a running process. 
```
jmap -histo pid

then

jmap -histo \ /java/re/javase/6/latest/binaries/solaris-sparc/bin/java core.27421
```
### `jstat`
Get JVM stats.
### `jcmd`
Swiss army knife of general tools.
### `jconsole`
GUI for monitoring. Run it with a pid or you need a JMX port.
## More on Java from a person who loves perf
-<<https://www.brendangregg.com/FlameGraphs/cpuflamegraphs.html#Jav>>

## OS profiling
Pretty much theres only a few ways to do this. The main problem is actually reading the information presented. Following the church of brendan gregg, lets use the USE method.
- Whats the utlisation?
- Whats the saturation?
- Whats the errors?

<<https://www.brendangregg.com/USEmethod/use-unix7th.html>>
### `dstat`

### `iostat`

### `iotop`

## Appendix
-<<https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/memleaks004.htm>>
-<<https://talktotheduck.dev/debug-the-jvm-using-jhsd>>
-<<https://spark.apache.org/docs/latest/monitoring.html>>
