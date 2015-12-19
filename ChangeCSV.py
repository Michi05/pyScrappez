import csv
import re

def countLabelsInPos(p):
        with open('MovieFileFiltered.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                label_counter = {}
                for row in spamreader:
                        if row[p] in label_counter:
                                label_counter[row[p]] += 1
                        else:
                                label_counter[row[p]] = 1
                        
                for i in sorted(label_counter.keys()):
                        print(i + ": " + str(label_counter[i]))

#def changeStuff():

def noIniZero(theString):
        while(theString != "" and theString[0] == "0"):
                theString = theString[1:]
        return theString

def trimCol(c):
        with open('MovieFileFiltered.csv', newline='') as fInput:
                fReader = csv.reader(fInput, delimiter=',', quotechar='"')
                with open('movieList2nd.csv', 'w', newline='') as fOutput:
                        fWriter = csv.writer(fOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for row in fReader:
                                row[c] = noIniZero("".join(row[c].split()))
                                fWriter.writerow(row)

def formatDate(c):
        with open('MovieFileFiltered.csv', newline='') as fInput:
                fReader = csv.reader(fInput, delimiter=',', quotechar='"')
                with open('movieList2nd.csv', 'w', newline='') as fOutput:
                        fWriter = csv.writer(fOutput, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for row in fReader:
                                row[c] = row[c].lower()
                                yearList = re.findall(r"[0-9]{4,4}", row[c])
                                monthList = re.findall(r"[a-z]{3,10}", row[c])
                                if len(yearList) > 0:
                                        row[c] = yearList[0]
                                else:
                                        row[c] = ""
                                if len(yearList) > 1:
                                        print(yearList + " matches in: " + row[0])
                                if len(monthList) > 0:
                                        row[c] = row[c] + monthList[0]
                                fWriter.writerow(row)
    

formatDate(1)
#trimCol(4)
#countLabelsInPos(3)

