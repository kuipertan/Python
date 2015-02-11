import os
import collect

path = os.path.abspath(os.path.dirname(__file__))

flume = {}
_sources = {
    "hdfs-mobile":{"port":34546, "ips":["10.35.66.41", "10.35.66.42", "10.35.66.43"]},
    "kafka-0.8-dmo":{"port":34546, "ips":["10.35.66.41", "10.35.66.42", "10.35.66.43"]},
}
_interval = 600 #10 minutes

flume["name"] = "flume"
flume["sources"] = _sources
flume["interval"] = _interval # required 
flume["path"] = path + '/history'#  
flume["callback"] = collect.collect
flume["http"] = collect.fetchstatistic

tasks = (flume,)
