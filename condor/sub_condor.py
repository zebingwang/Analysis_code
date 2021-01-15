#!/usr/bin/python

import sys, os, pwd, commands
import optparse, shlex, re
import time
from time import gmtime, strftime
import math

#define function for parsing options
def parseOptions():
    global observalbesTags, modelTags, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option('-l', '--list', dest='LIST', type='string',default='./data_list/list_data_17.txt', help='the path of input data list')
    parser.add_option('-p', '--python', dest='PYTHON', type='string',default='../Reduced-tree/runCondor/condorFile/codeFile/makePlots_LLA_tree.py', help='path of the excuted python file')
    parser.add_option('-L', '--Lumi', dest='LUMI', type='string',default='35.9', help='luminosities')
    parser.add_option('-C', '--CR', dest='CR', action='store_true', default=False, help='make control region')
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# define function for processing the external os commands
def processCmd(cmd, quite = 0):
    #    print cmd
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
        return "ERROR!!! "+output
    else:
        return output

def sub_condor():

    # parse the arguments and options
    global opt, args
    parseOptions()

    pyFile = opt.PYTHON
    datalist = opt.LIST
    lumi = opt.LUMI
    CR = opt.CR

    basicPath_output = '/publicfs/cms/user/wangzebing/ALP/Analysis_out/'

    list = open(datalist)

    for line in list:

        if (line.startswith('#')): continue
        line.rstrip()
        line.lstrip()

        path_data = line.split()[0]
        cross_section = line.split()[1]
        nEvent = line.split()[2]
        lumi = line.split()[3]
        year = line.split()[4]
        year = year.strip('\n')

        if 'Run2018' in path_data:
            path_out = basicPath_output + '18/massInde/data/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')
        elif 'Run2017' in path_data:
            path_out = basicPath_output + '17/massInde/data/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')
        elif 'Run2016' in path_data:
            path_out = basicPath_output + '16/massInde/data/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')
        elif year == '2016':
            path_out = basicPath_output + '16/massInde/mc/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')
        elif year == '2017':
            path_out = basicPath_output + '17/massInde/mc/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')
        elif year == '2018':
            path_out = basicPath_output + '18/massInde/mc/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')
        else:
            print "wrong year"
            exit(0)

        if CR:
            path_out = path_out.replace('massInde', 'massInde/CR')
        #path_out = '/publicfs/cms/user/wangzebing/ALP/NTuples/17/test/ALP_' + path_data.split('/')[-1].lstrip('ntuple_')

        if CR:
            cmd = 'hep_sub condor.sh -g cms -mem 4000 -wt mid -argu ' + pyFile + ' ' + path_data + ' ' + path_out + ' ' + cross_section + ' ' + lumi + ' ' + nEvent + ' ' + year + ' -o ./condor_out/' + path_data.split('/')[-1].lstrip('ntuple_').rstrip('.root') + '_' + year + '_massInde_CR.log' + ' -e ./condor_out/' + path_data.split('/')[-1].lstrip('ntuple_').rstrip('.root') + '_' + year + '_massInde_CR.err'
        else:
            cmd = 'hep_sub condor.sh -g cms -mem 4000 -wt mid -argu ' + pyFile + ' ' + path_data + ' ' + path_out + ' ' + cross_section + ' ' + lumi + ' ' + nEvent + ' ' + year + ' -o ./condor_out/' + path_data.split('/')[-1].lstrip('ntuple_').rstrip('.root') + '_' + year + '_massInde.log' + ' -e ./condor_out/' + path_data.split('/')[-1].lstrip('ntuple_').rstrip('.root') + '_' + year + '_massInde.err'
        #print cmd
        output = processCmd(cmd)

        print output

# run the submitAnalyzer() as main()
if __name__ == "__main__":
    sub_condor()
