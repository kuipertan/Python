import time,httplib,json


def getfile(path,tm, mode):
    fn = time.strftime('%Y%m%d', time.gmtime(tm))
    try:
        fn = path + "/" + fn
        fp = open(fn, mode)
    except Exception,e:
        return None 
    return fp

def collect(*args):
    print "collect"
    now = time.time()
    sources = args[0]["sources"]

    fp = getfile(args[0]["path"], now, 'a+')
    if fp == None:
        return
    record = fp.read()
    if len(record):
        record = json.loads(record)
    else:
        record = {}

    for key in sources:
        port = sources[key]["port"]
        total = 0
        for ip in sources[key]["ips"]:
            total += fetchmetric(key,ip,port, "bytes")
                    
        storemetric(key, now, args[0]["interval"], "bytes", total, record)

    fp.truncate(0)
    fp.write(json.dumps(record))
    fp.close()

def fetchmetric(chan, ip, port, metric):
    try:
        h = httplib.HTTPConnection(ip, port, timeout=5)
        h.request('GET', r'/metrics/'+ chan + r'/' + metric)
        val = h.getresponse()
        val = int(val.read())
    except Exception,e:
        val = 0
        
    return val
"""
{
hdfs-mobile:{10:{bytes:1024, events:32}},
}
"""
def storemetric(chan, tm, interval, metric, val, record):
    tmkey = tm2tmkey(tm, interval)
    if chan in record.keys():
        if tmkey in record[chan].keys():
            record[chan][tmkey][metric] = val
        else:
            record[chan][tmkey] = {}
            record[chan][tmkey][metric] = val 
    else:
        record[chan] = {}
        record[chan][tmkey] = {}
        record[chan][tmkey][metric] = val

def tm2tmkey(tm, interval):
    interval /= 60
    _,_,_,h,m,_,_,_,_ = time.gmtime(tm)
    return (h * 60 + m) / interval * interval

def fetchstatistic(flume, *args):
    tm = time.time()

    count_now, count_pre = fetchcount(tm, flume, *args)
    count_10, count_10_pre = fetchcount(tm - 10*60, flume, *args)
    if count_10 > count_now:
        count_10 = 0
    if count_10_pre > count_pre:
        count_10_pre = 0

    return (count_now - count_10 + count_10_pre - count_pre) / (10 * 60)
        
def fetchcount(tm, flume, *args):
    chan = args[0]
    metric = args[1]
    tmkey = str(tm2tmkey(tm, flume['interval']))
    fn = getfile(flume['path'], tm, 'r')
    fn_h = getfile(flume['path'], tm - (7*24*3600), 'r') # last week
    val = 0
    val_h = 0

    if not fn is None:
        try:
            record = fn.read()
            record = json.loads(record)
            val = record[chan][tmkey][metric]
        except Exception, ex:
            print "Exception when read val"
            print ex
        finally:
            fn.close()
            
    if not fn_h is None:
        try:
            record = fn_h.read()
            record = json.loads(record)
            val_h = record[chan][tmkey][metric]
        except Exception, ex:
            print "Exception when read val"
            print ex
        finally:
            fn_h.close()

    return (val, val_h)

