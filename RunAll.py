# script which runs Draw on ALL datasets in fast mode

import sys
sys.path.insert(0, "backend") # allow code to be imported from subdirectory

import ROOT as r
import os
from Draw import Draw
from DrawC import DrawC
from infofile import infos
from keyTranslate import keyTranslate
from dataSets import dataSets, totRealLum, realList

langMode = "py" # coding language to use for the analysis script
#totalRealLum = 10.064 # total measured integrated luminosity in inverse femtobarns

def runAnalysis(key, fast):
    """
    Function to run the analysis for a given decay chain labelled 'key'
    """
    # get filename
    filename = dataSets[key]

    # get luminosity weight if data is MC
    if key in realList:
        lumStr = "1"
    else:
        # calculate luminosity weight
        # if it does not work try again without "_1lep" or "_2lep" suffix for key
        try:
            lumWeight = totRealLum * 1000 * infos[key]["xsec"] / (infos[key]["sumw"] *
                infos[key]["red_eff"])
        except KeyError:
            shortKey = key[:-5]
            lumWeight = (totRealLum * 1000 * infos[shortKey]["xsec"] /
                (infos[shortKey]["sumw"] * infos[shortKey]["red_eff"]))

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

for dataKey in dataSets.keys():
    print(dataKey)
    runAnalysis(dataKey,True)