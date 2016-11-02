#!/usr/bin/python
from SocketServer import ThreadingMixIn
import os
import datetime

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
 
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler

fn = '/opt/sys/stopwords/StopWords.dic'
 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        if self.path != '/stopwords.dic':
            self.send_error(404, 'File Not Found: %s' % self.path)
            return
        retag = self.headers.getheader('If-None-Match')
        rlm = self.headers.getheader('If-Modified-Since')
        st=os.stat(fn)
        if retag and retag == str(st.st_mtime):
            self.send_response(304)
            self.send_header('Etag',str(st.st_mtime))
            self.send_header('Content-Type',"charset=UTF-8")
            self.end_headers()
            self.wfile.write("Not Modified")
            return
         
        d = datetime.datetime.fromtimestamp(int(st.st_mtime))
        d = d.strftime(GMT_FORMAT)
        if rlm and rlm == d:
            self.send_response(304)
            self.send_header('Last-Modified',d)
            self.send_header('Content-Type',"charset=UTF-8")
            self.end_headers()
            self.wfile.write("Not Modified")
            return

        file_object = open(fn)
        stopwords = None
        try:
            stopwords = file_object.read()
        finally:
            file_object.close()

        self.send_response(200)
        self.send_header('Etag',str(st.st_mtime))
        self.send_header('Last-Modified',d)
        self.send_header('Content-Type',"charset=UTF-8")
        self.send_header('Content-Length',len(stopwords))
        self.end_headers()
        self.wfile.write(stopwords)
 
    def do_HEAD(self):
        if self.path != '/stopwords.dic':
            self.send_error(404, 'File Not Found: %s' % self.path)
            return
        retag = self.headers.getheader('If-None-Match')
        rlm = self.headers.getheader('If-Modified-Since')
        st=os.stat(fn)
        if retag and retag == str(st.st_mtime):
            self.send_response(304)
            self.send_header('Etag',str(st.st_mtime))
            self.send_header('Content-Type',"charset=UTF-8")
            self.end_headers()
            self.wfile.write("Not Modified")
            return
         
        d = datetime.datetime.fromtimestamp(int(st.st_mtime))
        d = d.strftime(GMT_FORMAT)
        if rlm and rlm == d:
            self.send_response(304)
            self.send_header('Last-Modified',d)
            self.send_header('Content-Type',"charset=UTF-8")
            self.end_headers()
            self.wfile.write("Not Modified")
            return

        self.send_response(200)
        self.send_header('Etag',str(st.st_mtime))
        self.send_header('Content-Type',"charset=UTF-8")
        self.send_header('Last-Modified',d)
        self.end_headers()
  
class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    PORT_NUM=3721
    serverAddress=("", PORT_NUM)
    server=ThreadingHttpServer(serverAddress, myHandler)
    #server=HTTPServer(serverAddress, myHandler)
    print 'Started httpserver on port ' , PORT_NUM
    server.serve_forever()

if __name__ == '__main__':
    main()
    
