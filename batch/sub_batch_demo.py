#!/usr/bin/env python

import getopt
import os
import sys
import glob
import math
import time
import subprocess

def usage():
    print ' '
    print 'Usage: sub.py %s inputLocation [options]' % sys.argv[0]
    print '-t | --type: specify the analysis type'
    print '-n | --name: specify the data file name'
    print '-o | --output directory: specify output directory'
    print ' '

#default settings
Type=0
Name='test'
Output=''
Walltime=2
Memory=2
system=os.system
currentDir = os.getcwd()

t = time.localtime()
timestr = '%s_%s_%s_%s:%s:%s' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

try:
    # command line options
    shortopts = 't:n:o:'
    longopts = ['Type=','Name=','Output=']
    opts, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
 
except getopt.GetoptError:
    print >> sys.stderr, 'ERROR: options unknown in %s' %sys.argv[1:]
    usage()
    sys.exit(1)

for o, a in opts:
    if o in('--Type', '-t'):
        Type = float(a)
    if o in('--Name', '-n'):
        Name = a
    if o in('--Output', '-o'):
        Output = a

#create submission shell script
if not os.path.exists('subs/'+Output):
    os.makedirs('subs/'+Output)
flname = 'subs/'+Output+'/'+Name+'_'+timestr+'.sh'

with open(flname,'a') as file:
    fstr = 'hostname \n'
    file.write(fstr)
    fstr = 'cd '+currentDir+' \n'
    file.write(fstr)
    #fstr = 'cd ../scripts/ \n'
    fstr = 'cd ../demo/ \n'
    file.write(fstr)
    #fstr = 'cp analyzetree.py analyzetree_running.py\n'
    #file.write(fstr)
    if Type == 0:
        fstr = 'python maketree_demo.py %s %s\n' % (Name,Output)
    #elif Type == 1:
    #    fstr = 'python analyzetree_running.py %s\n' % Output
    file.write(fstr)


ts = 'subs/'+Output+'/'+Name+'_'+timestr+'.sh'
w = 'walltime=0%s:00:00' % Walltime
m = 'mem=%sgb' % Memory
command = ['qsub -d . -l '+m+','+w+',naccesspolicy=shared -V -q hep -e '+currentDir+'/log/err.%s_%s' % (Name,timestr) + ' -o '+currentDir+'/log/log.%s_%s ' % (Name, timestr) + ts]
for c in command:
    print c
    time.sleep(1)
    os.system(c)
