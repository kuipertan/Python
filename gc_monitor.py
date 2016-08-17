import os,time,string,sys

last_ygct = 0
last_ygc = 0
last_fgct = 0
last_fgc = 0

f = open('gc.log', 'w')

while True:
    o = os.popen('jstat -gcutil 6040').read()
    u = o.split('\n')
    (S0, S1, E, O, P, YGC, YGCT, FGC, FGCT, GCT) = u[1].split()
    ygct = string.atof(YGCT)
    ygc = string.atof(YGC)
    fgct = string.atof(FGCT)
    fgc = string.atof(FGC)

    if ygc > last_ygc or fgc > last_fgc:
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
        f.write( now + "\n" + o )
        if ygct - last_ygct > 3 or fgct - last_fgct > 2 or ygc-last_ygc > 5:
            f.write( 'Long time gc')
        f.write( '\n\n' )
        f.flush()        

        last_ygc = ygc
        last_ygct = ygct
        last_fgc = fgc
        last_fgct = fgct

    time.sleep(60)
