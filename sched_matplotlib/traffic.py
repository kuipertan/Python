from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import sys,signal,struct,json,threading,traceback,urlparse,getopt,os
from scheduler import Scheduler
from config import *
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

log = open(path+'/log', 'w')
sys.stdout = log

port = 10000
serv = None
stop_thd = None
thds = []  

def siginthandler(signum, frame):
        stop_thd = threading.Thread(target=stopall)
        stop_thd.start()

signal.signal(signal.SIGINT, siginthandler)


class TrafficRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:  
			parsed_path = urlparse.urlparse(self.path).path  
			parsed_path = parsed_path.strip('/')
                        eles = parsed_path.split('/')
                        if len(eles) > 3 and eles[0] == 'diff':
                                task_name = eles[1]
                                sub_task = eles[2]
                                metric = eles[3]
                                val = 0
                                for t in tasks:
                                        if t['name'] == task_name:
                                                val = t['http'](t, sub_task, metric) 
                                                break;
                                self.send_response(200)
                                self.end_headers()
                                self.wfile.write('diff=' + str(val))
                        else:
                                self.send_response(404)  
                                self.end_headers()  
                                self.wfile.write('Check your request path')    
		except:  
			traceback.print_exc()  

				
class ThreadingTcpServer(ThreadingMixIn, HTTPServer):pass

class ScheduleTask(threading.Thread):
	def setconfig(self, cfg):
		self.cfg = cfg

	def run(self):
		self.s = Scheduler(self.cfg["name"], self.cfg["interval"],self.cfg["callback"],self.cfg)
		self.s.run()
        def cancel(self):
                self.s.cancel()


def usage():
	print """Usage: traffic.py [-f ] [-p port] 
 e.g. traffic -p 8080
Without -p xxx ,it uses port 10000 defaultly."""


def startwork():
	global thds
	for t in tasks:
                st = ScheduleTask()
                st.setconfig(t)
		thds.append(st)
	for td in thds:
		td.start()
	

def stopwork():
	for td in thds:
		td.cancel()
                print "cancel returned"
        for td in thds:
                td.join()
                print "stopwork join returned"

def stopall():
        stopwork()
        print "stopall to shutdown"
        serv.shutdown()

if __name__ == "__main__":
	
	opts,_ = getopt.getopt(sys.argv[1:], "hp:")
	for op,val in opts:
		if op == '-h':
			usage()
			sys.exit()
		elif op == '-p':
			if val.isdigit():
				port = int(val)
			else:
				print "Wrong port number"
				sys.exit()

        
	global serv
	#serv = ThreadingTcpServer(("", port), TrafficRequestHandler)
	serv = HTTPServer(("", port), TrafficRequestHandler)
	serv.allow_reuse_address = True
	
	startwork()
	serv.serve_forever()
        if stop_thd:
                stop_thd.join()
        print "Main exits."
        
        #debug
        #import collect
        #collect.collect(tasks[0])
        #collect.fetchstatistic(flume, 'hdfs-mobile', 'bytes')

