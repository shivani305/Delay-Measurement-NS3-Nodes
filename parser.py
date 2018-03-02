import csv


ifile=open('Project2Results.csv','rb')
reader = csv.reader(ifile)
reader.next()
packets=0
for row in reader:
 packets += int(row[2])

print(packets)

