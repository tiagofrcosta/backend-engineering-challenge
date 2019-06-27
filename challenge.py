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

#Writes the data into the JSON file
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
    #For every entry in the data check if the entry is inside the time window, if so append the duration of the data transmission to a temporary list
    for i in iptData:
        if i['timestamp']>topLimit-timedelta(minutes=timeWindow) and i['timestamp']<=topLimit:
            tempList.append(i["duration"])
    
    #Check if the list is empty, this should be the case for the first minute.
    if len(tempList)==0:
        return 0

    #Simple moving average, is the sum of the durations divided by the number of entries
    average=sum(tempList)/len(tempList)
    return average

def challenge(arguments):

    #Data treatment operations
    iptData=readInput(arguments["--input"])
    iptData=convertTime(iptData)
    
    #Finds the minimum data from the collection, this marks the start of the cycle to calculate the Moving Average
    minDates=min([i['timestamp'] for i in iptData]) 


    #Maximum Date should be the minimum date present on the input plus the window.
    maxDates=minDates+timedelta(minutes=int(arguments["--window"]))
   
    outData=[]

	#Set the seconds and microsenconds to zero in order to count the MA for a full lenght of a minute
    date= minDates.replace(second=0, microsecond=0)
    
    #Go through the dates starting with the lowest one till the highest one.
    while date <= maxDates:
    	avg = calculateMovingAverage(iptData, int(arguments["--window"]), date)
    	outData.append({"date": date.strftime('%Y-%m-%d %H:%M:%S'), "average_delivery_time":'%g'%(avg)})
    	date += timedelta(minutes=1)

    # print(outData)
    #Print data to the exit file
    writeOutput(outData,arguments["--output"])

if __name__ == "__main__":
    arguments=docopt(__doc__)
    challenge(arguments)
