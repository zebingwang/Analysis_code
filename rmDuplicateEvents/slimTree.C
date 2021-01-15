#include <iostream>
#include <set>
#include <TString.h>
#include <TFile.h>
#include <TTree.h>

void slimTree() {
    TString prefix = "/scratchfs/cms/wangzebing/ntuple_DoubleEG_Run2017B";
    TString filename = prefix+".root";

    std::cout<<filename<<std::endl;

    TFile *oldfile = new TFile(filename);
    TTree *oldtree = (TTree*)oldfile->Get("Ana/passedEvents");
    //TTree *oldtree = (TTree*)oldfile->Get("passedEvents");

    Long64_t nentries = oldtree->GetEntries();
    std::cout<<nentries<<" total entries."<<std::endl;
    vector<float> lep_pt, pho_pt;
    oldtree->SetBranchAddress("lep_pt",&lep_pt);
    oldtree->SetBranchAddress("pho_pt",&pho_pt);

    //Create a new file + a clone of old tree in new file
    TFile *newfile = new TFile(
            prefix+"_slimmed.root"
            ,"recreate");
    TTree *newtree = oldtree->CloneTree(0);

    std::set<TString> runlumieventSet;
    int nremoved = 0;
    for (Long64_t i=0;i<nentries; i++) {
        if (i%10000==0) std::cout<<i<<"/"<<nentries<<std::endl;
        if (i==100000) break;
        oldtree->GetEntry(i);

        if (lep_pt.size() >=2 && pho_pt.size() >=1) {
            newtree->Fill();
        } else {
            nremoved++;
        }
        //if (passedZ4lSelection) newtree->Fill();
    }

    std::cout<<nremoved<<" duplicates."<<std::endl;
    newtree->Print();
    newtree->AutoSave();
    //delete oldfile;
    delete newfile;
}
