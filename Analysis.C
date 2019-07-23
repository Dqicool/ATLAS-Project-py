#ifndef Analysis
#define Analysis

#include "backend/CLoop.h"

void CLoop::Book() {
    h_lep_n = new TH1F("lep_n","Number of leptons",10,-0.5,9.5);
}

void CLoop::Fill() {
    // fill lepton number
    h_lep_n -> Fill(lep_n);
}

void CLoop::Style() {
    h_lep_n -> Write();
}

#endif
