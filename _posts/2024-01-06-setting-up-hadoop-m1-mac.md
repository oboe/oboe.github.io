I'd expect it to be no different than instructions, but I'll log any differences here:
https://apache.github.io/hadoop/hadoop-project-dist/hadoop-common/SingleCluster.html

```

brew install hadoop

export JAVA_HOME=$(/usr/libexec/java_home)
// or you can add it to hadoop-env.sh

cd /opt/homebrew/Cellar/hadoop/3.3.6/libexec/etc/hadoop

// update core-site.xml with
<property>
	<name>fs.defaultFS</name>
	<value>hdfs://localhost:9000</value>
</property> 

// update hdfs-site.xml with
<property>
	<name>dfs.replication</name>
	<value>1</value>
</property>

// update mapred-site.xml with
<property>
	<name>mapreduce.framework.name</name>
	<value>yarn</value>
</property>
<property>
	<name>mapreduce.application.classpath</name>
	<value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
</property>

// update yarn-site.xml with
<property>
	<name>yarn.nodemanager.aux-services</name>
	<value>mapreduce_shuffle</value>
</property>
<property>
	<name>yarn.nodemanager.env-whitelist</name>
	<value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
</property>

// Enable System settings -> Sharing -> Remote Login
// And test it out
ssh localhost

// Enable passwordless login
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

// format something
hadoop namenode -format 

// Run everything
./../../sbin/start-all.sh

// check stuff is running
jps
and
http://localhost:9870/

// try stuff!

// and if you want to stop everything
./../../sbin/stop-all.sh


```

