from ROOT import *
from array import array

def SetgStyle():

    gStyle.SetFrameFillColor(0)
    gStyle.SetStatColor(0)
    gStyle.SetOptStat(0)
    gStyle.SetTitleFillColor(0)
    gStyle.SetCanvasBorderMode(0)
    gStyle.SetPadBorderMode(0)
    gStyle.SetFrameBorderMode(0)
    gStyle.SetPadColor(kWhite)
    gStyle.SetCanvasColor(kWhite)
    
    
    gStyle.SetCanvasDefH(600) #Height of canvas
    gStyle.SetCanvasDefW(600) #Width of canvas
    gStyle.SetCanvasDefX(0)   #POsition on screen
    gStyle.SetCanvasDefY(0)

    
    gStyle.SetPadLeftMargin(0.13)
    gStyle.SetPadRightMargin(0.05)
    gStyle.SetPadTopMargin(0.085)
    gStyle.SetPadBottomMargin(0.12)
    
    # For hgg axis titles:
    gStyle.SetTitleColor(1, "XYZ")
    gStyle.SetTitleFont(42, "XYZ")
    gStyle.SetTitleSize(0.05, "XYZ")
    gStyle.SetTitleXOffset(0.95)#//0.9)
    gStyle.SetTitleYOffset(0.9)# // => 1.15 if exponents
    
    # For hgg axis labels:
    gStyle.SetLabelColor(1, "XYZ")
    gStyle.SetLabelFont(42, "XYZ")
    gStyle.SetLabelOffset(0.007, "XYZ")
    gStyle.SetLabelSize(0.04, "XYZ")
    
    # Legends
    gStyle.SetLegendBorderSize(0)
    gStyle.SetLegendFillColor(kWhite)
    gStyle.SetLegendFont(42)
    
    gStyle.SetFillColor(10)
    # Nothing for now
    gStyle.SetTextFont(42)
    gStyle.SetTextSize(0.03)

   


#massList = [1,2,3,4,5,6,7,8,9,10,15,20,25,30]
massList = range(1,31)
#massList = [1,2,3,4,5,6,7,8,9,10]
m_x = array('d')
for m in massList:
    m_x.append(m)
events_id = {}

for m in massList:
    file = open("M"+str(m)+".txt")
    lines = file.readlines()
    events_id[m] = []
    for l in lines[3:-1]:
        events_id[m].append(l.rstrip('\n'))

overlap = {}
overlap_rate = {}

for m in massList:
    overlap[m] = {}
    overlap_rate[m] = array('d')
    for mj in massList:
        overlap[m][mj] = set(events_id[m]) & set(events_id[mj])

        overlap_rate[m].append(float(len(overlap[m][mj]))/float(len(events_id[m])))

#print overlap
print overlap_rate, len(overlap[1][2]), len(events_id[1]), len(events_id[2])

canvas = TCanvas('c','c',6500,6500)
canvas.Divide(5,6,0.01,0.01)
gr = {}
for i in range(1,31):
    canvas.cd(i)
    canvas.SetRightMargin(0.13)
    canvas.SetLeftMargin(0.03)
    canvas.SetTopMargin(0.085)
    canvas.SetBottomMargin(0.12)
    SetgStyle()

    gr[i] = TGraph( len(massList), m_x, overlap_rate[i] )


    gr[i].SetLineWidth( 2 )

    gr[i].SetTitle('M'+str(i))
    gr[i].GetHistogram().SetMaximum(1.1)
    gr[i].GetHistogram().SetMinimum(0.0)
    gr[i].SetMarkerStyle(20)
    gr[i].SetMarkerSize(2)
    gr[i].GetXaxis().SetTitle( 'm_{a} (GeV)' )
    gr[i].GetYaxis().SetTitle( 'Overlap rate' )
    gr[i].SetFillColor(40)

    gr[i].Draw("AB")

canvas.SaveAs('OverlapRate.png')
canvas.Close()