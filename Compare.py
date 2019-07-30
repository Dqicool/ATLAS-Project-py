# script to display data and MC invariant mass histograms together for comparison
import ROOT as r

# get histograms from files
data = r.TFile("outC/2lep.root")
h_data = data.Get("lep_mass;1")
mc = r.TFile("outC/H_4lep.root")
h_mc = mc.Get("lep_mass;1")
back = r.TFile("outC/H_back.root")
h_back = back.Get("lep_mass;1")

# calculate residuals for data by subtracting background
h_res_data = h_data - h_back

# restyle hists
h_mc.SetFillColorAlpha(r.kTeal+2,0.5)
#h_mc.SetLineColor(r.kTeal+1)
h_back.SetFillColorAlpha(r.kPink-6,0.5)
h_back.SetLineColor(r.kPink-5)

h_res_data.SetLineColor(r.kBlack)

# do fits on residuals
f1 = r.TF1("f1","gaus",110e3,135e3)
h_res_data.Fit("f1","R")
#h_mc.Fit("gaus")

# make canvases
c_compare = r.TCanvas("comparison","comparison")
c_compare.SetFillStyle(4000)
c_residuals = r.TCanvas("residuals","residuals")
c_residuals.SetFillStyle(4000)
r.gStyle.SetOptStat(1111111)

# add histograms to a stack
stack = r.THStack("stack","")
stack.Add(h_back,"HIST")
stack.Add(h_mc,"HIST")

# draw objects on comparison canvas
c_compare.cd()
h_data.Draw()
stack.Draw("SAME NOCLEAR") 

# draw on residuals canvas
c_residuals.cd()
h_res_data.Draw()
h_mc.Draw("SAME")

# output file
outFile = r.TFile("comparison.root","RECREATE")
c_compare.Write()
c_compare.Print("comparison.pdf","pdf")
c_residuals.Write()
c_residuals.Print("residuals.pdf","pdf")
outFile.Close()
