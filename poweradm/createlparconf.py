#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# createlparconf.py
#
# Copyright (c) 2014 Kairo Araujo
#
# It was created for personal use. There are no guarantees of the author.
# Use at your own risk.
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
from systemvios import *
from verify import *
from execchange import *
from fields import *
from mklparconf import *

###############################################################################################
#### FRONTEND                                                                              ####
###############################################################################################

def changeconfig():
    print ("\n[CHANGE/TICKET INFORMATION]\n")
    global change
    change = Fields('Change/Ticket', 'Change or Ticket number: ')
    change.chkFieldStr()
    change = change.strVarOut()

# get lpar configuration (mem, cpu etc)
def lparconfig():
    global prefix, lparname, lparentcpu, lparentcpumin, lparentcpumax, lparvcpu
    global lparvcpumin, lparvcpumax, lparmem, lparmenmin, lparmenmax
    global npiv_vio1, npiv_vio2

    print ("\n[LPAR CONFIGURATION ]\n")

    prefix = Fields('Prefix', 'Prefix (XXXX-lparname): ')
    prefix.chkFieldStr()
    prefix = prefix.strVarOut()

    lparname = Fields('LPAR Hostname', 'LPAR Hostname: ')
    lparname.chkFieldStr()
    lparname = lparname.strVarOut()

    check_cpu_config = 0 # check if entitled is 10% >= virtual ('if' down)
    while check_cpu_config == 0:
        while True:
            try:
                lparentcpu = float(raw_input("LPAR Entitled CPU desired: "))
                break
            except (TypeError, ValueError):
                print ('\tERROR: LPAR Entitled needs a flot: Example: 0.1, 1.2, 2.4 etc')

        lparentcpumin = lparentcpu-(lparentcpu*cpu_min/100)
        lparentcpumin = round(lparentcpumin, 1)
        if lparentcpumin < 0.10:
            lparentcpumin = 0.1
        lparentcpumax = (lparentcpu*cpu_max/100)+lparentcpu

        while True:
            try:
                lparvcpu = int(raw_input("LPAR Virtual CPU desired: "))
                break
            except (TypeError, ValueError):
                print('\tERROR: LPAR Virtual needs full cpu: Example: 1, 3, 4 etc')

        lparvcpumin = lparvcpu-(lparvcpu*cpu_min/100)
        if lparvcpumin < 1:
            lparvcpumin = 1
        lparvcpumax = (lparvcpu*cpu_max/100)+lparvcpu

        # check if entitled is 10% >= virtual
        cpu_config = lparentcpu*100/lparvcpu
        if cpu_config >= 10:
            check_cpu_config = 1
        else:
            print ("\tERROR: It's necessary that CPU Entitled is at least 10% of the Virtual")

    while True:
        try:
            lparmem = int(raw_input("LPAR Memory desired: "))
            break
        except (TypeError, ValueError):
            print ('\tERROR: LPAR Memory needs GB value: Example: 8, 10, 20 etc')

    lparmenmin = lparmem-(lparmem*mem_min/100)
    lparmenmax = (lparmem*mem_max/100)+lparmem

    # prepare to os deploy
    global nim_deploy
    if enable_nim_deploy.lower() == 'yes':
        nim_deploy = CheckOK("Do you want prepare LPAR to deploy OS using NIM?(y/n): ", 'n')
        nim_deploy.mkCheck()
	nim_deploy = nim_deploy.answerCheck()

    """ get network to deploy using nim (only if nim deploy is enabled) """
    if nim_deploy == 'y':

        print ("\n[DEPLOY NETWORK SELECTION]\n")
        print ("\033[1;31mImportant: This configuration is temporaly. Used only to deploy!\033[1;00m")
        print ("\033[1;31m           LPAR network configuration is made in [LPAR NETWORK CONFIGURATION]\033[1;00m")
        print ("\nSelect the Virtual Switch to deploy:")
        vsw_length = (len(virtual_switches))-1
        count = 0
        while count <= vsw_length:
            print ("%s : %s" % (count, virtual_switches[count]))
            count +=1

        while True:
            try:
                vsw_option = int(input("Virtual Switch to Deploy: "))
                vsw_deploy = virtual_switches[vsw_option]
                break
            except(IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (vsw_length))

        vlan_deploy = input("VLAN deploy (%s): " % virtual_switches[vsw_option])


    # get free id from newID.py
    global lparid
    freeid = NewID()
    freeid.mkID()
    lparid = freeid.getID()

    # select a system and vios from systemVios.py
    global system, vio1, vio2
    system_vio = SystemVios()
    system_vio.selectSystemVios()
    system = system_vio.getSystem()
    vio1 = system_vio.getVio1()
    vio2 = system_vio.getVio2()

    # SCSI and DISK configuration
    print ("\n[SCSI AND DISK CONFIGURATION]\n")
    global vscsi
    global add_disk
    global vscsi_vio1, vscsi_vio2
    vscsi = CheckOK('Do you want add Virtual SCSI to LPAR? (y/n): ', 'n')
    vscsi.mkCheck()
    vscsi = vscsi.answerCheck()

    if vscsi == 'y':
        global stgpool

        if active_ssp.lower() == 'yes':
            add_disk = CheckOK('\nDo you want add an disk from Storage Pool to LPAR?\n'
                    '**** FUNCTION ALPHA NOT TESTED YET **** (y/n): ', 'n')
            add_disk.mkCheck()
            add_disk = add_disk.answerCheck()

            if add_disk == 'y':
                while True:
                    try:
                        global disk_size
                        disk_size = int(raw_input("Disk Size in GB: "))
                        break
                    except (TypeError, ValueError):
                        print ('\tERROR: Disk Size needs GB value: Example: 10, 15, 50 etc')

                print ("\nSelect the Storage Pool to add:\n")
                storage_pools_length = (len(storage_pools))-1

                if storage_pools_length == 0:
                    global storage_pools_option
                    storage_pool_option = storage_pools[0]
                else:
                    count = 0
                    while count <= storage_pools_length:
                        print ("%s : %s" % (count, storage_pools[count]))
                        count +=1

                    while True:
                        try:
                            storage_pools_option = int(input("Storage Pool: "))
                            stgpool = storage_pools[storage_pools_option]
                            break
                        except (IndexError):
                            print('\tERROR: Select an existing option between 0 and %s.' % (storage_pools_length))
            else:
                disk_size = 0
                add_disk = 'n'
        else:
            stgpool = 'none'
            disk_size = 0
            add_disk = 'n'

    else:
        stgpool = 'none'
        disk_size = 0
        add_disk = 'n'


    # get network configuration
    net_vlan = []
    net_vsw = []
    netconfiglpar = CheckOK('Do you want another network interface (max 3 ethernets)? (y/n): ', 'y')
    while netconfiglpar.answerCheck() == 'y':
        print ("\n[LPAR NETWORK CONFIGURATION]\n")
        if (len(net_vsw) == 0) and (nim_deploy == 'y'):
                print ("\033[1;31mImportant: This is default network config to LPAR!\033[1;00m")
        print ("\nSelect the Virtual Switch to ethernet:")
        vsw_length = (len(virtual_switches))-1
        count = 0
        while count <= vsw_length:
            print ("%s : %s" % (count, virtual_switches[count]))
            count +=1

        while True:
            try:
                vsw_option = int(input("Virtual Switch: "))
                net_vsw.append(virtual_switches[vsw_option])
                break
            except(IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (vsw_length))

        net_vlan.append(input("Ethernet VLAN (%s): " % virtual_switches[vsw_option]))

        # Check if VLAN exists on VIOs
        vlan_list = commands.getoutput('ssh -l poweradm %s lshwres  -r virtualio --rsubtype vswitch -m %s -F | grep %s' %
                (hmcserver, system, virtual_switches[vsw_option]))

        if '%s' % (net_vlan[-1]) not in vlan_list:
            print ("\033[1;31mImportant: VLAN %s need to be registered on VIOS!\033[1;00m" % (net_vlan[-1]))

        net_length = len(net_vsw)-1
        if net_length == 2:
            print ('Sorry. Maximum initial interface is 3. Continuing..')
            break
        netconfiglpar.mkCheck()
        netconfiglpar.answerCheck()


    print ("\n\n[NPIV HBA Configuration]\n")
    global vfc
    vfc = CheckOK('Do you want add Virtual Fiber Adapter (HBA/NPIV)? (y/n): ', 'n')
    vfc.mkCheck()
    vfc = vfc.answerCheck()

    if vfc == 'y':
        # VIOs NPIV selection
        print ("\nFinding on %s the NPIVs availabe.\n"
               "This might take a few minutes...\n" % (vio1))

        # // simulation
        #os.system('cat poweradm/simulation/VIO1A_NPIV')
        #os.system('cat simulation/FCSINFO')
        #os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'cat FCSINFO\'\"' % (hmcserver,
        #          system, vio1))
        # // simulation

        os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
                  system, vio1))

        """ get the file with comments if exists """
        if os.path.isfile('npiv/%s-%s' % ( system, vio1)):
            os.system('cat npiv/%s-%s' % ( system, vio1))

        npiv_vio1 = raw_input('\nWhat HBA (ex: fcs0) you want to use for NPIV to %s?: ' % (vio1))

        print ("\nFinding on %s the NPIVs availabe.\n"
               "This might take a few minutes...\n" % (vio2))

        # // simulation
        #os.system('cat poweradm/simulation/VIO2A_NPIV')
        #os.system('cat simulation/FCSINFO')
        #os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'cat FCSINFO\'\"' % (hmcserver,
        #          system, vio2))
        # // simulation

        os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
                  system, vio2))


        """ get the file with comments if exists """
        if os.path.isfile('npiv/%s-%s' % ( system, vio2)):
            os.system('cat npiv/%s-%s' % ( system, vio2))

        npiv_vio2 = raw_input('\nWhat HBA (ex: fcs0) you want to use for NPIV to %s?: ' % (vio2))

    else:
        npiv_vio1 = 'none'
        npiv_vio2 = 'none'

    # verify configuration
    global veth
    global veth_final
    print ("\n[LPAR Configuration Validation]\n"
           "\nCheck configuration last LPAR:\n")
    print ('*' * 80)
    print ("LPAR name    : %s-%s hosted in %s with ID %s\n"
           "Entitled CPU : Minimum: %.1f , Desired: %.1f, Maximum: %.1f\n"
           "Virtual CPU  : Minimum: %s , Desired: %s, Maximum: %s\n"
           "Memory       : Minimum: %s , Desired: %s, Maximum: %s"
           % (prefix, lparname, system, lparid,
              lparentcpumin, lparentcpu, lparentcpumax, lparvcpumin,
              lparvcpu, lparvcpumax, lparmenmin, lparmem, lparmenmax))

    if vscsi == 'y':
        print("SCSI         : %s: 1%s \t %s: 2%s" % (vio1, lparid, vio2, lparid))

        if active_ssp.lower() == 'yes':
            if add_disk == 'y':
                print("DISK         : %sG" % (disk_size))

    if vfc == 'y':
        print("NPIV         : %s: %s \t %s: %s" % (vio1, npiv_vio1, vio2,
            npiv_vio2))

    count = 0
    while count <= net_length:

        print ("Network %s    : Virtual Switch: %s - VLAN: %s" % (count, net_vsw[count], net_vlan[count]))
        count += 1
        if net_length == 0:
            veth = ("10/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0]))
        elif net_length == 1:
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0],
                                    net_vlan[1],net_vsw[1]))
        elif net_length == 2:
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" % (net_vlan[0],
                                    net_vsw[0], net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))
    print ('*' * 80)


    # temporaly and final NIM deploy virtual ethernet settings
    if nim_deploy == 'y':

        if net_length == 0:
            veth = ("10/0/%s//0/0/%s" % (vlan_deploy, vsw_deploy))
            veth_final = ("10/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0]))

        elif net_length == 1:
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (vlan_deploy, vsw_deploy,
                                    net_vlan[1],net_vsw[1]))

            veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0],
                                    net_vlan[1],net_vsw[1]))

        elif net_length == 2:
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                    (vlan_deploy, vsw_deploy, net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))

            veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                (net_vlan[0], net_vsw[0], net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))
    else:
        veth_final = veth


###############################################################################################
#### MAIN                                                                                  ####
###############################################################################################

def exec_createlparconf():

    changeconfig()

    #
    # verify if lpar is OK and option to add another lpar
    #

    # questions
    configlpar = CheckOK('\nThe configuration of last LPAR is OK?(y/n): ', 'n')
    newconfiglpar = CheckOK('\nDo you want add another LPAR on this Change or Ticket?(y/n): ' , 'y')

    # Count of LPAR
    lpar_count = 0

    # While config is not OK create a config
    while configlpar.answerCheck() == 'n':

        # While want add a new config
        while newconfiglpar.answerCheck() == 'y':

            # check is config ok
            lparconfig()
            newchange = MakeLPARConf(change, prefix, lparname, lparid, nim_deploy, lparmem,
                    lparentcpu, lparvcpu, vscsi, add_disk, stgpool, disk_size, vfc,
                    npiv_vio1, npiv_vio2, veth, veth_final, system, vio1, vio2)

            # verify if is first lpar to create header.
            if lpar_count == 0:
                newchange.headerchange()
                lpar_count += 1

            configlpar.mkCheck()
            configlpar.answerCheck()

            # if config is ok
            if configlpar.answerCheck() == 'y':

                # write the change file
                newchange.writechange()

                # check if want add another config on the change/ticket
                newconfiglpar.mkCheck()
                newconfiglpar.answerCheck()

                # if not end.
                if newconfiglpar.answerCheck() == 'n':
                    print ('Closing the file changes/%s-%s' % (change, timestr))

    newchange.closechange()

    # check if you want executes the change/ticket after creation
    check_exec_createlpar = CheckOK('\nDo you want execute this change/ticket now %s-%s? (y/n): ' %
            (change, timestr), 'n')
    check_exec_createlpar.mkCheck()
    if check_exec_createlpar.answerCheck() == 'y':
        print ('Runing changes/ticket %s-%s' % (change, timestr))
        exec_change_after_creation = ExecChange('%s/poweradm/changes/%s_%s.sh' % (pahome, change, timestr))
        exec_change_after_creation.runChange()
    else:
        print ('Change/Ticket not executed. Storing %s-%s...\nExiting!' %
                (change, timestr))
