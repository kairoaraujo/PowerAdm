#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
# Importing classes/modules
import time
import os.path
from globalvar import *
from config import *
from newid import *
from systemVios import *
from verify import *

def lparconfig():
    prefix = raw_input("Prefix (XXXX-lparname): ")
    lparname = raw_input("LPAR Hostname: ")
    lparentcpu = float(raw_input("LPAR Entitled CPU desired: "))
    lparentcpumin = lparentcpu-(lparentcpu*cpu_min/100)
    lparentcpumax = (lparentcpu*cpu_max/100)+lparentcpu
    lparvcpu = int(raw_input("LPAR Virtual CPU desired: "))
    calcvcpumin = lparvcpu-(lparvcpu*cpu_min/100)
    if calcvcpumin < 1:
        lparvcpumin = 1
    lparvcpumax = (lparvcpu*cpu_max/100)+lparvcpu
    lparmem = int(raw_input("LPAR Memory desired: "))
    lparmenmin = lparmem-(lparmem*mem_min/100)
    lparmenmax = (lparmem*mem_max/100)+lparmem

os.system('clear')
print ("\n\n[ Power Adm ]\n[ Version: %s - © 2014 Kairo Araujo - BSD License ]\n\n" % version)

print ("[LPAR Configuration ]\n")
change = raw_input("Change or Ticket number: ")

#f_change = open("changes/%s_%s.sh" % (change, timestr) , 'w')

lparconfig()
configlpar = checkOk('The configuration of last LPAR is OK?(y/n): ', 'answer')
configlpar.mkCheck()
configlpar.answerCheck()

freeid = newId('newid')
freeid.mkId()
freeid.getId()

system_vio = systemVios('system', 'vio1', 'vio2')
system_vio.selectSystemVios()
system_vio.getSystem()
system_vio.getVio1()
system_vio.getVio1()


print (freeid.getId())
print (system_vio.getSystem())
print (system_vio.getVio1())
print (system_vio.getVio2())
print (configlpar.answerCheck())


