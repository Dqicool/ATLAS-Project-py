# Analysis.py
# Skeleton code in python provided for you
# In place of this comment you should write [your name] -- [the date] and update it as you go!
# Make sure to make backups and comment as you go along :-)

# allow python to use ROOT
import ROOT as r
import numpy as np
r.gROOT.SetBatch(True)

def Analyse(t: r.TTree, weighting: str):
    r.EnableImplicitMT()
    df = r.RDataFrame(t)
    lumifac = weighting.split("*")[-1]
    r.gInterpreter.Declare("""
    #ifndef __GETWEIGHT_MC__
    #define __GETWEIGHT_MC__
    double getWeightMC(double mc_weight, 
                    double sf_PILEUP,
                    double sf_ELE,
                    double sf_MUON,
                    double sf_PHOTON,
                    double sf_TAU,
                    double sf_BTAG,
                    double sf_LepTRIGGER,
                    double sf_PhotonTRIGGER,
                    double sf_TauTRIGGER,
                    double sf_DiTauTRIGGER,
                    double lumi_factor) {
                return mc_weight * sf_PILEUP * sf_ELE * sf_MUON * 
                sf_PHOTON * sf_TAU * sf_BTAG * sf_LepTRIGGER * 
                sf_PhotonTRIGGER * sf_TauTRIGGER * sf_DiTauTRIGGER * 
                lumi_factor;
    }
    #endif
    """)
    r.gInterpreter.Declare("""
    #ifndef __GETWEIGHT_DATA__
    #define __GETWEIGHT_DATA__
    double getWeightData(){
                return 1;
    }
    #endif
    """)
    if weighting != '1':
        stringGetWeight = "getWeightMC(mcWeight, scaleFactor_PILEUP, scaleFactor_ELE,\
                        scaleFactor_MUON, scaleFactor_PHOTON, scaleFactor_TAU,\
                        scaleFactor_BTAG, scaleFactor_LepTRIGGER, scaleFactor_PhotonTRIGGER,\
                        scaleFactor_TauTRIGGER, scaleFactor_DiTauTRIGGER,"+lumifac+")" 
    else :
        stringGetWeight = "getWeightData()"
    
    ef = df.Define('weight', stringGetWeight)
    h_lep_n = ef.Histo1D(r.RDF.TH1DModel("h_lep_n", "", 6, -0.5, 5.5), 'lep_n', 'weight').GetPtr()

    h_lep_n.Write()

    # # Draw histograms
    # # Format is t.Draw("variable_to_plot >> histogram_name (number_of_bins, x_axis_minimum, x_axis_maximum"),weighting)

    
    # # A couple of simple examples:
    # # 1) Draw a histogram of number of leptons per event.
    # t.Draw("lep_n >> h_lep_n(10, -0.5, 9.5)", weighting)
    # # 2) Draw a histogram of the "lepton type" of every lepton in every event.
    # t.Draw("lep_type >> h_lep_type(10, 7.5, 17.5)", weighting)
    # # Note: lepton type takes the value 11 for electrons and 13 for muons
    

    # # Selection cuts can be used to plot only data that pass certain "selection cuts".
    # # For second argument in t.Draw() use (weighting + "* (selection_cuts)")

    # # For example, plotting transverse momentum of leptons only for events with 3 or more leptons:
    # t.Draw("lep_pt >> h_3lep_pt(200,0,140e3)", weighting + "* (lep_n >= 3)")


    # # It is also possible to plot calculated quantities - here is an example
    # # To make this easier one can use the function SetAlias("name","formula") to perform intermediate calculations

    # # For example, plotting the average transverse momenta of leptons in each event:
    # t.SetAlias("meanPt","Sum$(lep_pt)/Length$(lep_pt)") # define meanPt
    # t.Draw("meanPt >> h_lep_pt_mean(200,0,140e3)", weighting) # plot meanPt
    # # For more information see https://root.cern.ch/doc/master/classTTree.html#a73450649dc6e54b5b94516c468523e45

    
    # # It can be useful to define selection cuts that can take input arguments - here is an example
    
    # # Define selection cuts for each lepton
    # lepCut = "lep_pt[{0}] > 20e3  && lep_type[{0}]=={1}"
    # # Note: here "{0}" and "{1}" are dummy arguments that take the values specified when the function is used, as given below 
    
    # # Require that both leptons [0] and [1] satisfy the specified selection cuts 
    # selCutsE = "(" + lepCut.format(0,11) + "&&" + lepCut.format(1,11) + ")"
    
    # # For events containing two electrons satisfying the specified selection cuts plot the average of the pseudorapidity of the two electrons
    # t.Draw("(lep_eta[0]+lep_eta[1])/2.0 >> h_electron_eta_average(100,-3.0,3.0)", weighting + "*" + selCutsE)


    # # Retrieve the results of drawing the histograms.
    # # This needs to be done for each histogram.
    # h_lep_n = r.gDirectory.Get("h_lep_n")
    # h_lep_type = r.gDirectory.Get("h_lep_type")
    # h_3lep_pt = r.gDirectory.Get("h_3lep_pt")
    # h_lep_pt_mean = r.gDirectory.Get("h_lep_pt_mean")
    # h_electron_eta_average = r.gDirectory.Get("h_electron_eta_average")


    # # Set style of lep_n  histogram.
    # h_lep_n.GetXaxis().SetTitle("Number of leptons per event") # label x axis
    # h_lep_n.GetYaxis().SetTitle("Number of entries/bin") # label y axis
    # h_lep_n.SetTitle("Number of leptons per event")
    # h_lep_n.SetLineColor(r.kRed) # set the line colour to red
    # # For more information on histogram styling see https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html

    # # Note useful trick to get selection cuts used in making a particular histogram written out as a "title" for the histogram
    # h_electron_eta_average.SetTitle(selCutsE)

    

    # # Write histograms to the output file.
    # # This needs to be done for each histogram.
    # h_lep_n.Write()
    # h_lep_type.Write()
    # h_3lep_pt.Write()
    # h_lep_pt_mean.Write()
    # h_electron_eta_average.Write()
