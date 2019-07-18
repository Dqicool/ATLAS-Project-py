import ROOT as r

def DrawC(filename,lumStr,fast):
    """
    Function to load in the C++ code and run it for a given data set
    """

    # reset environment and get path to file
    r.gROOT.Reset()
    path = "/data/OpenData/" + filename 

    # load in CLoop.C
    r.gROOT.ProcessLine(".L CLoop.C")

    # load in tree from file
    r.gROOT.ProcessLine("TFile* f = new TFile(\""+path+"\")")
    r.gROOT.ProcessLine("TTree * minTree = new TTree")
    r.gROOT.ProcessLine("f->GetObject(\"mini\",minTree)")

    # create new instance of CLoop and loop over events
    r.gROOT.ProcessLine("CLoop* t = new CLoop(minTree)")
    r.gROOT.ProcessLine("t->Loop("+lumStr+","+str(fast).lower()+")")
