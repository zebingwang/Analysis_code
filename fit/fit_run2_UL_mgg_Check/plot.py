from ROOT import *

mass_list = [1,2,3,4,5,6,7,8,9,10,15,20,25,30]

def main():
    for mass in mass_list:
        file_name = "ALP_data_bkg_Am"+str(mass)+"_workspace.root"

        file = TFile(file_name)

        data = file.CMS_hza_workspace.data("data_mass_cat0")
        ma = file.CMS_hza_workspace.var("CMS_hza_mass")
        
        c = TCanvas("c","c")
        c.cd()
        plot = ma.frame()
        data.plotOn(plot)
        plot.Draw()
        
        
        c.SaveAs("mass{0}.png".format(mass))

main()