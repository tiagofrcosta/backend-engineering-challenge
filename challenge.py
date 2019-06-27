"""challenge

Usage:
    challenge.py --help | -h
    challenge.py (--input=<file>| -i=<file>)
    challenge.py (--input=<file>| -i=<file>) (--output=<Out_file>|-o=<Out_file>)
    challenge.py (--input=<file>| -i=<file>) (-w <size>|--window <size>) (--output=<Out_file>|-o=<Out_file>)


Options:
    -h --help       Show this screen.
    -i <file>, --input <file>   File to pass
    -o <Out_file>, --output <Out_file>  Destination File [default: ./test.txt] 
    -w <size>, --window <size>   Define the size of the window [default: 10]
    

"""
from docopt import docopt
from datetime import datetime, timedelta
import json

#Reads the JSon file into a list of dictionarys
def readInput(file):
    with open(file,'r') as ifile:
        iptData=[json.loads(line) for line in ifile]
    return iptData

#Writes teh data into the JSON file
def writeOutput(optData, file):
    with open (file,'w') as outfile:
        json.dump(optData,outfile)

# Converts from timestamp to datetime
def convertTime (iptData):
    for i in range(len(iptData)):
        dateCoverter=datetime.strptime(iptData[i]["timestamp"],'%Y-%m-%d %H:%M:%S.%f')
        iptData[i]["timestamp"]=dateCoverter
    return iptData

def calculateMovingAverage(iptData,timeWindow,topLimit):
    tempList=[]
    for i in iptData:
        if i['timestamp']>topLimit-timedelta(minutes=timeWindow) and i['timestamp']<=topLimit:
            tempList.append(i["duration"])
    
    if not tempList:
        return 0
    average=sum(tempList)/len(tempList)
    return average

def challenge(arguments):

    iptData=readInput(arguments["--input"])
    iptData=convertTime(iptData)
    
    minDates=min([i['timestamp'] for i in iptData]) 
    # maxDates=max([i['timestamp'] for i in iptData]) +timedelta(minutes=1) #Increase the value by 1 so it counts the last minute
    #Maximum Date should be the minimum date present on the input plus the window.
    maxDates=minDates+timedelta(minutes=int(arguments["--window"]))
    
    outData=[]
	#Loop through the timespan and for each minute and calculate the averages
    date= minDates.replace(second=0, microsecond=0)
    while date <= maxDates:
    	avg = calculateMovingAverage(iptData, int(arguments["--window"]), date)
    	outData.append({"date": date.strftime('%Y-%m-%d %H:%M:%S'), "average_delivery_time":'%g'%(avg)})
    	date += timedelta(minutes=1)

    # print(outData)
    writeOutput(outData,arguments["--output"])

if __name__ == "__main__":
    arguments=docopt(__doc__)
    challenge(arguments)
