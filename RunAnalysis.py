# script which runs Draw multiple times for different data sets

import sys
sys.path.insert(0, "backend")

import ROOT as r
import os
from Draw import Draw
from DrawC import DrawC
from infofile import infos
from keyTranslate import keyTranslate
from dataSets import dataSets, totRealLum

langMode = "py" # coding language to use for the analysis script
totalRealLum = 10.064 # total measured integrated luminosity in inverse femtobarns

def runAnalysis(key, fast):
    """
    Function to run the analysis for a given decay chain labelled 'key'
    """
    # get filename
    filename = dataSets[key]

    # get luminosity weight if data is MC
    if key in ("a","b","c","d"):
        lumStr = "1"
    else:
        newKey = keyTranslate[key] # use dataset naming convention of ATLAS

        # calculate luminosity weight
        lumWeight = totalRealLum * 1000 * infos[newKey]["xsec"] / (infos[newKey]["sumw"] *
                infos[newKey]["red_eff"])

        lumStr = "%.5E" % (lumWeight)

    # launch the analysis script for the given data set with the desired language
    if langMode == "C":
        DrawC(filename,lumStr,fast)
    else:
        Draw(filename,lumStr,fast)

def combine(files):
    """
    function to get a list of .root files containing histograms and
    add all the histograms together
    """
    # store histograms from the first section of data in a list
    totHist = []
    sec0 = r.TFile("out"+langMode+"/"+files[0]+fastName+".root") # first file
    key0 = sec0.GetListOfKeys() # first list of keys
    for j in range(len(key0)):
        obj0 = sec0.Get(key0[j].GetName()) # get first object
        if obj0.InheritsFrom("TH1"): # if object is a histogram add it to the list
            totHist.append(obj0)

    # loop over other output files
    for i in range(1,len(files)):
        # read in output file for this section of data
        secFile = r.TFile("out" + langMode + "/" + files[i] + fastName + ".root")
        
        # get histogram keys
        keys = secFile.GetListOfKeys()
        
        # loop over histograms in the file and add them to the total histograms
        for j in range(len(keys)):
            obj = secFile.Get(keys[j].GetName()) # get object
            if obj.InheritsFrom("TH1"): # if object is a histogram add it on
                totHist[j].Add(obj)
    
    # save the combined histograms to a file
    name = "_".join(files) # name of output file
    totFile = r.TFile("out"+langMode+"/"+ name + fastName + ".root","RECREATE")
    for hist in totHist:
        hist.Write()
    totFile.Close()

# get list of decay chains from user
print("Please enter a comma-seperated list of decay chains. Use '+' to add data sets together:")
userInput = input().lower() # get input and remove case-sensitivity
userInput = userInput.replace(" ","") # remove any spaces from list
series = userInput.split(",") # get list of series of chains from string

# new 2d list to hold chains
# first index is series, second is chain in the series
chains = [[]]*len(series)

for i in range(len(series)):
   chains[i] = series[i].split("+") 

# check that all the decay chains are valid
chainsValid = True

for i in range(len(chains)):
    for j in range(len(chains[i])):
        if not (chains[i][j] in dataSets.keys()):
            print("Sorry I don't recognise " + chains[i][j] + " as a valid data set.")
            chainsValid = False

# if all decay chains are valid loop over series 
if chainsValid:

    # detect whether the user wants to run in 'fast' mode for only 1% of data
    answered = False
    while (not answered):
        print("Would you like to run in fast mode to only analyse 1% of data? (yes/no)")
        useFast = input().lower()
        if useFast in "yes":
            answered = True
            fastMode = True
            fastName = "_fast"
        elif useFast in "no":
            answered = True
            fastMode = False
            fastName = ""

    for i in range(len(chains)):

        # loop over chains in the series and run the analysis
        for j in range(len(chains[i])):
            chain = chains[i][j]
            runAnalysis(chain,fastMode)

            # move the output to a different directory
            os.system("mv outfile.root out" + langMode + "/" + chain + fastName + ".root")

        # combine chains in the series if it contains more than one chain
        if (len(chains[i])>1):
            combine(chains[i])
