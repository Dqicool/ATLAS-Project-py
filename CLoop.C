
#define CLoop_cxx
#include "CLoop.h"
#include <TH2.h>
#include <TCanvas.h>
#include <iostream>
#include <vector>
#include <time.h>
#include <math.h>

bool CLoop::Paired(int l0, int l1)
{
    // check if two leptons form a same-flavour, opposite-charge pair
    if (lep_type->at(l0) == lep_type->at(l1)
    and lep_charge->at(l0) == -lep_charge->at(l1)) 
    return true;
    else return false;
}

bool CLoop::Isolated(int l)
{
    // check if lepton l passes the isolation selection cuts
    if (lep_pt->at(l)>20e3 and lep_etcone20->at(l)<20e3 and lep_ptcone30->at(l)<20e3)
    return true;
    else return false;
}

void CLoop::Style(TH1F *hist, const char* xaxis, const char* yaxis) {
    // set the style of the histograms
    hist->GetXaxis()->SetTitle(xaxis);
    hist->GetYaxis()->SetTitle(yaxis);
    hist->SetLineColor(kBlue-4);
    hist->SetFillColor(kBlue-6);
}

void CLoop::Loop(double lumFactor, bool fastMode)
{
//    In a ROOT session, you can do:
//        root> .L CLoop.C
//        root> CLoop t
//        root> t.GetEntry(12); // Fill t data members with entry number 12
//        root> t.Show();         // Show values of entry 12
//        root> t.Show(16);      // Read and show values of entry 16
//        root> t.Loop();         // Loop on all entries
//

//      This is the loop skeleton where:
//     jentry is the global entry number in the chain
//     ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//     jentry for TChain::GetEntry
//     ientry for TTree::GetEntry and TBranch::GetEntry
//
//         To read only selected branches, Insert statements like:
// METHOD1:
//     fChain->SetBranchStatus("*",0);  // disable all branches
//     fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//     fChain->GetEntry(jentry);         //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch

    clock_t startTime = clock(); // get start time

    if (fChain == 0) return;

    // read only certain branches
    /*
    fChain->SetBranchStatus("*",0);
    fChain->SetBranchStatus("lep_n",1);
    fChain->SetBranchStatus("lep_type",1);
    fChain->SetBranchStatus("lep_pt",1);
    fChain->SetBranchStatus("lep_eta",1);
    fChain->SetBranchStatus("lep_phi",1);
    fChain->SetBranchStatus("lep_E",1);
    fChain->SetBranchStatus("lep_ptcone30",1);
    fChain->SetBranchStatus("lep_etcone20",1);
    fChain->SetBranchStatus("mcWeight",1);
    fChain->SetBranchStatus("scaleFactor_PILEUP",1);
    fChain->SetBranchStatus("scaleFactor_ELE",1);
    fChain->SetBranchStatus("scaleFactor_PHOTON",1);
    fChain->SetBranchStatus("scaleFactor_TAU",1);
    fChain->SetBranchStatus("scaleFactor_BTAG",1);
    fChain->SetBranchStatus("scaleFactor_LepTRIGGER",1);
    fChain->SetBranchStatus("scaleFactor_PhotonTRIGGER",1);
    fChain->SetBranchStatus("scaleFactor_TauTRIGGER",1);
    fChain->SetBranchStatus("scaleFactor_DiTauTRIGGER",1);
    //fChain->SetBranchStatus("met_et",1);
    */

    // book histograms
    TH1F * h_lep_n = new TH1F("lep_n","Number of leptons",10,-0.5,9.5);
    TH1F * h_lep_type = new TH1F("lep_type","Type of leptons",10,10.5,20.5);
    TH1F * h_lep_charge = new TH1F("lep_charge","Charge of leptons",10,-1.5,1.5);
    TH1F * h_lep_mass = new TH1F("lep_mass","Invariant mass of leptons",200,4e4,14e4);
    TH1F * h_lep_pt = new TH1F("lep_pt","Transverse momentum of leptons",200,0,14e4);
    TH1F * h_lep_ptcone = new TH1F("lep_ptcone30","ptcone30 of leptons",200,9e2,3e3);
    TH1F * h_lep_etcone = new TH1F("lep_etcone20","etcone20 of leptons",200,-3e3,7e3);

    Long64_t nentries = fChain->GetEntriesFast();

    // if in fast mode only loop over 1% of the entries
    Long64_t nLoop = nentries;
    if (fastMode) nLoop = nentries * 0.01;

    Long64_t nbytes = 0, nb = 0;

    // loop over number of entries
    for (Long64_t jentry=0; jentry<nLoop;jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;
        nb = fChain->GetEntry(jentry);    nbytes += nb;
        // if (Cut(ientry) < 0) continue;
        
        // calculate event weight
        double weight = 1;

        // check if event is from real data
        if (mcWeight != 0) {
            // take product of all scale factors
            weight = mcWeight*scaleFactor_PILEUP*scaleFactor_ELE*scaleFactor_MUON*
                scaleFactor_PHOTON*scaleFactor_TAU*scaleFactor_BTAG*scaleFactor_LepTRIGGER*
                scaleFactor_PhotonTRIGGER*scaleFactor_TauTRIGGER*scaleFactor_DiTauTRIGGER*lumFactor;
        }

        // fill lepton number histogram
        h_lep_n -> Fill(lep_n);
        
        // varaiables to hold leading and subleading pt values
        double leadpt = 0;
        double subLeadpt = 0;
        int leadLep = 0;
        int subLeadLep = 0;

        // loop over leptons in event
        for (size_t ilep=0; ilep<lep_type->size(); ilep++) {
            h_lep_type -> Fill(lep_type->at(ilep));
            h_lep_charge -> Fill(lep_charge->at(ilep)); // fill lepton charge
            h_lep_pt -> Fill(lep_pt->at(ilep)); // fill lepton transverse momentum
            h_lep_etcone -> Fill(lep_etcone20->at(ilep)); // fill lepton etcone20
            h_lep_ptcone -> Fill(lep_ptcone30->at(ilep)); // fill lepton ptcone30

            // update leading and subleading leptons
            if (lep_pt->at(ilep) > leadpt){
                subLeadpt = leadpt;
                subLeadLep = leadLep;
                leadpt = lep_pt->at(ilep);
                leadLep = ilep;
            } else if (lep_pt->at(ilep) > subLeadpt){
                subLeadpt = lep_pt->at(ilep);
                subLeadLep = ilep;
            }
        }
        
        // perform selection cuts
        if (lep_n > 1) { // require at least 2 leptons

            // check leading and subleading leptons have same flavour, opposite charge 
            if (Paired(leadLep,subLeadLep)) {
                
                // check both leptons are isolated
                if (Isolated(leadLep) and Isolated(subLeadLep)) {
                
                    TLorentzVector lVec1, lVec2, lVecTot; // lorentz vectors of leptons

                    // add lorentz vectors of leptons
                    lVec1.SetPtEtaPhiE(lep_pt->at(leadLep),lep_eta->at(leadLep),
                    lep_phi->at(leadLep),lep_E->at(leadLep));
                    lVec2.SetPtEtaPhiE(lep_pt->at(subLeadLep),lep_eta->at(subLeadLep),
                    lep_phi->at(subLeadLep),lep_E->at(subLeadLep));
                    lVecTot = lVec1 + lVec2;
                    
                    // calculate invariant masses
                    double invMass = lVecTot.M();
                    h_lep_mass -> Fill(invMass);
                }
            }
        }
    }
    
    // set style of histograms
    // generic style
    Style(h_lep_n,"Leptons","Events");
    Style(h_lep_type,"Flavour","Events");
    Style(h_lep_mass,"Invariant Mass (MeV)","Events");
    Style(h_lep_etcone,"E_T Isolation (MeV)","Events");
    Style(h_lep_ptcone,"p_T Isolation (MeV)","Events");
    Style(h_lep_charge,"Elementary Charge","Events");

    // specific style for invariant mass hist
    TCanvas * mCan = new TCanvas("mCan","mCan",600,500);
    mCan->cd();
    gPad->SetTicks(1,1);
    h_lep_mass->SetTitle("");
    h_lep_mass->SetStats(0);
    h_lep_mass->Draw();

    // add labels
    TLatex latex;

    latex.SetNDC();
    latex.SetTextSize(0.03);
    latex.DrawLatex(0.2,0.8,"#sqrt{s} = 13 Tev");
    latex.DrawLatex(0.2,0.72,"#int L dt = 10.064 fb^{-1}");

    // write histograms to file
    TFile outfile("outfile.root","recreate");
    h_lep_n -> Write();
    h_lep_type -> Write();
    h_lep_etcone -> Write();
    h_lep_ptcone -> Write();
    h_lep_charge -> Write();
    h_lep_mass -> Write();
    mCan->Write();
    delete mCan;
    outfile.Close();
    
    clock_t endTime = clock(); // get end time
    // calculate time taken and print it
    double time_spent = (endTime - startTime) / CLOCKS_PER_SEC;
    cout << time_spent << std::endl;
}
