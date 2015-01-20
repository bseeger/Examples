#/bin/python
# 
# written by Bethany Seeger <bseeger.cs.umass.edu>
# July 2, 2014
#
# python script that will process all pdf files in a specified directory
# It will run them first through pstotext and then metatagger
# The end result will be two extra files per pdf, like this: 
#
#  00007BF8CD3BCA7EB1F474EB124A06714A36EE3F.pdf   <-- input
#  00007BF8CD3BCA7EB1F474EB124A06714A36EE3F.pdf.meta.xml
#  00007BF8CD3BCA7EB1F474EB124A06714A36EE3F.pdf.pstotext.xml
# 


import sys, getopt
import os.path
import glob
from subprocess  import call

# location of pstotext and metatagger exe's
pstotext = "/Users/bseeger/Projects/rexa-workspace/rexa1-pstotext/bin/pstotext"
metatagger_dir = "/Users/bseeger/Projects/rexa-workspace/rexa1-metatagger/"
metatagger = metatagger_dir + "/bin/runcrf"
inst_dict = "/Users/bseeger/Projects/UniversityParser/University.dict"
# AEI = Author Email Institution 
analyzeAEI_dir = "/Users/bseeger/Projects/rexa-workspace/rexa1-metatagger/"
analyzeAEI = analyzeAEI_dir + "bin/runAnalyze"

csvAuthorEmail = "/Users/bseeger/Projects/dataset/goodfiles/dataset_AuthorEmailInst.csv";
csvCitation = "/Users/bseeger/Projects/dataset/anyfiles/dataset.csv"

tmpfile = "PDFtoText.tmp"

def usage():
        print "PdftoXML -d <directory> -s <step>"
        print "  -d --dir  :  directory where PDF files are located"
        print "  -f        :  where to put the analysis's output "
        print "               default: whatever -d dir is with Analysis.txt tacked on end"
        print "  -s --step :  skip to a starting at a specific step [1,2,3] default 1"
        print "               1  is pstotext"
        print "               2  is metatagger" 
        print "               3  is analyze results"
        print "  -h        :  usage message"


def step1_pstotext(directory):
    fileobj = open(directory + tmpfile, 'w')
    num_files = 0
    print ("---- pstotext ----");
    if directory != '':
        #filename will contain path
        for filename in glob.glob(os.path.join(directory, '*.pdf')):
            print ("Processing file '" + filename + "'");

            filename_pstotext = filename + ".pstotext.xml"

            print(pstotext + " " + filename + " > " + filename_pstotext);
            with open (filename_pstotext, 'w') as outfile:
                call([pstotext, filename], stdout=outfile)

            print ("Finished processing file '" + filename + "'");
            fileobj.write(os.path.abspath(filename_pstotext) + " -> " + os.path.abspath(filename) + ".meta.xml\n");
            num_files += 1
    fileobj.close()
    while (fileobj.closed != True) :
        print("File obj not closed yet");
    return num_files


def step2_metatagger(directory) :
    # Now run metatager on the entire newly created dataset, versus one file at a time. More efficient use
    # of resourses that way, since metatagger has a large setup cost. 
    # First, switch to metatagger dir so sbt dependencies work. 
    origdir = os.getcwd()
    os.chdir(metatagger_dir)

    print ("---- metatagger ----");
    print ("directory: " + tmpfile)
    with open (directory + tmpfile, 'r') as infile:
        call([metatagger], stdin=infile)

    os.chdir(origdir);

def step3_analyzeAEI(directory, csvFile, outfile) :
    success = 0;
    failure = 0;
    origdir = os.getcwd()
    os.chdir(analyzeAEI_dir)
    num_files = 0

    print ("---- Analyzing Author/Email/Institution Tagging ----");
    retval = call([analyzeAEI, "-d", directory, "-a", csvAuthorEmail, "-c", csvCitation, "-f", outfile]);

    os.chdir(origdir)

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "d:f:hr:s:", ["dir=","step="])

    except getopt.GetoptError:
        usage()
        sys.exit(2);

    directory = ''
    num_files = 0
    skipto = 1
    csvFile = ''
    analysisFile = ''

    for opt,arg in opts:
        print ("opt is '" + opt + "' and arg is '" + arg + "'")
        if opt in ('-d', '--dir'):
            directory = arg;
        if opt in ('-r') : 
            csvFile = arg;
        if opt in ('-f') : 
            analysisFile = arg;
        if opt in ('-h') :
            usage() 
            sys.exit(2)
        if opt in ('-s', '--step'):
            skipto = int(arg)

    if (directory == '') :
        usage()
        sys.exit(2)


    if (skipto in (1,2,3) == False) :
        print ("Invalid skip request: " + str(skipto));
        usage()
        sys.exit(2)

    print ("Examining directory '" + directory + "'")
    print ("Starting with Step " + str(skipto))

    # unix only right now.     
    directory = os.path.abspath(directory); 

    if (not directory.endswith('/')) :
        directory += '/'

    print ("directory is " + directory)

    if (analysisFile == '') : 
        analysisFile = directory + "Analysis.txt"

    # This does not handle the directory equalling "." right now. Sigh. 

    pstotext_num = 0
    successes = 0
    failures = 0

    # STEP ONE
    if (skipto == 1) :
        pstotext_num = step1_pstotext(directory)  

    # now run meta tagger and parser on things. 
    if (os.path.isfile(directory + tmpfile)) :

        # STEP TWO
        if (skipto <= 2) :
            step2_metatagger(directory)

        # STEP THREE
        if (skipto <= 3) :
            step3_analyzeAEI(directory, csvFile, analysisFile)

    #todo - delete the tmp file, but not really necessary right now and kinda useful to see. 
    print ("Processing complete. Processed files in directory " + directory)    
    print ("\tpstotext: " + str(pstotext_num))
    print("\tNumber of metatagger files parsed:")
    call(["wc", "-l", directory+tmpfile])


if __name__ == "__main__":
    main(sys.argv[1:])

