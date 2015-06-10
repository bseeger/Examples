#!/usr/bin/python
# 
# written by Bethany Seeger <bethany@seeger.ws>
# June 6th, 2015
#
# python script that will a CSV file and tally up certain fields. 
# Produces a new CSV file with the prefix "LGF_Tally_"
#
# 

import sys, getopt
import os.path
import glob
from subprocess  import call
from collections import namedtuple


MINUTES_PER_MILE = 15.0

Category = namedtuple('Category', ['mileval', 'minutes', 'index'])
# what index in the incoming array?
WALKING = Category(6, 7, 'WALK')
BIKING = Category(8, 9, 'BIKE')
TEAM = Category(10, 11, 'TEAM')
PLAYGROUND = Category(12, 13, 'PLAY')
INDOOR = Category(14, 15, 'INDOOR')
OUTDOOR = Category(16, 17, 'OUTDOOR')
WATER = Category(18, 19, 'WATER')
WINTER = Category(20, 21, 'WINTER')
CHORE = Category(22, 23, 'CHORE')
PE = Category(24, 25, 'PE')
OTHER = Category(27, 28, 'OTHER') #note that we skipped 26 here!


def usage():
        print "python LeverettGetFit.py -f <CSV file>"
        print "  -f        :  file to do calculations on"
        print "  -h        :  usage message"



def main(argv):

    try:
        opts, args = getopt.getopt(argv, "f:h", ["file="])

    except getopt.GetoptError:
        usage()
        sys.exit(2);

    newfile = "";

    for opt,arg in opts:
        print ("opt is '" + opt + "' and arg is '" + arg + "'")
        if opt in ('-f', '--file'):
            csvfile = arg;
        if opt in ('-h') :
            usage() 
            sys.exit(2)

    if (csvfile == '') :
        usage()
        sys.exit(2)

    newfile = "Calcs-" + csvfile;

    print ("Running calculations on file '" + csvfile + "'")
    origfile = open(csvfile, 'r')
    newfilename = "./LGF_Tally_" + csvfile
    newfile = open(newfilename, 'w')
    
    datadict = {}

    origHeader = origfile.readline().split(',')

    print("File pos is: " + str(origfile.tell()))
   
    line = origfile.readline().strip("\n"); 
    while line != '':
    #for line in origfile:
        data = map(lambda x: x.strip(' ').strip('"'), line.split(','));

        # think tally per student here. They may be in the csv file multiple times
        # note that this might be a staff person's name - the script could get fancy
        # here and look at the column name. 
        studentName = data[4]
        splitname = map(lambda x: x.strip(' '), studentName.split(';'))
        print "studentName: " + studentName
        print  splitname
        if studentName not in datadict:
            print("creating entry for " + studentName)
            datadict[studentName] = {
                'first':splitname[1],
                'last':splitname[0],
                WALKING.index:0.0,
                BIKING.index:0.0,
                TEAM.index:0.0,
                PLAYGROUND.index:0.0,
                INDOOR.index:0.0,
                OUTDOOR.index:0.0,
                WATER.index:0.0,
                WINTER.index:0.0,
                CHORE.index:0.0,
                PE.index:0.0,
                OTHER.index:0.0,
                'total': 0.0
            }

        # can really trim this down to where datadict[studentName]['Total'] is all we need and add on all the mile info to just one number
        # for now leave this as it will help with debugging. 

        #datadict[studentName][WALKING.index] += float(data[WALKING.mileval]) * (float(data[WALKING.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][BIKING.index] += float(data[BIKING.mileval]) * (float(data[BIKING.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][TEAM.index] += float(data[TEAM.mileval]) * (float(data[TEAM.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][PLAYGROUND.index] += float(data[PLAYGROUND.mileval]) * (float(data[PLAYGROUND.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][INDOOR.index] += float(data[INDOOR.mileval]) * (float(data[INDOOR.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][OUTDOOR.index] += float(data[OUTDOOR.mileval]) * (float(data[OUTDOOR.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][WATER.index] += float(data[WATER.mileval]) * (float(data[WATER.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][WINTER.index] += float(data[WINTER.mileval]) * (float(data[WINTER.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][CHORE.index] += float(data[CHORE.mileval]) * (float(data[CHORE.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][PE.index] += float(data[PE.mileval]) * (float(data[PE.minutes]) / MINUTES_PER_MILE)
        #datadict[studentName][OTHER.index] += float(data[OTHER.mileval]) * (float(data[OTHER.minutes]) / MINUTES_PER_MILE)

        #duplicate here -- keep this one ultimately once things check out okay. 
        datadict[studentName]['total'] += float(data[WALKING.mileval]) * (float(data[WALKING.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[BIKING.mileval]) * (float(data[BIKING.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[TEAM.mileval]) * (float(data[TEAM.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[PLAYGROUND.mileval])* (float(data[PLAYGROUND.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[INDOOR.mileval]) * (float(data[INDOOR.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[OUTDOOR.mileval]) * (float(data[OUTDOOR.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[WATER.mileval]) * (float(data[WATER.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[WINTER.mileval]) * (float(data[WINTER.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[CHORE.mileval]) * (float(data[CHORE.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[PE.mileval]) * (float(data[PE.minutes]) / MINUTES_PER_MILE)
        datadict[studentName]['total'] += float(data[OTHER.mileval]) * (float(data[OTHER.minutes]) / MINUTES_PER_MILE)

    
        line = origfile.readline().strip('\n'); 
    

    # phew, done with that. ;) 

    # round it out, now... should this be ceil? 
    for studentName in datadict: 
        datadict[studentName]['total'] = round(datadict[studentName]['total'])

    # Now write the new file ------------------------
    newfile.write('"student","total miles"\n')

    # sort by the funky key (lastname; firstname)
    students = sorted(datadict.keys())

    for student in students:
        # print using the split out first name and last name. 
        newfile.write('"' + datadict[student]['first'] + " " + datadict[student]['last'] + '":"' + str(datadict[student]['total']) + ' miles"\n');

    # done writing file ------------------------------

    # Now close the new file
    newfile.close()
    origfile.close()
     
    print ("Finished running calculations.  Created file: " + newfilename + "'");

if __name__ == "__main__":
    main(sys.argv[1:])

