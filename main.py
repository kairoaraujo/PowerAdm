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

#### FRONTEND ####

# get lpar configuration (mem, cpu etc)
def lparconfig():
    global prefix, lparname, lparentcpu, lparentcpumin, lparentcpumax, lparvcpu
    global lparvcpumin, lparvcpumax, lparmem, lparmenmin, lparmenmax

    print ("\n[LPAR Configuration ]\n")
    prefix = raw_input("Prefix (XXXX-lparname): ")
    lparname = raw_input("LPAR Hostname: ")
    lparentcpu = float(raw_input("LPAR Entitled CPU desired: "))
    lparentcpumin = lparentcpu-(lparentcpu*cpu_min/100)
    lparentcpumax = (lparentcpu*cpu_max/100)+lparentcpu
    lparvcpu = int(raw_input("LPAR Virtual CPU desired: "))
    lparvcpumin = lparvcpu-(lparvcpu*cpu_min/100)
    if lparvcpumin < 1:
        lparvcpumin = 1
    lparvcpumax = (lparvcpu*cpu_max/100)+lparvcpu
    lparmem = int(raw_input("LPAR Memory desired: "))
    lparmenmin = lparmem-(lparmem*mem_min/100)
    lparmenmax = (lparmem*mem_max/100)+lparmem

    # get free id from newId.py
    global freeid
    freeid = newId('newid')
    freeid.mkId()
    freeid.getId()

    # select a system and vios from systemVios.py
    global system_vio
    system_vio = systemVios('system', 'vio1', 'vio2')
    system_vio.selectSystemVios()
    system_vio.getSystem()
    system_vio.getVio1()
    system_vio.getVio1()

    # get network configuration
    net_vlan = []
    net_vsw = []
    netconfiglpar = checkOk('Do you want another network interface (max 3 ethernets)? (y/n): ', 'y')
    while netconfiglpar.answerCheck() == 'y':
        print ("\n[LPAR Network Configuration]\n"
               "\nSelect the Virtual Switch to ethernet:")
        vsw_length = (len(virtual_switches))-1
        count = 0
        while count <= vsw_length:
            print ("%s : %s" % (count, virtual_switches[count]))
            count +=1
        vsw_option = int(input("Virtual Switch: "))
        net_vsw.append(virtual_switches[vsw_option])
        net_vlan.append(input("Ethernet VLAN (%s): " % virtual_switches[vsw_option]))
        net_length = len(net_vsw)-1
        if net_length == 2:
            print ('Sorry. Maximum initial interface is 3. Continuing..')
            break
        netconfiglpar.mkCheck()
        netconfiglpar.answerCheck()

    # verify configuration
    print ("\n[LPAR Configuration Validation]\n"
           "\nCheck configuration last LPAR:\n\n"
           "LPAR name: %s-%s hosted in %s with ID %s\n"
           "Entitled CPU: Minimum: %.1f , Desired: %.1f, Maximum: %.1f\n"
           "Virtual CPU : Minimum: %s , Desired: %s, Maximum: %s\n"
           "Memory      : Minimum: %s , Desired: %s, Maximum: %s"
           % (prefix, lparname, system_vio.getSystem(), freeid.getId(),
              lparentcpumin, lparentcpu, lparentcpumax, lparvcpumin,
              lparvcpu, lparvcpumax, lparmenmin, lparmem, lparmenmax ))
    count = 0
    while count <= net_length:
        print ("Network %s: Virtual Switch: %s - VLAN: %s" % (count, net_vsw[count], net_vlan[count]))
        count += 1
        if net_length == 0:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,\'" % (net_vlan[0],net_vsw[0]))
        elif net_length == 1:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,\'" % (net_vlan[0],net_vsw[0],
                                    net_vlan[1],net_vsw[1]))
        elif net_length == 2:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s\'," % (net_vlan[0],
                                    net_vsw[0], net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))


os.system('clear')
print ("\n\n[ Power Adm ]\n[ Version: %s - © 2014 Kairo Araujo - BSD License ]\n\n" % version)

change = raw_input("Change or Ticket number: ")

file_change = open("tmp/%s_%s.sh" % (change, timestr) , 'w')

configlpar = checkOk('\nThe configuration of last LPAR is OK?(y/n): ', 'n')
newconfiglpar = checkOk('\nDo you want add another LPAR on this Change or Ticket?(y/n)' , 'y')
while configlpar.answerCheck() == 'n':
    while newconfiglpar.answerCheck() == 'y':
        lparconfig()
        configlpar.mkCheck()
        configlpar.answerCheck()
        if configlpar.answerCheck() == 'y':
            print ('Save config')
            file_change.write('%s-%s\n' % (prefix, lparname))
            newconfiglpar.mkCheck()
            newconfiglpar.answerCheck()
            if newconfiglpar.answerCheck() == 'n':
                print ('Encerrando CRQ')

file_change.write('# File closed with success by PowerAdm\n')
file_change.close()
os.system('mv tmp/%s_%s.sh changes/' % (change, timestr))

print (freeid.getId())
print (system_vio.getSystem())
print (system_vio.getVio1())
print (system_vio.getVio2())
print (configlpar.answerCheck())


