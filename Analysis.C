#ifndef Analysis
#define Analysis

#include "backend/CLoop.h"

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
    if (lep_pt->at(l)>10e3 and lep_etcone20->at(l)<10e3 and lep_ptcone30->at(l)<10e3)
    return true;
    else return false;
}

void CLoop::StyleHist(TH1F *hist, const char* xaxis, const char* yaxis) {
    // set the style of the histograms
    hist->GetXaxis()->SetTitle(xaxis);
    hist->GetYaxis()->SetTitle(yaxis);
    hist->SetLineColor(kBlue-4);
    hist->SetFillColor(kBlue-6);
}

void CLoop::Book() {
    h_lep_n = new TH1F("lep_n","Number of leptons",10,-0.5,9.5);
    h_lep_type = new TH1F("lep_type","Type of leptons",10,10.5,20.5);
    h_lep_charge = new TH1F("lep_charge","Charge of leptons",10,-1.5,1.5);
    h_lep_mass = new TH1F("lep_mass","Invariant mass of leptons",20,100e3,150e3);
    h_lep_pt = new TH1F("lep_pt","Transverse momentum of leptons",200,0,14e4);
    h_lep_ptcone = new TH1F("lep_ptcone30","ptcone30 of leptons",200,9e2,3e3);
    h_lep_etcone = new TH1F("lep_etcone20","etcone20 of leptons",200,-3e3,7e3);
}

void CLoop::Fill(double weight) {
    // fill lepton number histogram
    h_lep_n -> Fill(lep_n);

    // loop over leptons in event
    for (size_t ilep=0; ilep<lep_type->size(); ilep++) {
        h_lep_type -> Fill(lep_type->at(ilep),weight);
        h_lep_charge -> Fill(lep_charge->at(ilep),weight); // fill lepton charge
        h_lep_pt -> Fill(lep_pt->at(ilep),weight); // fill lepton transverse momentum
        h_lep_etcone -> Fill(lep_etcone20->at(ilep),weight); // fill lepton etcone20
        h_lep_ptcone -> Fill(lep_ptcone30->at(ilep),weight); // fill lepton ptcone30
    }

    if (lep_n > 3) { // require at least 4 leptons
        // get ordered list of letons by transverse momentum
        int lepOrder [4];
        vector <float> ptOrder = * lep_pt;
        sort(ptOrder.begin(), ptOrder.end(), greater<double>());
        for (size_t i=0; i<4; i++) {
            for (size_t j=0; j<lep_pt->size(); j++) {
                if (ptOrder[i] == lep_pt->at(j))
                    lepOrder[i] = j;
            }
        }
        
    
        // perform selection cuts
        //
        // check for pairs of leptons with same flavour, opposite charge 
        if ((Paired(lepOrder[0],lepOrder[1]) and Paired(lepOrder[2],lepOrder[3])) or
                (Paired(lepOrder[0],lepOrder[2]) and Paired(lepOrder[1],lepOrder[3])) or
                (Paired(lepOrder[0],lepOrder[3]) and Paired(lepOrder[1],lepOrder[2]))) {
            
            // check both leptons are isolated
            if (Isolated(lepOrder[0]) and Isolated(lepOrder[1]) and Isolated(lepOrder[2]) and Isolated(lepOrder[3])) {
            
                TLorentzVector lVecs [4]; // lorentz vectors of leptons

                // add lorentz vectors of leptons
                for (size_t i=0; i<4; i++) {
                    lVecs[i].SetPtEtaPhiE(lep_pt->at(lepOrder[i]),lep_eta->at(lepOrder[i]),
                            lep_phi->at(lepOrder[i]),lep_E->at(lepOrder[i]));
                }

                TLorentzVector lVecTot;
                for (size_t i=0; i<4; i++) {
                    lVecTot += lVecs[i];
                }
                
                // calculate invariant masses
                double invMass = lVecTot.M();
                h_lep_mass -> Fill(invMass,weight);
            }
        }
    }
}

void CLoop::Style() {
    // set style of histograms
    // generic style
    StyleHist(h_lep_n,"Leptons","Events");
    StyleHist(h_lep_type,"Flavour","Events");
    StyleHist(h_lep_mass,"Invariant Mass (MeV)","Events / 2.5 Gev");
    StyleHist(h_lep_etcone,"E_T Isolation (MeV)","Events");
    StyleHist(h_lep_ptcone,"p_T Isolation (MeV)","Events");
    StyleHist(h_lep_charge,"Elementary Charge","Events");

    // specific style for invariant mass hist
    TCanvas * mCan = new TCanvas("mCan","mCan",600,500);
    mCan->cd();
    gPad->SetTicks(1,1);
    h_lep_mass->SetTitle("");
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
}

#endif
