# Flume-Data-Ingestion
Here is the .conf file you'd use after setting up flume on your machine.
TwitterAgent.sources = Twitter 
TwitterAgent.channels = MemChannel
TwitterAgent.sinks = HDFS
 
TwitterAgent.sources.Twitter.type = org.apache.flume.source.twitter.TwitterSource
TwitterAgent.sources.Twitter.channels = MemChannel
TwitterAgent.sources.Twitter.consumerKey = <insert your key here>
TwitterAgent.sources.Twitter.consumerSecret = <insert your key here>
TwitterAgent.sources.Twitter.accessToken = <insert your key here>
TwitterAgent.sources.Twitter.accessTokenSecret = <insert your key here>
TwitterAgent.sources.Twitter.keywords = bigdata, Modi, rahul, flume, kafka, hdfs, machine, artificial intelligence, nosql, businessintelligence
 
################## SINK #################################
TwitterAgent.sinks.HDFS.channel = MemChannel
TwitterAgent.sinks.HDFS.type = hdfs
TwitterAgent.sinks.HDFS.hdfs.path = sandbox.hortonworks.com/172.17.0.2(this will be your host IP)/user/flume/tweets
TwitterAgent.sinks.HDFS.hdfs.fileType = DataStream(Makes the imported data readable)
TwitterAgent.sinks.HDFS.hdfs.writeFormat = Text
 
TwitterAgent.sinks.HDFS.hdfs.batchSize = 10
TwitterAgent.sinks.HDFS.hdfs.rollSize = 0
TwitterAgent.sinks.HDFS.hdfs.rollInterval = 600
TwitterAgent.sinks.HDFS.hdfs.rollCount = 10000
 
#################### CHANNEL #########################
TwitterAgent.channels.MemChannel.type = memory
TwitterAgent.channels.MemChannel.capacity = 100
#default - TwitterAgent.channels.MemChannel.capacity = 100
TwitterAgent.channels.MemChannel.transactionCapacity = 100
 
