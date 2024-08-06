#include <iostream>
#include <set>
#include <TString.h>
#include <TFile.h>
#include <TTree.h>

void removeDuplicates() {
    //TString prefix = "/publicfs/cms/user/wangzebing/ALP/NTuples/17/data/ntuple_data17";
    //TString prefix = "/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/data/ALP_data_beforRM";
    TString prefix = "/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/massInde/CR/data/ALP_data_beforRM";
    //TString prefix = "/publicfs/cms/user/wangzebing/ALP/Analysis_out/17/QCD/ALP_QCD";
    //TString prefix = "/publicfs/cms/user/wangzebing/ALP/Analysis_out/18/data/data_Run2018";
    //TString prefix = "/publicfs/cms/user/wangzebing/ALP/Analysis_out/16/data/ALP_data_beforRM";
    TString filename = prefix+".root";

    std::cout<<filename<<std::endl;

    TFile *oldfile = new TFile(filename);
    //TTree *oldtree = (TTree*)oldfile->Get("Ana/passedEvents");
    TTree *oldtree = (TTree*)oldfile->Get("passedEvents");

    // Clone HIST
    TH1D *old0 = (TH1D*)oldfile->Get("nEvents_total");
    TH1D *old1 = (TH1D*)oldfile->Get("Events_weight");
    TH1D *old2 = (TH1D*)oldfile->Get("cross_section");
    TH1D *old3 = (TH1D*)oldfile->Get("nEvents_ntuple");
    TH1D *old4 = (TH1D*)oldfile->Get("nEvents_trig");
    TH1D *old5 = (TH1D*)oldfile->Get("Z_e_nocut");
    TH1D *old6 = (TH1D*)oldfile->Get("Z_mu_nocut");
    TH1D *old7 = (TH1D*)oldfile->Get("Z_e_lIso");
    TH1D *old8 = (TH1D*)oldfile->Get("Z_mu_lIso");
    TH1D *old9 = (TH1D*)oldfile->Get("Z_e_lIso_lTight");
    TH1D *old10 = (TH1D*)oldfile->Get("Z_mu_lIso_lTight");
    TH1D *old11 = (TH1D*)oldfile->Get("Z_50");

    Long64_t nentries = oldtree->GetEntries();
    std::cout<<nentries<<" total entries."<<std::endl;
    Long64_t Run, LumiSect, Event;
    bool passedZ4lSelection;
    oldtree->SetBranchAddress("Run",&Run);
    oldtree->SetBranchAddress("LumiSect",&LumiSect);
    oldtree->SetBranchAddress("Event",&Event);

    //Create a new file + a clone of old tree in new file
    TFile *newfile = new TFile(
            prefix+"_noDuplicates.root"
            ,"recreate");
    TTree *newtree = oldtree->CloneTree(0);

    std::set<TString> *runlumieventSet = new std::set<TString>;
    int nremoved = 0;
    for (Long64_t i=0;i<nentries; i++) {
        if (i%10000==0) std::cout<<i<<"/"<<nentries<<std::endl;
        oldtree->GetEntry(i);

        TString s_Run  = std::to_string(Run);
        TString s_Lumi = std::to_string(LumiSect);
        TString s_Event = std::to_string(Event);
        TString runlumievent = s_Run+":"+s_Lumi+":"+s_Event;

        if (runlumieventSet->find(runlumievent)==runlumieventSet->end()) {
            runlumieventSet->insert(runlumievent);
            newtree->Fill();
        } else {
            nremoved++;
        }
        //if (passedZ4lSelection) newtree->Fill();
    }

    std::cout<<nremoved<<" duplicates."<<std::endl;
    newtree->Print();
    newtree->AutoSave();

    old0->SetBinContent(1,old0->GetBinContent(1) - nremoved);
    old3->SetBinContent(1,old3->GetBinContent(1) - nremoved);
    old4->SetBinContent(1,old4->GetBinContent(1) - nremoved);
    old5->SetBinContent(1,old5->GetBinContent(1) - nremoved);
    old7->SetBinContent(1,old7->GetBinContent(1) - nremoved);
    old9->SetBinContent(1,old9->GetBinContent(1) - nremoved);
    old11->SetBinContent(1,old11->GetBinContent(1) - nremoved);

    old0->Write();
    old1->Write();
    old2->Write();
    old3->Write();
    old4->Write();
    old5->Write();
    old6->Write();
    old7->Write();
    old8->Write();
    old9->Write();
    old10->Write();
    old11->Write();

    //delete oldfile;
    delete runlumieventSet;
    delete newfile;
}
