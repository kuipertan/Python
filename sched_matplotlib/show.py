import time,json,getopt,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


day_before = 0
#chan = 'kafka-0.8-dmo'
chan = 'hdfs-mobile'

opts,_ = getopt.getopt(sys.argv[1:], "hd:")
for op,val in opts:
    if op == '-h':
        print "python show.py [-d 0]"
        sys.exit()
    elif op == '-d':
        if val.isdigit():
            day_before = int(val)
        else:
            print "Wrong port number"
            sys.exit()


# evenly sampled time at 200ms intervals
x = []
y = []

x_c = []
y_c = []

metric = 'bytes'

now = time.time()
while day_before:
    day_before -= 1
    gmd = time.gmtime(now)
    now = now - gmd.tm_hour * 3600 - (gmd.tm_min + 1) * 60

print "Show day: ", time.gmtime(now)

last_week_now = now - 7*24*3600
yesterday = now - 24*3600
last_week_yesterday = yesterday - 7*24*3600



fp = None
fp_h = None


# Get last record in yesterday
fn = time.strftime('%Y%m%d', time.gmtime(yesterday))
fn_h = time.strftime('%Y%m%d', time.gmtime(last_week_yesterday))

try:
    fp = open('./history/'+fn, 'r')
    fp_h = open('./history/'+fn_h, 'r')
except Exception, ex:
    print ex

val_y = 0
val_last_week_y = 0

if fp:
    record = fp.read()
    record = json.loads(record)
    try:
        val_y = record[chan][str(1430)][metric]
    except Exception,ex:
        print ex
    finally:
        fp.close()
        fp = None

if fp_h:
    record = fp_h.read()
    record = json.loads(record)
    try:
        val_last_week_y = record[chan][str(1430)][metric]
    except Exception,ex:
        print ex
    finally:
        fp_h.close()
        fp_h = None



# read today
fn = time.strftime('%Y%m%d', time.gmtime(now))
fn_h = time.strftime('%Y%m%d', time.gmtime(last_week_now))

try:
    fp = open('./history/'+fn, 'r')
    fp_h = open('./history/'+fn_h, 'r')
except Exception, ex:
    print ex

if fp:
    rd_s = fp.read()
    rd_s = json.loads(rd_s)
    last = val_y
    last_tm = -10
    try:
        rd_s = rd_s.get(chan)
        if rd_s:
            rds = sorted(rd_s.iteritems(), key=lambda d:int(d[0]), reverse=False)
            for rd in rds:
                if metric in rd[1].keys():
                    x.append(int(rd[0]))
                    if rd[1][metric] < last:
                        last = 0
                    y.append((rd[1][metric] - last)/((int(rd[0]) - last_tm)*60))
                    last_tm = int(rd[0])
                    last = rd[1][metric]

    except Exception,ex:
        print ex
    finally:
        fp.close()

if fp_h:
    rd_s = fp_h.read()
    rd_s = json.loads(rd_s)
    last = val_last_week_y
    last_tm = -10
    try:
        rd_s = rd_s.get(chan)
        if rd_s:
            rds = sorted(rd_s.iteritems(), key=lambda d:int(d[0]), reverse=False)
            for rd in rds:
                if metric in rd[1].keys():
                    x_c.append(int(rd[0]))
                    if rd[1][metric] < last:
                        last = 0
                    y_c.append((rd[1][metric] - last)/((int(rd[0]) - last_tm)*60))
                    last_tm = int(rd[0])
                    last = rd[1][metric]
    except Exception,ex:
        print ex
    finally:
        fp_h.close()


# red dashes, blue squares and green triangles
length = len(x)
    
x = x[1:]
y = y[1:]
x_c = x_c[1:]
y_c = y_c[1:]
fig = plt.figure(1, figsize=(20,8))
splt = plt.subplot(111)
lines = plt.plot(x, y, 'r-', x_c, y_c, 'b-')
lines[0].set_label('Today')
lines[1].set_label('Last week')
plt.setp(lines, linewidth=2.0)
plt.xlabel("Time(minutes from 00:00)")
plt.ylabel("Traffic(Bytes per second)")
xmajorLocator = MultipleLocator(60)
#xmajorFormatter = FormatStrFormatter('%HH')
splt.xaxis.set_major_locator(xmajorLocator)
#splt.xaxis.set_major_formatter(xmajorFormatter)
splt.set_xlim(0,1500)
plt.grid(True)
plt.legend(loc='best')
plt.show()
