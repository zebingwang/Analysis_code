from ROOT import *
import math

import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from pynverse import inversefunc



sigma_excpet = 0.1
H_xs = 56.
H_total_width= 0.0032
H_mass = 125.18
Z_mass = 91.1876
ZToll_br = 0.06729
aTogg_br = 0.1
L_det = 1.5




def getLimits(file_name):
    file = TFile(file_name)

    if file:
        print 'file opened'
    tree = file.Get("limit")
    if tree:
        print 'tree opened'

    limits = []
    #print'tree = ', tree
    for quantile in tree:
        #print'quantile = ', quantile
        limits.append(tree.limit*1000.)  # fb

    return limits[:6]



def getlambda(x, y):
    return (1-x-y)*(1-x-y)-4*x*y

def width_hToza(m_h, m_z, m_a, C_zh):
    L = getlambda((m_z*m_z)/(m_h*m_h), (m_a*m_a)/(m_h*m_h))
    #print L
    #print L**(3./2.)
    return m_h*m_h*m_h*(L**(3./2.))*(C_zh)**(2.)/(16.*np.pi)

def width_aToGG(m_h, m_z, m_a, C_GG):
    return 4*np.pi*(1./137.)*(1./137.)*(m_a**(3))*((C_GG)**(2))

def getL_a(m_h, m_z, m_a, Br_aToGG, C_GG):
    #C_GG = 1 # GeV^{-1}
    gamma_a = (m_h*m_h-m_z*m_z+m_a*m_a)/(2*m_a*m_h)
    L_a = np.sqrt(gamma_a*gamma_a-1)*Br_aToGG/width_aToGG(m_h, m_z, m_a, C_GG)
    return L_a

def getf_dec_za(m_h, m_z, m_a, Br_aToGG, C_GG, L_det):
    #C_GG = 1 # GeV^{-1}
    L_a = getL_a(m_h, m_z, m_a, Br_aToGG, C_GG)
    #print "L_a = " + str(L_a)
    val1,err1=quad(lambda x:np.sin(x)*(1-np.exp(-L_det/L_a*np.sin(x))), 0., np.pi/2.)
    return val1


def getCoefficient(A_mass, r, C_GG, isPrompt):

    sigma_exc = r*sigma_excpet
    if isPrompt:
        f_dec_za = 1.
        #print "f_dec_za: " + str(f_dec_za)
    else:
        f_dec_za = getf_dec_za(H_mass, Z_mass, A_mass, aTogg_br, C_GG, L_det)
        #print "f_dec_za: " + str(f_dec_za)
    r_exc = sigma_exc/(H_xs*ZToll_br*aTogg_br*f_dec_za)

    Gamma_hToZa_exc = H_total_width*r_exc/(1.0-r_exc)
    #print Gamma_hToZa_exc, r_exc, f_dec_za
    return math.sqrt(Gamma_hToZa_exc*16.*math.pi/H_mass**3/getlambda((Z_mass/H_mass)**2,(A_mass/H_mass)**2)**1.5)*1000

def plot_L_a(masses):

    for m in masses:
        C_GG = np.arange(1., 1000000, 200) #TeV^-1
        L_a = []
        for x in C_GG:
            L_a.append(getL_a(H_mass, Z_mass, m, aTogg_br, x*0.001))

        #plt.axes(xscale = "log", yscale = "log")
        plt.rcParams['figure.figsize'] = (12.0, 8.0)
        plt.loglog(C_GG, L_a, label=r"m_{a} = "+str(m)+" GeV")
        plt.xlabel(r"$C^{eff}_{\gamma\gamma}\ ([\frac{\Lambda}{1 TeV}])$", size = 20)
        plt.ylabel(r'$L_{a}\ (m)$', size = 20)

    #plt.ylim(0., 1.2)
    plt.loglog(C_GG, 1.5*np.ones(len(C_GG)), label="distance of detector: 1.5m")
    plt.grid()
    plt.legend(loc='upper right',fontsize=10)
    plt.savefig('./plots/L_a_braTogg_p1.png')
    plt.close()
    #plt.show()

def plot_f_dec_za(masses, L_det):

    for m in masses:
        C_GG = np.append(np.arange(1, 1000., 10),np.arange(1000., 1000000, 200))#TeV^-1
        f_dec_za = []
        for x in C_GG:
            f_dec_za.append(getf_dec_za(H_mass, Z_mass, float(m), aTogg_br, x*0.001, L_det))

        #plt.axes(xscale = "log")
        plt.rcParams['figure.figsize'] = (12.0, 8.0)
        plt.axes(xscale = "log")
        plt.plot(C_GG, f_dec_za, label=r"m_{a} = "+str(m)+" GeV")
        plt.xlabel(r"$C^{eff}_{\gamma\gamma}\ ([\frac{\Lambda}{1 TeV}])$", size = 20)
        plt.ylabel(r'$f^{Za}_{dec}$', size = 20)

    #plt.ylim(0., 1.2)
    plt.grid()
    plt.legend(loc='upper left',fontsize=10)
    plt.savefig('./plots/f_dec_Za_braTogg_p1.png')
    plt.close()
    #plt.show()


def plot_Cza_vs_Cgg(masses, limits_xs):

    for m in masses:
        C_GG_x = np.append(np.arange(1, 1000., 10),np.arange(1000., 1000000, 1000))
        C_GG = []
        C_zh = []
        for x in C_GG_x:
            if limits_xs[m][5]/1000.*sigma_excpet/(H_xs*ZToll_br*aTogg_br*getf_dec_za(H_mass, Z_mass, m, aTogg_br, x*0.001, L_det)) > 1.:
                continue
            C_GG.append(x)
            C_zh.append(getCoefficient(float(m), limits_xs[m][5]/1000., x*0.001, 0))

        #plt.axes(xscale = "log")
        plt.rcParams['figure.figsize'] = (12.0, 8.0)
        plt.loglog(C_zh, C_GG, label=r"m_{a} = " + str(m) + " GeV")
        plt.xlabel(r"$C^{eff}_{zh}\ ([\frac{\Lambda}{1 TeV}])$", size = 20)
        plt.ylabel(r"$C^{eff}_{\gamma\gamma}\ ([\frac{\Lambda}{1 TeV}])$", size = 20)

    #plt.ylim(0., 1.2)
    plt.grid()
    plt.legend(loc='upper right',fontsize=10)
    plt.savefig('./plots/Cza_vs_Cgg_braTogg_p1.png')
    plt.close()
    #plt.show()


def plot_Cgg_vs_mA(masses, limits_xs):
    C_zh = [0.1, 0.01]
    #for m in masses:
        



def main():
    mass_lists = [1,2,3,4,5,6,7,8,9,10,15,20,25,30]
    #plot_L_a(mass_lists)
    #plot_f_dec_za(mass_lists,L_det)
    masses = range(1,31)
    limit = {}
    for m in masses:
        file_name = "limit_M"+str(m)+".root"
        limit[m] = getLimits(file_name)
    
    #plot_Cza_vs_Cgg(masses, limit)

main()