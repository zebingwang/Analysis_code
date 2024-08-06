from ROOT import *


lumi = {'16':35.9, '17':41.5, '18':56.9}
years = ['16','17','18']
sysList = ['normal', 'phoScale_up', 'phoScale_dn', 'phoSmear_up', 'phoSmear_dn', 'lepScale_up', 'lepScale_dn', 'lepSmear_up', 'lepSmear_dn']
colors = [kRed, kBlue, kBlue, kGreen, kGreen, kYellow, kYellow, kMagenta, kMagenta]
a_masses = [1, 5, 15, 30]

param = {}
for a in a_masses:
    param[a] = {}
    for year in years:
        param[a][year] = {}

param[1]['16'] = {'dm0':-0.0652533, 'sigma0':0.0553823, 'dm1':-0.1912, 'sigma1':1.75688, 'dm2':2.23737, 'sigma2':6.05617, 'dm3':-0.371351, 'sigma3':1.02913, 'frac1':0.484577, 'frac2':0.366876, 'frac3':0.148547}
param[1]['17'] = {'dm0':0.0249542, 'sigma0':0.101339, 'dm1':-1.04821, 'sigma1':0.39956, 'dm2':2.23738, 'sigma2':5.98204, 'dm3':-0.137767, 'sigma3':1.54108, 'frac1':0.0137924, 'frac2':0.387875, 'frac3':0.598332}
param[1]['18'] = {'dm0':-0.0655347, 'sigma0':0.0552845, 'dm1':-0.357444, 'sigma1':1.08468, 'dm2':2.23738, 'sigma2':6.16043, 'dm3':-0.226777, 'sigma3':1.72545, 'frac1':0.118423, 'frac2':0.379169, 'frac3':0.502408}

param[5]['16'] = {'dm0':-0.236094, 'sigma0':0.0850695, 'dm1':2.25012, 'sigma1':1.09445, 'dm2':-2.14988, 'sigma2':2.23017, 'dm3':-0.323266, 'sigma3':1.30717, 'frac1':0.041347, 'frac2':0.326177, 'frac3':0.632476}
param[5]['17'] = {'dm0':-0.408279, 'sigma0':0.194628, 'dm1':-2.25012, 'sigma1':2.30817, 'dm2':2.25012, 'sigma2':1.03793, 'dm3':-0.331407, 'sigma3':1.30429, 'frac1':0.30561, 'frac2':0.0513742, 'frac3':0.63946}
param[5]['18'] = {'dm0':-0.386207, 'sigma0':0.278767, 'dm1':2.25012, 'sigma1':1.16426, 'dm2':-2.14988, 'sigma2':2.24451, 'dm3':-0.317729, 'sigma3':1.34256, 'frac1':0.0316429, 'frac2':0.325861, 'frac3':0.634445}

param[15]['16'] = {'dm0':-0.177703, 'sigma0':0.877, 'dm1':-2.01908, 'sigma1':0.873737, 'dm2':1.66408, 'sigma2':0.640646, 'dm3':-2.16039, 'sigma3':2.96118, 'frac1':0.139504, 'frac2':0.0701894, 'frac3':0.334317}
param[15]['17'] = {'dm0':-0.329109, 'sigma0':1.34821, 'dm1':-0.15021, 'sigma1':0.719246, 'dm2':-2.16039, 'sigma2':4.76834, 'dm3':-2.16039, 'sigma3':2.42401, 'frac1':0.0646494, 'frac2':0.0655748, 'frac3':0.254521}
param[15]['18'] = {'dm0':0.0779263, 'sigma0':0.0704068, 'dm1':-0.329406, 'sigma1':1.40078, 'dm2':-0.0403169, 'sigma2':0.799094, 'dm3':-2.16039, 'sigma3':3.0898, 'frac1':0.527187, 'frac2':0.101912, 'frac3':0.370902}

param[30]['16'] = {'dm0':-0.044217, 'sigma0':0.0724405, 'dm1':-0.241888, 'sigma1':1.25249, 'dm2':-1.72783, 'sigma2':10.4212, 'dm3':-2.12743, 'sigma3':2.6405, 'frac1':0.624885, 'frac2':0.044041, 'frac3':0.331074}
param[30]['17'] = {'dm0':-0.0402202, 'sigma0':0.0541007, 'dm1':-0.254839, 'sigma1':1.26166, 'dm2':-1.87255, 'sigma2':11.0724, 'dm3':-2.12744, 'sigma3':2.6061, 'frac1':0.622296, 'frac2':0.0507838, 'frac3':0.32692}
param[30]['18'] = {'dm0':-0.0442199, 'sigma0':0.14837, 'dm1':-0.261486, 'sigma1':1.27452, 'dm2':-1.72748, 'sigma2':11.0707, 'dm3':-2.12744, 'sigma3':2.64128, 'frac1':0.62626, 'frac2':0.0438758, 'frac3':0.329865}

param_float = {'Scale':['dm0', 'dm1', 'dm2', 'dm3'], 'Smear':['sigma0', 'sigma1', 'sigma2', 'sigma3']}

def sumGaussians(mass, param, scale):

    global MH, dm0, mean0, sigma0, gauss0
    global dm1, mean1, sigma1, gauss1, frac1
    global dm2, mean2, sigma2, gauss2, frac2
    global dm3, mean3, sigma3, gauss3, frac3

    MH = RooRealVar("MH","MH",125.0)
    
    dm0 = RooRealVar("dm0","dm0",param['dm0'],-3.,3.)
    mean0 = RooFormulaVar("mean0","mean0","@0+@1",RooArgList(MH,dm0))
    sigma0 = RooRealVar("sigma0","sigma0",param['sigma0'],0.01,20.)
    gauss0 = RooGaussian("gaus0","gaus0",mass,mean0,sigma0)
    #frac0 = RooRealVar("frac0","frac0",0.01,-0.005,0.005)

    dm1 = RooRealVar("dm1","dm1",param['dm1'],-3.,3.)
    mean1 = RooFormulaVar("mean1","mean1","@0+@1",RooArgList(MH,dm1))
    sigma1 = RooRealVar("sigma1","sigma1",param['sigma1'],0.01,20.)
    gauss1 = RooGaussian("gaus1","gaus1",mass,mean1,sigma1)
    frac1 = RooRealVar("frac1","frac1",param['frac1'],0.,1.0)

    dm2 = RooRealVar("dm2","dm2",param['dm2'],-3.,3.)
    mean2 = RooFormulaVar("mean2","mean2","@0+@1",RooArgList(MH,dm2))
    sigma2 = RooRealVar("sigma2","sigma2",param['sigma2'],0.01,20.)
    gauss2 = RooGaussian("gaus2","gaus2",mass,mean2,sigma2)
    frac2 = RooRealVar("frac2","frac2",param['frac2'],0.,1.0)

    dm3 = RooRealVar("dm3","dm3",param['dm3'],-3.,3.)
    mean3 = RooFormulaVar("mean3","mean3","@0+@1",RooArgList(MH,dm3))
    sigma3 = RooRealVar("sigma3","sigma3",param['sigma3'],0.01,20.)
    gauss3 = RooGaussian("gaus3","gaus3",mass,mean3,sigma3)
    frac3 = RooRealVar("frac3","frac3",param['frac3'],0.,1.0);

    MH.setConstant(kTRUE)
    frac1.setConstant(kTRUE)
    frac2.setConstant(kTRUE)
    frac3.setConstant(kTRUE)

    if scale == 1:
        sigma0.setConstant(kTRUE)
        sigma1.setConstant(kTRUE)
        sigma2.setConstant(kTRUE)
        sigma3.setConstant(kTRUE)
    elif scale == 2:
        dm0.setConstant(kTRUE)
        dm1.setConstant(kTRUE)
        dm2.setConstant(kTRUE)
        dm3.setConstant(kTRUE)
    else:
        sigma0.setConstant(kTRUE)
        sigma1.setConstant(kTRUE)
        sigma2.setConstant(kTRUE)
        sigma3.setConstant(kTRUE)

        dm0.setConstant(kTRUE)
        dm1.setConstant(kTRUE)
        dm2.setConstant(kTRUE)
        dm3.setConstant(kTRUE)

    func = RooAddPdf("nSum", "nSum", RooArgList(gauss3,gauss2,gauss1,gauss0), RooArgList(frac3,frac2,frac1))

    #gauss0.Print()
    #func.Print()

    return func
    



def main():

    path_file = '/publicfs/cms/user/wangzebing/ALP/Analysis_code/fit/fit_run2_param_ScaleSmear/'
    path_out = '/publicfs/cms/user/wangzebing/ALP/Analysis_code/fit/fit_run2_param_ScaleSmear/ScaleSmear_plot/'
    ws_name = 'CMS_hza_workspace'

    for a_mass in a_masses:
        for year in years:
            file = TFile(path_file+'ALP_sig_Am'+str(a_mass)+'_Hm125_'+year+'_workspace.root')
            inWS = file.Get(ws_name)

            mass_ = inWS.var("CMS_hza_mass")
            mass_.SetTitle("m_{Za}")
            mass_.setUnit("GeV")
            mass_.setRange(110.0, 140.0)
            intLumi_ = inWS.var("IntLumi")

            data = {}
            model = {}
            fitResult = {}
            h = {}

            canv = TCanvas("c1","c1",800,1000)
            frame = mass_.frame()
            legend = TLegend(0.55,0.55,0.89,0.89)
            #legend.SetHeader("The Legend Title","C")
            

            for sys in sysList:
                if 'Scale' in sys:
                    s = 1
                elif 'Smear' in sys:
                    s = 2
                else:
                    s = 0
                data[sys] = inWS.data("ggh_125_13TeV_cat0_"+sys)
                model[sys] = sumGaussians(mass_, param[a_mass][year], s)
                fitResult[sys] = model[sys].fitTo(data[sys],RooFit.Save(kTRUE))
                if sys == 'normal': data[sys].plotOn(frame)
                #data[sys].plotOn(frame, RooFit.LineColor(colors[sysList.index(sys)]))
                model[sys].plotOn(frame, RooFit.LineColor(colors[sysList.index(sys)]))
                #if sys == 'normal': data[sys].plotOn(frame)

                h[sys] = TH1F("h_"+sys,"h_"+sys,1,0,1)
                h[sys].SetLineColor(colors[sysList.index(sys)])
                legend.AddEntry(h[sys],sys,'L')


            #legend.Draw()
            frame.SetTitle("ScaleSmear_"+str(a_mass)+"_"+year)
            frame.Draw()
            legend.Draw()
            canv.SaveAs(path_out+"ScaleSmear_m"+str(a_mass)+"_"+year+".png")

            #print fitResult['normal']
            #print fitResult[sys].getVal('dm0')
            #print fitResult['normal']
            #fitResult[sys]
            #print 'param: {0}'.format(fitResult['normal'].floatParsFinal().Print("s"))
            '''
            print '####'
            print fitResult['phosmear_up'].floatParsFinal()
            print fitResult['phosmear_up'].floatParsFinal().Print("s")
            print fitResult['phosmear_up'].constPars().Print("s")
            print fitResult['phosmear_up'].floatParsFinal().Print()
            print fitResult['phosmear_up'].floatParsFinal().find("sigma3").getVal()
            '''

            
            file = open(path_out+'ScaleSmear_m'+str(a_mass)+'_'+year+'.txt', 'a')
            title = '{0:15}\t\t\t'.format('paramters')
            for sys in sysList:
                title = title + '{0:15}\t\t\t'.format(sys)

            file.write(title + '\n')

            for scsm in param_float:
                for par in param_float[scsm]:
                    line = '{0:15}\t'.format(par)
                    for sys in sysList:
                        if sys == 'normal':
                            if scsm == 'Scale':
                                par_val = fitResult['phoScale_up'].floatParsInit().find(par).getVal()
                            else:
                                par_val = fitResult['phoScale_up'].constPars().find(par).getVal()
                            par_val_norm = par_val
                        else:
                            if scsm in sys:
                                par_val = fitResult[sys].floatParsFinal().find(par).getVal()
                            else:
                                par_val = fitResult[sys].constPars().find(par).getVal()

                        line = line + '{0:15}\t\t\t'.format(par_val)
                    file.write(line + '\n')



            sysType = ['photon', 'lepton']
            
            for scsm in param_float:
                line = "photonCat" + scsm +"="
                for p in sysType:
                    line = line + p + '_' + scsm + '_M' + str(a_mass)+'_'+year + ','
                line.rstrip(',')
                file.write(line + '\n')

            L = ['diphotonCat=0', 'proc=ggh']
            for line in L:
                file.write(line + '\n')

            mean_change = 0.0
            sigma_change = 0.0
            rate_change = 0.0

            for scsm in param_float:
                for p in sysType:
                    line = p + '_' + scsm + '_' + str(a_mass)+'_'+year +'\t'

                    par_val_norm = -99.9
                    par_val_change = -99.9

                    for par in param_float[scsm]:

                        for sys in sysList:

                            if sys == 'normal':
                                if scsm == 'Scale':
                                    par_val = fitResult['phoScale_up'].floatParsInit().find(par).getVal()
                                else:
                                    par_val = fitResult['phoScale_up'].constPars().find(par).getVal()
                                par_val_norm = par_val
                            else:
                                if scsm in sys:
                                    par_val = fitResult[sys].floatParsFinal().find(par).getVal()
                                else:
                                    par_val = fitResult[sys].constPars().find(par).getVal()

                            if scsm == 'Scale':
                                if abs(par_val_norm - par_val)/(125.0+par_val_norm) > par_val_change:
                                    par_val_change = abs(par_val_norm - par_val)/(125.0+par_val_norm)
                            else:
                                if abs(par_val_norm - par_val) > par_val_change:
                                    par_val_change = abs(par_val_norm - par_val)
                    
                    
                    if scsm == 'Scale':
                        line = line + str(par_val_change) + '\t0.0\t0.0'
                    else:
                        line = line + '0.0\t' + str(par_val_change) + '\t0.0'

                    file.write(line + '\n')


            

main()