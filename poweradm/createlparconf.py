#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# createlparocnf.py
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
from systemVios import *
from verify import *
from execchange import *
from fields import *

###############################################################################################
#### FRONTEND                                                                              ####
###############################################################################################

def changeconfig():
    print ("\n[Change/Ticket Information]\n")
    global change
    change = Fields('change', 'Change/Ticket', 'Change or Ticket number: ')
    change.chkFieldStr()


# get lpar configuration (mem, cpu etc)
def lparconfig():
    global prefix, lparname, lparentcpu, lparentcpumin, lparentcpumax, lparvcpu
    global lparvcpumin, lparvcpumax, lparmem, lparmenmin, lparmenmax
    global npiv_vio1, npiv_vio2

    print ("\n[LPAR Configuration ]\n")

    prefix = Fields('prefix', 'Prefix', 'Prefix (XXXX-lparname): ')
    prefix.chkFieldStr()

    lparname = Fields('lparname', 'LPAR Hostname', 'LPAR Hostname: ')
    lparname.chkFieldStr()

    check_cpu_config = 0 # check if entitled is 10% >= virtual ('if' down)
    while check_cpu_config == 0:
        while True:
            try:
                lparentcpu = float(raw_input("LPAR Entitled CPU desired: "))
                break
            except (TypeError, ValueError):
                print ('\tERROR: LPAR Entitled needs a flot: Example: 0.1, 1.2, 2.4 etc')

        lparentcpumin = lparentcpu-(lparentcpu*cpu_min/100)
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
        nim_deploy = checkOk("Do you want prepare LPAR to deploy OS using NIM?(y/n): ", 'n')
        nim_deploy.mkCheck()

    # get free id from newId.py
    global freeid
    freeid = newId('newid')
    freeid.mkId()

    # select a system and vios from systemVios.py
    global system_vio
    system_vio = systemVios('system', 'vio1', 'vio2')
    system_vio.selectSystemVios()


    # SCSI and DISK configuration
    print ("\n[SCSI and DISK Configuration]\n")
    global vscsi
    global add_disk
    vscsi = checkOk('Do you want add Virtual SCSI to LPAR? (y/n): ', 'n')
    vscsi.mkCheck()

    if vscsi.answerCheck() == 'y':
        global vscsi_vio1
        global vscsi_vio2
        vscsi_vio1 = ("21/client//%s/1%s/0" % (system_vio.getVio1(), freeid.getId()))
        vscsi_vio2 = ("22/client//%s/2%s/0" % (system_vio.getVio2(), freeid.getId()))

        if active_ssp.lower() == 'yes':
            global num_disk
            add_disk = checkOk('\nDo you want add an disk to LPAR?\n'
                    '**** FUNCTION ALPHA NOT TESTED YET **** (y/n): ', 'n')
            add_disk.mkCheck()

            if add_disk.answerCheck() == 'y':
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
                    storage_pools_option = int(input("Storage Pool: "))

    # get network configuration
    net_vlan = []
    net_vsw = []
    netconfiglpar = checkOk('Do you want another network interface (max 3 ethernets)? (y/n): ', 'y')
    while netconfiglpar.answerCheck() == 'y':
        print ("\n[LPAR Network Configuration]\n"
               "\nSelect the Virtual Switch to ethernet:")
        if (len(net_vsw) == 0) and (nim_deploy.answerCheck() == 'y'):
                print ("\033[1;31mImportant: First ethernet is used to NIM deploy!\033[1;00m")
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


    print ("\n\n[NPIV HBA Configuration]\n")
    global vfc
    vfc = checkOk('Do you want add Virtual Fiber Adapter (HBA/NPIV)? (y/n): ', 'n')
    vfc.mkCheck()
    if vfc.answerCheck() == 'y':
        # VIOs NPIV selection
        print ("\nFinding on %s the NPIVs availabe.\n"
               "This might take a few minutes...\n" % (system_vio.getVio1()))

        # // simulation
        #os.system('cat poweradm/simulation/VIO1A_NPIV')
        #os.system('cat simulation/FCSINFO')
        #os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'cat FCSINFO\'\"' % (hmcserver,
        #          system_vio.getSystem(), system_vio.getVio1()))
        # // simulation

        os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
                  system_vio.getSystem(), system_vio.getVio1()))

        npiv_vio1 = raw_input('\nWhat HBA (ex: fcs0) you want to use for NPIV to %s?: ' % (system_vio.getVio1()))

        print ("\nFinding on %s the NPIVs availabe.\n"
               "This might take a few minutes...\n" % (system_vio.getVio2()))

        # // simulation
        #os.system('cat poweradm/simulation/VIO2A_NPIV')
        #os.system('cat simulation/FCSINFO')
        #os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'cat FCSINFO\'\"' % (hmcserver,
        #          system_vio.getSystem(), system_vio.getVio2()))
        # // simulation

        os.system('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
                  system_vio.getSystem(), system_vio.getVio2()))

        npiv_vio2 = raw_input('\nWhat HBA (ex: fcs0) you want to use for NPIV to %s?: ' % (system_vio.getVio1()))

    # verify configuration
    global virtual_eth_adapters
    print ("\n[LPAR Configuration Validation]\n"
           "\nCheck configuration last LPAR:\n")
    print ('*' * 80)
    print ("LPAR name    : %s-%s hosted in %s with ID %s\n"
           "Entitled CPU : Minimum: %.1f , Desired: %.1f, Maximum: %.1f\n"
           "Virtual CPU  : Minimum: %s , Desired: %s, Maximum: %s\n"
           "Memory       : Minimum: %s , Desired: %s, Maximum: %s"
           % (prefix.strVarOut(), lparname.strVarOut(), system_vio.getSystem(), freeid.getId(),
              lparentcpumin, lparentcpu, lparentcpumax, lparvcpumin,
              lparvcpu, lparvcpumax, lparmenmin, lparmem, lparmenmax))

    if vscsi.answerCheck() == 'y':
        print("SCSI         : %s: 1%s \t %s: 2%s" % (system_vio.getVio1(), freeid.getId(),
              system_vio.getVio2(), freeid.getId()))

        if active_ssp.lower() == 'yes':
            if add_disk.answerCheck() == 'y':
                print("DISK         : %sG" % (disk_size))

    if vfc.answerCheck() == 'y':
        print("NPIV         : %s: %s \t %s: %s" % (system_vio.getVio1(), npiv_vio1, system_vio.getVio2(),
            npiv_vio2))

    count = 0
    while count <= net_length:
        print ("Network %s    : Virtual Switch: %s - VLAN: %s" % (count, net_vsw[count], net_vlan[count]))
        count += 1
        if net_length == 0:
            virtual_eth_adapters = ("10/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0]))
        elif net_length == 1:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan[0],net_vsw[0],
                                    net_vlan[1],net_vsw[1]))
        elif net_length == 2:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" % (net_vlan[0],
                                    net_vsw[0], net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))
    print ('*' * 80)


###############################################################################################
#### BACKEND                                                                               ####
###############################################################################################

def headerchange():

    global file_change

    file_change = open("poweradm/tmp/%s_%s.sh" % (change.strVarOut(), timestr) , 'w')
    file_change.write("#!/bin/sh\n")


def writechange():

    #
    # config functions to write correct action to lpar
    #

    def wchg_creating_lpar(): # message information creating LPAR

        file_change.write("\n\necho 'Creating LPAR %s-%s on %s ...'\n" % (prefix.strVarOut(),
                          lparname.strVarOut(),system_vio.getSystem()))


    def wchg_vio_mkscsi(): # create SCSI on VIO Servers via DLPAR

        file_change.write("\n\necho 'Making DLPAR on %s and %s to create VSCSI'" %
                         ( system_vio.getVio1(), system_vio.getVio2()))

        file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype scsi "
                         "-s 1%s -a \'adapter_type=server,remote_lpar_name=%s-%s,remote_lpar_id=%s,remote_slot_num=21\'"
                         % (hmcserver, system_vio.getSystem(), system_vio.getVio1(), freeid.getId(),
                         prefix.strVarOut(), lparname.strVarOut(), freeid.getId()))

        file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype scsi "
                         "-s 2%s -a \'adapter_type=server,remote_lpar_name=%s-%s,remote_lpar_id=%s,remote_slot_num=22\'"
                         % (hmcserver, system_vio.getSystem(), system_vio.getVio2(), freeid.getId(),
                         prefix.strVarOut(), lparname.strVarOut(), freeid.getId()))


    def wchg_vio_mknpiv(): # create NPIV on VIO Servers via DLPAR

        file_change.write("\n\necho 'Making DLPAR on %s and %s to create FCs'" %
                         ( system_vio.getVio1(), system_vio.getVio2()))

        file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype fc "
                          "-s 3%s -a \'adapter_type=server,remote_lpar_name=%s-%s, remote_slot_num=33\'"
                          % (hmcserver, system_vio.getSystem(), system_vio.getVio1(), freeid.getId(),
                          prefix.strVarOut(), lparname.strVarOut() ))

        file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype fc "
                          "-s 4%s -a \'adapter_type=server,remote_lpar_name=%s-%s, remote_slot_num=34\'"
                          % (hmcserver, system_vio.getSystem(), system_vio.getVio2(), freeid.getId(),
                          prefix.strVarOut(), lparname.strVarOut() ))

    def wchg_vio_cfgdev(): # make cfgdev on VIOs

        file_change.write("\n\necho 'Making cfgdev on %s and %s to reconize new devices'" %
                     ( system_vio.getVio1(), system_vio.getVio2()))

        file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'cfgdev -dev vio0\'\"" %
                     (hmcserver, system_vio.getSystem(), system_vio.getVio1()))

        file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'cfgdev -dev vio0\'\"" %
                     (hmcserver, system_vio.getSystem(), system_vio.getVio2()))


    def wchg_vio_vfcmap(): # make vfcmap on VIOS

        # ---> simulation
        #file_change.write("\n\nvfchost_vio1=$(cat simulation/%s| grep \"\\-C3%s\" | awk \'{ print $1 }\')" %
        #                 (system_vio.getVio1(), freeid.getId()))
        #
        #file_change.write("\n\nvfchost_vio2=$(cat simulation/%s| grep \"\\-C4%s\" | awk \'{ print $1 }\')" %
        #                 (system_vio.getVio2(), freeid.getId()))
        # ---  simulation

        file_change.write("\n\necho 'Making vfcmap on %s and %s to connect the NPIV'" %
                         ( system_vio.getVio1(), system_vio.getVio2()))


        file_change.write("\n\nvfchost_vio1=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv\'\""
                          "| grep \"\\-C3%s \" | awk \'{ print $1 }\')" % (hmcserver, system_vio.getSystem(),
                          system_vio.getVio1(), freeid.getId()))

        file_change.write("\n\nvfchost_vio2=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv\'\""
                          "| grep \"\\-C4%s \" | awk \'{ print $1 }\')" % (hmcserver, system_vio.getSystem(),
                          system_vio.getVio2(), freeid.getId()))

        # <--- simulation

        file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'vfcmap -vadapter "
                          "$vfchost_vio1 -fcp %s\'\"" % (hmcserver, system_vio.getSystem(),
                          system_vio.getVio1(), npiv_vio1))

        file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'vfcmap -vadapter "
                          "$vfchost_vio2 -fcp %s\'\"" % (hmcserver, system_vio.getSystem(),
                              system_vio.getVio2(), npiv_vio2))


    def wchg_vio_mkbdsp(): # add disk LPAR

        file_change.write("\n\necho 'Adding disk with %s to %s-%s via %s ONLY'" %
                         (disk_size, prefix.strVarOut(), lparname.strVarOut(), system_vio.getVio1()))

        file_change.write("\n\nvhost_vio1=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all\'\""
                          "| grep \"\\-C1%s \" | awk \'{ print $1 }\')" % (hmcserver, system_vio.getSystem(),
                          system_vio.getVio1(), freeid.getId()))

        file_change.write("\n\nvhost_vio2=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all\'\""
                          "| grep \"\\-C2%s \" | awk \'{ print $1 }\')" % (hmcserver, system_vio.getSystem(),
                          system_vio.getVio2(), freeid.getId()))

        file_change.write("\n\nssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'mkbdsp -clustername "
                          "%s -sp %s %sG -bd %s_lu1 -thick -vadapter $vhost_vio1 -tn %s_rootvg\'\"" %
                          (hmcserver, system_vio.getSystem(), system_vio.getVio1(), cluster_name,
                           storage_pools[storage_pools_option], disk_size, lparname.strVarOut(),
                           lparname.strVarOut()))

    def wchg_lpar(): # LPAR with Ethernet Only

        file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                "boot_mode=%s, max_virtual_slots=40, "
                "\\\"virtual_eth_adapters=%s\\\"'\n"
                % ( hmcserver, system_vio.getSystem(), prefix.strVarOut(), lparname.strVarOut(), freeid.getId(),
                    lparname.strVarOut(), lparmenmin*1024, lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                    lparvcpu, lparvcpumax, lparentcpumin, lparentcpu, lparentcpumax, sharing_mode,
                    uncap_weight, conn_monitoring, boot_mode, virtual_eth_adapters))


    def wchg_lpar_fc(): # LPAR with Ethernet and Fiber Channel

        file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                "boot_mode=%s, max_virtual_slots=40, "
                "\\\"virtual_eth_adapters=%s\\\","
                "\\\"virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\\\"'\n"
                % ( hmcserver, system_vio.getSystem(), prefix.strVarOut(), lparname.strVarOut(), freeid.getId(),
                    lparname.strVarOut(), lparmenmin*1024, lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                    lparvcpu, lparvcpumax, lparentcpumin, lparentcpu, lparentcpumax, sharing_mode,
                    uncap_weight, conn_monitoring, boot_mode, virtual_eth_adapters,
                    system_vio.getVio1(), freeid.getId(), system_vio.getVio2(), freeid.getId()))

    def wchg_lpar_fc_wwnget(): # Get physical and LPAR NPIV wwn

        file_change.write("\n\necho 'Getting Physical and LPAR %s-%s NPIV'" %
                         (prefix.strVarOut(), lparname.strVarOut()))

        file_change.write("\n\necho 'Physical Adapter to LPAR fcs0: '$(ssh -l poweradm %s viosvrcmd -m %s -p %s "
                         "-c \"\'lsdev -dev %s -vpd\'\" | grep \'Network Address\' | cut -d. -f14)" %
						 (hmcserver, system_vio.getSystem(), system_vio.getVio1(), npiv_vio1))

        file_change.write("\n\necho 'Physical Adapter to LPAR fcs1: '$(ssh -l poweradm %s viosvrcmd -m %s -p %s "
                         "-c \"\'lsdev -dev %s -vpd\'\" | grep \'Network Address\' | cut -d. -f14)" %
                         (hmcserver, system_vio.getSystem(), system_vio.getVio2(), npiv_vio2))

        file_change.write("\n\nssh -l poweradm %s lssyscfg -r prof -m %s -F virtual_fc_adapters --filter "
                          "lpar_names=%s-%s| awk -F \'/\' \'{ print \"fcs0 (active,inactive):\\t\"$6\"\\nfcs1 "
                          "(active,inactive):\\t\"$12 }\'" % (hmcserver, system_vio.getSystem(),
                            prefix.strVarOut(), lparname.strVarOut()))


    def wchg_lpar_scsi(): # LPAR with Ethernet and SCSI


        file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                "boot_mode=%s, max_virtual_slots=40, "
                "\\\"virtual_eth_adapters=%s\\\","
                "\\\"virtual_scsi_adapters=%s,%s\\\"'\n"
                % ( hmcserver, system_vio.getSystem(), prefix.strVarOut(), lparname.strVarOut(), freeid.getId(),
                    lparname.strVarOut(), lparmenmin*1024, lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                    lparvcpu, lparvcpumax, lparentcpumin, lparentcpu, lparentcpumax, sharing_mode,
                    uncap_weight, conn_monitoring, boot_mode, virtual_eth_adapters, vscsi_vio1, vscsi_vio2))


    def wchg_lpar_fc_scsi(): # Ethernet, SCSI and Fiber Channel

        file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                "boot_mode=%s, max_virtual_slots=40, "
                "\\\"virtual_eth_adapters=%s\\\","
                "\\\"virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\\\","
                "\\\"virtual_scsi_adapters=%s,%s\\\"'\n"
                % ( hmcserver, system_vio.getSystem(), prefix.strVarOut(), lparname.strVarOut(), freeid.getId(),
                    lparname.strVarOut(), lparmenmin*1024, lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                    lparvcpu, lparvcpumax, lparentcpumin, lparentcpu, lparentcpumax, sharing_mode,
                    uncap_weight, conn_monitoring, boot_mode, virtual_eth_adapters,
                    system_vio.getVio1(), freeid.getId(), system_vio.getVio2(), freeid.getId(), vscsi_vio1,
                    vscsi_vio2))

    def wchg_hmc_savecurrentconf():

        file_change.write("\n\necho 'Saving %s and %s current configuration'" %
                         ( system_vio.getVio1(), system_vio.getVio2()))

        file_change.write("\n\nssh %s -l poweradm mksyscfg -r prof -m %s -o save -p %s -n $(ssh %s -l poweradm "
                          "lssyscfg -r lpar -m %s --filter \"lpar_names=%s\" -F curr_profile) --force" %
                         (hmcserver, system_vio.getSystem(), system_vio.getVio1(), hmcserver, system_vio.getSystem(),
                          system_vio.getVio1()))

        file_change.write("\n\nssh %s -l poweradm mksyscfg -r prof -m %s -o save -p %s -n $(ssh %s -l poweradm "
                          "lssyscfg -r lpar -m %s --filter \"lpar_names=%s\" -F curr_profile) --force" %
                         (hmcserver, system_vio.getSystem(), system_vio.getVio2(), hmcserver, system_vio.getSystem(),
                          system_vio.getVio2()))

    def wchg_lpar_deploy_nim_enable():

        file_change.write("\n\necho 'Enabling Deploy to %s-%s'" % (prefix.strVarOut(), lparname.strVarOut()))

        file_change.write("\n\necho '#PREFIX %s' > poweradm/nim/%s-%s.nim" % (prefix.strVarOut(), prefix.strVarOut(),
            lparname.strVarOut()))

        file_change.write("\n\necho '#LPARNAME %s' >> poweradm/nim/%s-%s.nim" % (lparname.strVarOut(),
            prefix.strVarOut(), lparname.strVarOut()))

        file_change.write("\n\necho '#FRAME %s' >> poweradm/nim/%s-%s.nim" % (system_vio.getSystem(),
            prefix.strVarOut(), lparname.strVarOut()))


    #
    # End Of wchg_...
    #

    #
    # Function writechange() starts here
    #

    print ('Writing file %s-%s.sh ... ' % (change.strVarOut(), timestr))

    file_change.write("\n\n#LPARID %s" % (freeid.getId()))

    if (vscsi.answerCheck()) == 'y' and (vfc.answerCheck()) == 'y':

        wchg_creating_lpar()
        wchg_lpar_fc_scsi()
        wchg_vio_mkscsi()
        wchg_vio_mknpiv()
        wchg_vio_cfgdev()
        wchg_vio_vfcmap()
        if active_ssp.lower() == 'y':
            if (add_disk.answerCheck() == 'y'):
                wchg_vio_mkbdsp()
        wchg_hmc_savecurrentconf()
        wchg_lpar_fc_wwnget()
        if nim_deploy.answerCheck() == 'y':
            wchg_lpar_deploy_nim_enable()

    if (vscsi.answerCheck()) == 'y' and (vfc.answerCheck()) == 'n':

        wchg_creating_lpar()
        wchg_lpar_scsi()
        wchg_vio_mkscsi()
        wchg_vio_cfgdev()
        if active_ssp.lower() == 'y':
            if (add_disk.answerCheck() == 'y'):
                wchg_vio_mkbdsp()
        wchg_hmc_savecurrentconf()
        if nim_deploy.answerCheck() == 'y':
            wchg_lpar_deploy_nim_enable()

    if (vscsi.answerCheck()) == 'n' and (vfc.answerCheck()) == 'y':

        wchg_creating_lpar()
        wchg_lpar_fc()
        wchg_vio_mknpiv()
        wchg_vio_cfgdev()
        wchg_vio_vfcmap()
        wchg_hmc_savecurrentconf()
        wchg_lpar_fc_wwnget()
        if nim_deploy.answerCheck() == 'y':
            wchg_lpar_deploy_nim_enable()


    if (vscsi.answerCheck()) == 'n' and (vfc.answerCheck()) == 'n':

        wchg_creating_lpar()
        wchg_lpar()
        if nim_deploy.answerCheck() == 'y':
            wchg_lpar_deploy_nim_enable()

    file_reservedids_tmp = open('poweradm/tmp/reserved_ids_%s' %(timestr), 'ab')
    file_reservedids_tmp.write('%s\n' % (freeid.getId()))
    file_reservedids_tmp.close()

def closechange():
    file_change.write('\n\n# File closed with success by PowerAdm\n')
    file_change.close()
    os.system('mv poweradm/tmp/%s_%s.sh poweradm/changes/' % (change.strVarOut(), timestr))
    os.system('cat poweradm/tmp/reserved_ids_%s >> poweradm/data/reserved_ids' % (timestr))

###############################################################################################
#### MAIN                                                                                  ####
###############################################################################################

def exec_createlparconf():

    changeconfig()
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
                    print ('Closing the file changes/%s-%s' % (change.strVarOut(), timestr))

    closechange()

    # check if you want executes the change/ticket after creation
    check_exec_createlpar = checkOk('\nDo you want execute this change/ticket now %s-%s? (y/n): ' %
            (change.strVarOut(), timestr), 'n')
    check_exec_createlpar.mkCheck()
    if check_exec_createlpar.answerCheck() == 'y':
        print ('Runing changes/ticket %s-%s' % (change.strVarOut(), timestr))
        exec_change_after_creation = ExecChange('%s_%s.sh' % (change.strVarOut(), timestr))
        exec_change_after_creation.runChange()
    else:
        print ('Change/Ticket not executed. Storing %s-%s...\nExiting!' %
                (change.strVarOut(), timestr))
