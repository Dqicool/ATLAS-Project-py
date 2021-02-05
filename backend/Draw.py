# Draw.py
# contains some back-end functionality such as loading in the data and setting weights
import ROOT as r
import time
from os import listdir
from Analysis import Analyse
from dataSets import dirs


def Draw(fileName, lumFactor, fastMode):

    start_time = time.time()  # get start time

    # search through several directories to find where the input file is located
    for path in dirs:
        if fileName in listdir(path):
            correctPath = path
            break

    # open the input data
    openFile = r.TFile(correctPath+fileName, "READ")

    # open output file and canvas
    outFile = r.TFile("outfile.root","RECREATE") # file to write output to
    # canvas = r.TCanvas("Canvas","Canvas") # create a canvas

    # stop the canvas from popping up
    #canvas.GetCanvasImp().UnmapWindow()

    # load the tree
    tree = openFile.Get('mini')

    # if in fast mode use only 1% of the data
    if fastMode:
        nEntries = int(tree.GetEntries()*0.01)
        t = tree.CloneTree(nEntries)
        
    else:
        t = tree
        
    # string holding weight calculation
    # set weight to 1 if data is real, calculate weights otherwise
    if lumFactor == "1":
        weighting = "1"
    else:
        weighting = ("mcWeight*scaleFactor_PILEUP*scaleFactor_ELE*scaleFactor_MUON*"+
                "scaleFactor_PHOTON*scaleFactor_TAU*scaleFactor_BTAG*scaleFactor_LepTRIGGER*"+
                "scaleFactor_PhotonTRIGGER*scaleFactor_TauTRIGGER*scaleFactor_DiTauTRIGGER"+
                "*"+str(lumFactor))

    Analyse(t, weighting)

    # canvas.Close()  # close the canvas

    # delete tree data from output file if present
    if outFile.Get("mini"):
        r.gDirectory.Delete("mini;1")

    outFile.Close() # close output

    # print time taken
    print("%.3f seconds" % (time.time() - start_time))

