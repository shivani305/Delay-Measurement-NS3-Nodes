import re

myNodes = {'10.1.1.1': 0,
           '10.1.1.2': 1,
           '10.1.1.3': 2,
           '10.1.1.4': 3,
           '10.1.1.5': 4,
           '10.1.1.6': 5,
           '10.1.1.7': 6,
           '10.1.1.8': 7,
           '10.1.1.9': 8,
           '10.1.1.10': 9,
           '10.1.1.11': 10,
           '10.1.1.12': 11,
           '10.1.1.13': 12,
           '10.1.1.14': 13,
           '10.1.1.15': 14,
           '10.1.1.16': 15,
           '10.1.1.17': 16,
           '10.1.1.18': 17,
           '10.1.1.19': 18,
           '10.1.1.20': 19,
           '10.1.1.21': 20,
           '10.1.1.22': 21,
           '10.1.1.23': 22,
           '10.1.1.24': 23,
           '10.1.1.25': 24}
         #  '10.1.1.255':0           }

transmitter={}
receiver={}


#x=re.compile('hello/id+') is used to find the pattern in string.
#re.findall(x,filename) returns the value of id in list.

def transmit(l):

    ip=re.compile(r'10.1.1.\d+ > 10.1.1.\d+')
    #seqnum=re.compile(r'SeqNumber=\d+')
    #retry=re.compile(r'Retry=(\d+)')
    id = re.compile(r'id (\d+)')
    Node=re.compile(r'NodeList/(\d+)')
    time=re.compile(r't (\d+.\d+)')
    buffertx = re.compile(r'Tx.(.)')
    ####finding patterns
    ipmatch=re.findall(ip,l)
    # seqnummatch=re.findall(seqnum,l)
    # retrymatch=re.findall(retry,l)
    idnum = re.findall(id,l)
    nodenum=re.findall(Node,l)
    timestamp=re.findall(time,l)
    buf=re.findall(buffertx,l)
    founddupkey=0
    try:
        sourceip=ipmatch[0].split(' > ')[0]
        destinationip=ipmatch[0].split(' > ')[1]
        sourcenode=myNodes[sourceip]
        destinationnode=myNodes[destinationip]
        tstream=destinationip+','+sourceip+','+str(idnum[0])
        if int(nodenum[0])==sourcenode:
            if buf == '1':
                for i in transmitter:
                    if i == tstream:
                        founddupkey=1
            if founddupkey is not 1:
                transmitter[tstream]=timestamp
    except:
        #print ('terror')
        pass

    return transmitter


def receive(l):

    ip=re.compile(r'10.1.1.\d+ > 10.1.1.\d+')
    #seqnum=re.compile(r'SeqNumber=\d+')
    Node=re.compile(r'NodeList/(\d+)')
    time=re.compile(r'r (\d+.\d+)')
    ipmatch=re.findall(ip,l)
    #seqnummatch=re.findall(seqnum,l)
    nodenum=re.findall(Node,l)
    timestamp=re.findall(time,l)
    id=re.compile(r'id (\d+)')
    idnum=re.findall(id,l)
    try:

        sourceip=ipmatch[0].split(' > ')[0]
        destinationip=ipmatch[0].split(' > ')[1]
        #sourcenode=myNodes[sourceip]
        destinationnode=myNodes[destinationip]
        tstream=destinationip+','+sourceip+','+str(idnum[0])
        if int(nodenum[0])==destinationnode:
            receiver[tstream]=timestamp
    except:
        #print ('rerror')
        pass



    return receiver

with open('IP_Trace.tr', 'r') as fi:
#with open('Project2_25Nodes_5Pause (1).tr', 'r') as ti:
    for ln in fi:
        if ln.startswith("t "):
            a=transmit(ln)

with open('Project2_25Nodes_5Pause.tr', 'r') as fi:
    for ln in fi:
        if ln.startswith("r "):
            b=receive(ln)

delay=[]
def delay_measure(a,b):

    drop=0
    tx=0
    rx=0
    ad=0.0
    maxdelay=0.0
    for i in a:
        tx=tx+1
        #print(i)
        try:
            d = float(b[i][0])-float(a[i][0])
            if d == 2.1454000000000004 :
                 print(float(b[i][0]))
                 print (float(a[i][0]))
                 print (i)
            delay.append(d)
            ad=float(ad+d)
            rx=rx+1
        except:
            drop+=1
            pass
    maxdelay = max(delay)
    ad = float(ad/rx)
    return tx,rx,drop,ad,maxdelay

#print (a)
#print (b)
print("transmitted packets, received packets, dropped packets, average delay, maximumdelay")
x=delay_measure(a,b)
print (x)


