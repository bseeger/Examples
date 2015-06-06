#/bin/python
# 
# written by Bethany Seeger <bseeger.cs.umass.edu>
# April 29th, 2015
#
# python script that will a CSV file and tally up certain fields. 
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
        print "LES_FitCalculator -f <CSV file>"
        print "  -f        :  file to do calculations on"
        print "  -h        :  usage message"

#
#    fileobj = open(directory + tmpfile, 'w')
#                print(pstotext + " " + filename + " > " + filename_pstotext);
#
#            fileobj.write(os.path.abspath(filename_pstotext) + " -> " + os.path.abspath(filename) + ".meta.xml\n");
#            num_files += 1
#    fileobj.close()
#    while (fileobj.closed != True) :
#        print("File obj not closed yet");
#    return num_files
#
#    os.chdir(origdir);
#

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
    newfilename = "./New" + csvfile
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

        if studentName not in datadict:
            print("creating entry for " + studentName)
            datadict[studentName] = {
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


        datadict[studentName][WALKING.index] += float(data[WALKING.mileval]) * (float(data[WALKING.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][BIKING.index] += float(data[BIKING.mileval]) * (float(data[BIKING.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][TEAM.index] += float(data[TEAM.mileval]) * (float(data[TEAM.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][PLAYGROUND.index] += float(data[PLAYGROUND.mileval]) * (float(data[PLAYGROUND.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][INDOOR.index] += float(data[INDOOR.mileval]) * (float(data[INDOOR.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][OUTDOOR.index] += float(data[OUTDOOR.mileval]) * (float(data[OUTDOOR.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][WATER.index] += float(data[WATER.mileval]) * (float(data[WATER.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][WINTER.index] += float(data[WINTER.mileval]) * (float(data[WINTER.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][CHORE.index] += float(data[CHORE.mileval]) * (float(data[CHORE.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][PE.index] += float(data[PE.mileval]) * (float(data[PE.minutes]) / MINUTES_PER_MILE)
        datadict[studentName][OTHER.index] += float(data[OTHER.mileval]) * (float(data[OTHER.minutes]) / MINUTES_PER_MILE)

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
    
    # phew, done with that. ;) Now write the new file 

    for studentName in datadict: 
        datadict[studentName]['total'] = round(datadict[studentName]['total'])

    newfile.write('"student","total miles"\n')

    # sort doesn't do what i think it does
    students = datadict.keys()

    for student in students:
        newfile.write('"' + student + '","' + str(datadict[student]['total']) + '"\n');

    # voila, new file created. Now close it. 
    newfile.close()
    origfile.close()
     


#
#    fileobj = open(directory + tmpfile, 'w')
#                print(pstotext + " " + filename + " > " + filename_pstotext);
#
#            fileobj.write(os.path.abspath(filename_pstotext) + " -> " + os.path.abspath(filename) + ".meta.xml\n");
#            num_files += 1
#    fileobj.close()
#    while (fileobj.closed != True) :
#        print("File obj not closed yet");
#    return num_files
#
#    os.chdir(origdir);
#

    print ("Finished running calculations.  Created file: " + newfilename + "'");


if __name__ == "__main__":
    main(sys.argv[1:])

