# Analysis.py
import ROOT as r

def Analyse(t,weighting):

    # Draw histograms
    # Format is t.Draw("variable_to_plot >> histogram_name (number_of_bins, x_axis_minimum, x_axis_maximum"),weighting)

    # Draw a histogram of number of leptons per event.
    t.Draw("lep_n >> h_lep_n(10, 0, 8)", weighting)
    
    # histogram of ptcone/pt
    t.Draw("lep_ptcone30/lep_pt >> h_lep_ptnorm(100,-0.1,0.3)",weighting)

    # histogram of etcone/pt
    t.Draw("lep_etcone20/lep_pt >> h_lep_etnorm(100,-0.1,0.3)",weighting)

    # Selection cuts can be used to only plot data which passes certain tests.
    # For second argument in t.Draw() use (weighting + "* (selection_cuts)")

    # For example plotting transverse momentum of leptons for events with 3 or more leptons only:
    t.Draw("lep_pt >> h_3lep_pt(200,0,140e3)", weighting + "* (lep_n >= 3)")


    # It is also possible to plot calculated quantities.
    # To make this easier one can use the function SetAlias("name","formula") to perform intermediate calculations
    # For example plotting the average transverse momenta of leptons in each event:
    t.SetAlias("meanPt","Sum$(lep_pt)/Length$(lep_pt)") # define meanPt
    t.Draw("meanPt >> h_lep_pt_mean(200,0,140e3)", weighting) # plot meanPt
    # For more information see https://root.cern.ch/doc/master/classTTree.html#a73450649dc6e54b5b94516c468523e45


    # Retrieve the results of drawing histograms.
    # This needs to be done for each histogram.
    h_lep_n = r.gDirectory.Get("h_lep_n")
    h_3lep_pt = r.gDirectory.Get("h_3lep_pt")
    h_lep_pt_mean = r.gDirectory.Get("h_lep_pt_mean")
    h_lep_ptnorm = r.gDirectory.Get("h_lep_ptnorm")
    h_lep_etnorm = r.gDirectory.Get("h_lep_etnorm")


    # Set style of lep_n  histogram.
    h_lep_n.GetXaxis().SetTitle("Number of leptons per event") # label x axis
    h_lep_n.GetYaxis().SetTitle("Number of entries") # label y axis
    h_lep_n.SetTitle("Leptons per event")
    h_lep_n.SetLineColor(r.kRed) # set the line colour to red
    # for more information on histogram styling see https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html


    # Write histograms to the output file.
    # This needs to be done for each histogram.
    h_lep_n.Write()
    h_3lep_pt.Write()
    h_lep_pt_mean.Write()
    h_lep_ptnorm.Write()
    h_lep_etnorm.Write()
