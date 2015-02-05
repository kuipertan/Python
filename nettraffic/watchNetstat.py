
import commands,time,sys,getopt,re


interval = 1 # second
interface = 'eth0'



def watch_netstat(interval, interface):
    
    cmd = r'ifconfig %s' % interface
    pattern = re.compile(r'RX bytes:(\d+) .+TX bytes:(\d+) .+')

    RX_pre = 0
    TX_pre = 0
    RX_spd = 0
    TX_spd = 0
    while True:
        
        try:
            (code, outtext) = commands.getstatusoutput(cmd)            
            if code != 0:
                print outtext
                sys.exit()

            m = pattern.findall(outtext)
            RX = int(m[0][0])
            TX = int(m[0][1])
            if RX_pre > 0:
                RX_spd = (RX - RX_pre)/interval
                TX_spd = (TX - TX_pre)/interval
                
                print "RX:%d B/S, TX:%d B/S" % (RX_spd, TX_spd)

            RX_pre = RX
            TX_pre = TX
            
            #msg = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(tm1)) 


        except Exception, e:
            print e

        time.sleep(interval)

def usage():
    print "python watchNetstat.py -n 1 -i eth0 \n Means watch eth0 every 1 second"

def main():
    interval = 1
    interface = 'eth0'

    opts,_ = getopt.getopt(sys.argv[1:], "n:i:h")
    for op,val in opts:
        if op == '-i':
            interface = val
        elif op == '-h':
            usage()
            sys.exit()
        elif op == '-n':
            if val.isdigit():
                interval = int(val)
            else:
                print "Wrong interval number"
                sys.exit()

    watch_netstat(interval, interface)

if __name__ == '__main__':
    main()
