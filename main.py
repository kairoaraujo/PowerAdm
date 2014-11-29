#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# main.py
#
# Copyright (c) 2014 Kairo Araujo
#
# This program was created to help in managing vhost devices and its hdisks
# in PowerVM (vios) servers. It was created for personal use. There are no
# guarantees of the author. Use at your own risk.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# Important:
# IBM, PowerVM (a.k.a. vios) are registered trademarks of IBM Corporation in
# the United States, other countries, or both.
#
# Imports
###############################################################################################
import time
import os.path
import commands
from globalvar import *
from config import *
from newid import *
from systemVios import *
from verify import *

###############################################################################################
#### FRONTEND                                                                              ####
###############################################################################################

def headerconfig():
    global change
    os.system('clear')
    print ("\n\n[ Power Adm ]\n[ Version: %s - © 2014 Kairo Araujo - BSD License ]\n\n" % version)

    change = raw_input("Change or Ticket number: ")


# get lpar configuration (mem, cpu etc)
def lparconfig():
    global prefix, lparname, lparentcpu, lparentcpumin, lparentcpumax, lparvcpu
    global lparvcpumin, lparvcpumax, lparmem, lparmenmin, lparmenmax
    global npiv_vio1, npiv_vio2

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

    # VIOs NPIV selection
    print ("\n\n[NPIV HBA Configuration]\n")
    print ("\nFinding on %s the NPIVs availabe.\n"
           "This might take a few minutes...\n" % (system_vio.getVio1()))
    # simulation
    #os.system('cat simulation/VIO1A_NPIV')
    #os.system('cat simulation/FCSINFO')
    os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
              system_vio.getSystem(), system_vio.getVio1()))
    #os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'cat FCSINFO\'\"' % (hmcserver,
    #          system_vio.getSystem(), system_vio.getVio1()))

    npiv_vio1 = raw_input('\nWhat HBA (ex: fcs0) you want to use for NPIV to %s?: ' % (system_vio.getVio1()))

    print ("\nFinding on %s the NPIVs availabe.\n"
           "This might take a few minutes...\n" % (system_vio.getVio2()))
    # simulation
    #os.system('cat simulation/VIO2A_NPIV')
    #os.system('cat simulation/FCSINFO')
    os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
              system_vio.getSystem(), system_vio.getVio2()))
    #os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'cat FCSINFO\'\"' % (hmcserver,
    #          system_vio.getSystem(), system_vio.getVio2()))

    npiv_vio2 = raw_input('\nWhat HBA (ex: fcs0) you want to use for NPIV to %s?: ' % (system_vio.getVio1()))

    # verify configuration
    global virtual_eth_adapters
    print ("\n[LPAR Configuration Validation]\n"
           "\nCheck configuration last LPAR:\n\n"
           "LPAR name: %s-%s hosted in %s with ID %s\n"
           "Entitled CPU: Minimum: %.1f , Desired: %.1f, Maximum: %.1f\n"
           "Virtual CPU : Minimum: %s , Desired: %s, Maximum: %s\n"
           "Memory      : Minimum: %s , Desired: %s, Maximum: %s\n"
           "NPIV        : %s: %s \t %s: %s\n"
           % (prefix, lparname, system_vio.getSystem(), freeid.getId(),
              lparentcpumin, lparentcpu, lparentcpumax, lparvcpumin,
              lparvcpu, lparvcpumax, lparmenmin, lparmem, lparmenmax,
              system_vio.getVio1(), npiv_vio1, system_vio.getVio2(),
              npiv_vio2))
    count = 0
    while count <= net_length:
        print ("Network %s: Virtual Switch: %s - VLAN: %s" % (count, net_vsw[count], net_vlan[count]))
        count += 1
        if net_length == 0:
            virtual_eth_adapters = ("10/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0]))
        elif net_length == 1:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0],
                                    net_vlan[1],net_vsw[1]))
        elif net_length == 2:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" % (net_vlan[0],
                                    net_vsw[0], net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))

###############################################################################################
#### BACKEND                                                                               ####
###############################################################################################

def headerchange():

    global file_change

    file_change = open("tmp/%s_%s.sh" % (change, timestr) , 'w')
    file_change.write("#!/bin/sh\n")


def writechange():

    print ('Writing file %s-%s.sh ... ' % (change, timestr))

    file_change.write("\n\necho 'Creating LPAR %s-%s on %s ...'\n" % (prefix, lparname,
                      system_vio.getSystem()))

    file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                      "lpar_id=%s ,profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                      "desired_mem=%s, max_mem=%s, proc_mode=shared, min_procs=%s,"
                      "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                      "max_proc_units=%s, sharing_mode=uncap, uncap_weight=128, conn_monitoring=1, "
                      "boot_mode=norm, max_virtual_slots=40, "
                      "\\\"virtual_eth_adapters=%s\\\","
                      "\\\"virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\\\"'\n"
                      % ( hmcserver, system_vio.getSystem(), prefix, lparname, freeid.getId(),
                      lparname, lparmenmin*1024, lparmem*1024, lparmenmax*1024, lparvcpumin, lparvcpu,
                      lparvcpumax, lparentcpumin, lparentcpu, lparentcpumax, virtual_eth_adapters,
                      system_vio.getVio1(), freeid.getId(), system_vio.getVio2(), freeid.getId()))

    file_change.write("\n\necho 'Making DLPAR on %s and %s to create FCs'" %
                     ( system_vio.getVio1(), system_vio.getVio2()))

    file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype fc "
                      "-s 3%s -a \'adapter_type=server,remote_lpar_name=%s-%s, remote_slot_num=33\'"
                      % (hmcserver, system_vio.getSystem(), system_vio.getVio1(), freeid.getId(),
                      prefix, lparname ))

    file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype fc "
                      "-s 4%s -a \'adapter_type=server,remote_lpar_name=%s-%s, remote_slot_num=34\'"
                      % (hmcserver, system_vio.getSystem(), system_vio.getVio2(), freeid.getId(),
                      prefix, lparname ))

    file_change.write("\n\necho 'Making cfgdev on %s and %s to reconize new devices'" %
                     ( system_vio.getVio1(), system_vio.getVio2()))

    file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'cfgdev -dev vio0\'\"" %
                     (hmcserver, system_vio.getSystem(), system_vio.getVio1()))

    file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'cfgdev -dev vio0\'\"" %
                     (hmcserver, system_vio.getSystem(), system_vio.getVio2()))

    file_change.write("\n\necho 'Identifying the news vfchost on %s and %s'" %
                     ( system_vio.getVio1(), system_vio.getVio2()))

    file_change.write("\n\nvfchost_vio1=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv\'\""
                      "| grep \"\\-C3%s\" | awk \'{ print $1 }\')" % (hmcserver, system_vio.getSystem(), 
                      system_vio.getVio1(), freeid.getId()))

    file_change.write("\n\nvfchost_vio2=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv\'\""
                      "| grep \"\\-C4%s\" | awk \'{ print $1 }\')" % (hmcserver, system_vio.getSystem(), 
                      system_vio.getVio2(), freeid.getId()))


    # simulation
    #vfchost_vio1 = commands.getoutput("cat simulation/%s| grep \"\\-C3%s\" | awk \'{ print $1 }\'" %
    #                        (system_vio.getVio1(), freeid.getId()))

    #vfchost_vio2 = commands.getoutput("cat simulation/%s| grep \"\\-C4%s\" | awk \'{ print $1 }\'" %
    #                        (system_vio.getVio2(), freeid.getId()))

    #print (vfchost_vio1)
    #print (vfchost_vio2)

    file_change.write("\n\necho 'Making vfcmap on %s and %s to connect the NPIV'" %
                     ( system_vio.getVio1(), system_vio.getVio2()))

    file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'vfcmap -vadapter $vfchost_vio1 -fcp %s\'\""
                      % (hmcserver, system_vio.getSystem(), system_vio.getVio2(), npiv_vio1))

    file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'vfcmap -vadapter $vfchost_vio2 -fcp %s\'\""
                      % (hmcserver, system_vio.getSystem(), system_vio.getVio2(), npiv_vio2))

    file_reservedids_tmp = open('tmp/reserved_ids_%s' %(timestr), 'ab')
    file_reservedids_tmp.write('%s\n' % (freeid.getId()))
    file_reservedids_tmp.close()

def closechange():
    file_change.write('\n\n# File closed with success by PowerAdm\n')
    file_change.close()
    os.system('mv tmp/%s_%s.sh changes/' % (change, timestr))
    os.system('cat tmp/reserved_ids_%s >> data/reserved_ids' % (timestr))

###############################################################################################
#### MAIN                                                                                  ####
###############################################################################################

headerconfig()
headerchange()

configlpar = checkOk('\nThe configuration of last LPAR is OK?(y/n): ', 'n')
newconfiglpar = checkOk('\nDo you want add another LPAR on this Change or Ticket?(y/n)' , 'y')
while configlpar.answerCheck() == 'n':
    while newconfiglpar.answerCheck() == 'y':
        lparconfig()
        configlpar.mkCheck()
        configlpar.answerCheck()
        if configlpar.answerCheck() == 'y':

            writechange()

            newconfiglpar.mkCheck()
            newconfiglpar.answerCheck()
            if newconfiglpar.answerCheck() == 'n':
                print ('Closing the file change/%s-%s' % (change, timestr))

closechange()

