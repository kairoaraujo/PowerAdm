#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
mklparconf.py

Copyright (c) 2014, 2015 Kairo Araujo

It was created for personal use. There are no guarantees of the author.
Use at your own risk.

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

IBM, Power, PowerVM (a.k.a. VIOS) are registered trademarks of IBM Corporation in
the United States, other countries, or both.
VMware, vCenter, vCenter Orchestrator are registered trademarks of VWware Inc in the United
States, other countries, or both.
'''

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


class MakeLPARConf():
    ''' Create on config.pahome/poweradm/changes/ the shell script file to create LPAR.

        Args:
          change          Change or Ticket number (string without spaces)
          prefix          LPAR Prefix [PREFIX-lparname] (string without spaces)
          lparname        LPAR name [prefix-LPARNAME] (string without spaces)
          lparid          LPAR ID number (ex: 32)
          nim_deploy      yes/no (Enabled or Disabled)
          lparmem         LPAR Desired Memory in GB (int) ex: 10
          lparentcpu      LPAR Entitled CPU (float) ex: 0.8
          lparvcpu        LPAR virtual CPU (int) ex: 10
          vscsi           yes/no (Create virtual SCSI)
          add_disk        yes/no (Add disk)
          stgpool         Storage Pool to use (string without spaces)
          disk_size       Disk Size in GB (int) ex: 50
          vfc             yes/no (Virtual Fiber Channel)
          npiv_vio1       The physical interface for NPIV (string) (ex. fcs0)
          npiv_vio2       The physical interface for NPIV (string) (ex. fcs1)
          veth            LPAR Ethernets (string)
                          Ex: "10/0/VLAN//0/0/VSW,11/0/VLAN//0/0/VSW,12/0/VLAN//0/0/VSW"
                          VLAN is the VLAN ID
                          VSW is the specific name of Virtual Switch in Power System.
          veth_final      Same veth string (first is temporary and that is final)
          system          The system name (string without spaces)
          vio1            Name of LPAR Name of VIO1 (PowerVM)
          vio2            Name of LPAR Name of VIO2 (PowerVM)
    '''

    def __init__(self, change, prefix, lparname, lparid, nim_deploy, lparmem, lparentcpu,
            lparvcpu, vscsi, add_disk, stgpool, disk_size, vfc, npiv_vio1, npiv_vio2,
            veth, veth_final, system, vio1, vio2):
        ''' Receive the arguments. '''

        self.change = change                    # change ID
        self.prefix = prefix                    # LPAR prefix (XXXX-lparname)
        self.lparname = lparname                # LPAR name/hostname
        self.lparid = lparid                    # ID da LPAR
        self.nim_deploy = nim_deploy            # Use NIM Server deploy y/n
        self.lparmem = lparmem                  # Memory of LPAR
        self.lparentcpu = lparentcpu            # Entitle CPU of LPAR
        self.lparvcpu = lparvcpu                # Virtual CPU of LPAR
        self.vscsi = vscsi                      # Use virtual scsi y/n
        self.add_disk = add_disk                # Add new disk y/n
        self.stgpool = stgpool                  # Storage pool name
        self.disk_size = disk_size              # Disk size em GB (int)
        self.vfc = vfc                          # Use Virtual FC/HBA y/n
        self.npiv_vio1 = npiv_vio1              # Virtual FC/HBA on VIO1
        self.npiv_vio2 = npiv_vio2              # Virtual FC/HBA on VIO2
        self.veth = veth                        # Ethernet adapters (C10 Deploy NIM if nim_deploy is y)
        self.veth_final = veth_final            # Ethernet adapters config final (modify C10 after deploy)
        self.system = system                    # System to host LPAR
        self.vio1 = vio1                        # VIO1 to host LPAR
        self.vio2 = vio2                        # VIO2 to host LPAR

        #
        # Minimal and Maximum CPU and Memory
        #

        # global variables
        global lparmenmin, lparmenmax, lparentcpumin, lparentcpumax, lparvcpumin, lparvcpumax

        # calcule the lpar memory min and max
        lparmenmin = self.lparmem-(self.lparmem*mem_min/100)
        lparmenmax = (self.lparmem*mem_max/100)+self.lparmem

        # verify entitle cpu and set min and maximum
        lparentcpumin = self.lparentcpu-(self.lparentcpu*cpu_min/100)
        lparentcpumin = round(lparentcpumin, 1)
        if lparentcpumin < 0.10:
            lparentcpumin = 0.1
        lparentcpumax = (self.lparentcpu*cpu_max/100)+self.lparentcpu

        # verify virtual cpu (if min cpu is < 1) and set min and max
        lparvcpumin = self.lparvcpu-(self.lparvcpu*cpu_min/100)
        if lparvcpumin < 1:
            lparvcpumin = 1
        lparvcpumax = (self.lparvcpu*cpu_max/100)+self.lparvcpu


        #
        # set default values vscsi
        #
        global vscsi_vio1, vscsi_vio2
        vscsi_vio1 = ("21/client//%s/1%s/0" % (vio1, lparid))
        vscsi_vio2 = ("22/client//%s/2%s/0" % (vio2, lparid))

    def headerchange(self):
        ''' Write the header of file. '''

        global file_change

        file_change = open("%s/poweradm/tmp/%s_%s.sh" % (pahome, self.change, timestr) , 'w')
        file_change.write("#!/bin/sh\n")


    def writechange(self):
        ''' Write the body of file. '''

        #
        # config functions to write correct action to lpar
        #

        def wchg_checksh():
            ''' Write the test of commands. '''
            file_change.write("\nif [ $? != 0 ];"
                              "then\n"
                              "\techo 'An error has occurred. Check the actions taken.'; \n"
                              "\texit;\n"
                              "else\n"
                              "\techo 'Command OK. Continuing';\n"
                              "fi\n")

        def wchg_creating_lpar(): # message information creating LPAR
            ''' Write the message of creating LPAR. '''

            file_change.write("\n\necho 'Creating LPAR %s-%s on %s ...'\n" % (self.prefix, self.lparname,
                self.system))


        def wchg_vio_mkscsi(): # create SCSI on VIO Servers via DLPAR
            ''' Write the SCSI creation on VIO using DLPAR. '''

            file_change.write("\n\necho 'Making DLPAR on %s to create VSCSI'" % (self.vio1))
            file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype scsi "
                             "-s 1%s -a \'adapter_type=server,remote_lpar_name=%s-%s,remote_lpar_id=%s,remote_slot_num=21\'"
                             % (hmcserver, self.system, self.vio1, self.lparid,
                             self.prefix, self.lparname, self.lparid))

            wchg_checksh()

            file_change.write("\n\necho 'Making DLPAR on %s to create VSCSI'" %
                         (self.vio2))

            file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype scsi "
                             "-s 2%s -a \'adapter_type=server,remote_lpar_name=%s-%s,remote_lpar_id=%s,remote_slot_num=22\'"
                             % (hmcserver, self.system, self.vio2, self.lparid,
                             self.prefix, self.lparname, self.lparid))

            wchg_checksh()

        def wchg_vio_mknpiv(): # create NPIV on VIO Servers via DLPAR
            ''' Write the FC/NPIV creation on VIO using DLPAR. '''

            file_change.write("\n\necho 'Making DLPAR on %s to create FCs'" %
                             (self.vio1))

            file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype fc "
                              "-s 3%s -a \'adapter_type=server,remote_lpar_name=%s-%s, remote_slot_num=33\'"
                              % (hmcserver, self.system, self.vio1, self.lparid,
                              self.prefix, self.lparname ))
            wchg_checksh()

            file_change.write("\n\necho 'Making DLPAR on %s to create FCs'" %
                             (self.vio2))

            file_change.write("\n\nssh %s -l poweradm chhwres -r virtualio -m %s -o a -p %s --rsubtype fc "
                              "-s 4%s -a \'adapter_type=server,remote_lpar_name=%s-%s, remote_slot_num=34\'"
                              % (hmcserver, self.system, self.vio2, self.lparid,
                              self.prefix, self.lparname ))
            wchg_checksh()

        def wchg_vio_cfgdev(): # make cfgdev on VIOs
            ''' Write the cfgdev on VIO. '''

            file_change.write("\n\necho 'Making cfgdev on %s to reconize new devices'" %
                             (self.vio1))

            file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'cfgdev -dev vio0\'\"" %
                             (hmcserver, self.system, self.vio1))

            wchg_checksh()

            file_change.write("\n\necho 'Making cfgdev on %s to reconize new devices'" %
                             (self.vio2))

            file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'cfgdev -dev vio0\'\"" %
                             (hmcserver, self.system, self.vio2))

            wchg_checksh()


        def wchg_vio_vfcmap(): # make vfcmap on VIOS
            ''' Write the vfcmap on VIO.'''

            file_change.write("\n\necho 'Getting vfchost on %s to connect the NPIV'" %
                             (self.vio1))

            file_change.write("\n\nvfchost_vio1=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv\'\""
                              "| grep \"\\-C3%s \" | awk \'{ print $1 }\')" % (hmcserver, self.system,
                              self.vio1, self.lparid))
            wchg_checksh()


            file_change.write("\n\necho 'Getting vfchost on %s to connect the NPIV'" %
                             (self.vio2))

            file_change.write("\n\nvfchost_vio2=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv\'\""
                              "| grep \"\\-C4%s \" | awk \'{ print $1 }\')" % (hmcserver, self.system,
                              self.vio2, self.lparid))
            wchg_checksh()


            file_change.write("\n\necho 'Making vfcmap on %s to connect the NPIV'" %
                             ( self.vio1))

            file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'vfcmap -vadapter "
                              "$vfchost_vio1 -fcp %s\'\"" % (hmcserver, self.system,
                              self.vio1, self.npiv_vio1))
            wchg_checksh()

            file_change.write("\n\necho 'Making vfcmap on %s to connect the NPIV'" %
                             (self.vio2))

            file_change.write("\n\nssh %s -l poweradm viosvrcmd -m %s -p %s -c \"\'vfcmap -vadapter "
                              "$vfchost_vio2 -fcp %s\'\"" % (hmcserver, self.system,
                              self.vio2, self.npiv_vio2))
            wchg_checksh()


        def wchg_vio_mkbdsp(): # add disk LPAR
            ''' Write the disk add on LPAR.'''

            file_change.write("\n\necho 'Adding disk with %s to %s-%s via %s ONLY'" %
                             (self.disk_size, self.prefix, self.lparname, self.vio1))

            file_change.write("\n\nvhost_vio1=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all\'\""
                              "| grep \"\\-C1%s \" | awk \'{ print $1 }\')" % (hmcserver, self.system,
                              self.vio1, self.lparid))
            wchg_checksh()

            file_change.write("\n\nvhost_vio2=$(ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all\'\""
                              "| grep \"\\-C2%s \" | awk \'{ print $1 }\')" % (hmcserver, self.system,
                              self.vio2, self.lparid))
            wchg_checksh()

            file_change.write("\n\nssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'mkbdsp -clustername "
                              "%s -sp %s %sG -bd %s_lu1 -thick -vadapter $vhost_vio1 -tn %s_rootvg\'\"" %
                              (hmcserver, self.system, self.vio1, cluster_name,
                               self.stgpool, self.disk_size, self.lparname,
                               self.lparname))
            wchg_checksh()

        def wchg_lpar(): # LPAR with Ethernet Only
            ''' Write LPAR (with Ethernet Only) creation. '''

            file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                    "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                    "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                    "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                    "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                    "boot_mode=%s, max_virtual_slots=40, "
                    "\\\"virtual_eth_adapters=%s\\\"'\n"
                    % ( hmcserver, self.system, self.prefix, self.lparname, self.lparid,
                        self.lparname, lparmenmin*1024, self.lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                        self.lparvcpu, lparvcpumax, lparentcpumin, self.lparentcpu, lparentcpumax, sharing_mode,
                        uncap_weight, conn_monitoring, boot_mode, self.veth))
            wchg_checksh()


        def wchg_lpar_fc(): # LPAR with Ethernet and Fiber Channel
            ''' Write LPAR (Ethernet and Fiber Channel) creation. '''

            file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                    "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                    "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                    "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                    "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                    "boot_mode=%s, max_virtual_slots=40, "
                    "\\\"virtual_eth_adapters=%s\\\","
                    "\\\"virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\\\"'\n"
                    % ( hmcserver, self.system, self.prefix, self.lparname, self.lparid,
                        self.lparname, lparmenmin*1024, self.lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                        self.lparvcpu, lparvcpumax, lparentcpumin, self.lparentcpu, lparentcpumax, sharing_mode,
                        uncap_weight, conn_monitoring, boot_mode, self.veth,
                        self.vio1, self.lparid, self.vio2, self.lparid))
            wchg_checksh()


        def wchg_lpar_scsi(): # LPAR with Ethernet and SCSI
            ''' Write LPAR (Ethernet and SCSI) creation. '''

            file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                    "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                    "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                    "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                    "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                    "boot_mode=%s, max_virtual_slots=40, "
                    "\\\"virtual_eth_adapters=%s\\\","
                    "\\\"virtual_scsi_adapters=%s,%s\\\"'\n"
                    % ( hmcserver, self.system, self.prefix, self.lparname, self.lparid,
                        self.lparname, lparmenmin*1024, self.lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                        self.lparvcpu, lparvcpumax, lparentcpumin, self.lparentcpu, lparentcpumax, sharing_mode,
                        uncap_weight, conn_monitoring, boot_mode, self.veth, vscsi_vio1, vscsi_vio2))

            wchg_checksh()

        def wchg_lpar_fc_scsi(): # Ethernet, SCSI and Fiber Channel
            ''' Write LPAR (Ethernet, Fiber Channel and SCSI) creation. '''

            file_change.write("\nssh %s -l poweradm mksyscfg -r lpar -m %s -i \'name=%s-%s, "
                    "lpar_id=%s, profile_name=%s, lpar_env=aixlinux, min_mem=%s, "
                    "desired_mem=%s, max_mem=%s, proc_mode=%s, min_procs=%s,"
                    "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                    "max_proc_units=%s, sharing_mode=%s, uncap_weight=%s, conn_monitoring=%s, "
                    "boot_mode=%s, max_virtual_slots=40, "
                    "\\\"virtual_eth_adapters=%s\\\","
                    "\\\"virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\\\","
                    "\\\"virtual_scsi_adapters=%s,%s\\\"'\n"
                    % ( hmcserver, self.system, self.prefix, self.lparname, self.lparid,
                        self.lparname, lparmenmin*1024, self.lparmem*1024, lparmenmax*1024, proc_mode, lparvcpumin,
                        self.lparvcpu, lparvcpumax, lparentcpumin, self.lparentcpu, lparentcpumax, sharing_mode,
                        uncap_weight, conn_monitoring, boot_mode, self.veth,
                        self.vio1, self.lparid, self.vio2, self.lparid, vscsi_vio1,
                        vscsi_vio2))
            wchg_checksh()

        def wchg_hmc_savecurrentconf():
            ''' Write save current configuration '''

            file_change.write("\n\necho 'Saving %s current configuration'" %
                             (self.vio1))

            file_change.write("\n\nssh %s -l poweradm mksyscfg -r prof -m %s -o save -p %s -n $(ssh %s -l poweradm "
                              "lssyscfg -r lpar -m %s --filter \"lpar_names=%s\" -F curr_profile) --force" %
                             (hmcserver, self.system, self.vio1, hmcserver, self.system,
                              self.vio1))
            wchg_checksh()

            file_change.write("\n\necho 'Saving %s current configuration'" %
                             ( self.vio2))

            file_change.write("\n\nssh %s -l poweradm mksyscfg -r prof -m %s -o save -p %s -n $(ssh %s -l poweradm "
                              "lssyscfg -r lpar -m %s --filter \"lpar_names=%s\" -F curr_profile) --force" %
                             (hmcserver, self.system, self.vio2, hmcserver, self.system,
                              self.vio2))
            wchg_checksh()

        def wchg_lpar_deploy_nim_enable():
            ''' Write NIM enabled to future deploy '''

            file_change.write("\n\necho 'Enabling Deploy to %s-%s'" % (self.prefix, self.lparname))

            file_change.write("\n\necho '#PREFIX %s' > %s/poweradm/nim/%s-%s.nim" % (self.prefix, pahome, self.prefix,
                                self.lparname))
            wchg_checksh()

            file_change.write("\n\necho '#LPARNAME %s' >> %s/poweradm/nim/%s-%s.nim" % (self.lparname, pahome,
                                self.prefix, self.lparname))
            wchg_checksh()

            file_change.write("\n\necho '#FRAME %s' >> %s/poweradm/nim/%s-%s.nim" % (self.system, pahome,
                                self.prefix, self.lparname))
            wchg_checksh()

            file_change.write("\n\necho '#VLAN_FINAL %s' >> %s/poweradm/nim/%s-%s.nim" % ( self.veth_final, pahome,
                                self.prefix, self.lparname))
            wchg_checksh()

        def wchg_lpar_fc_wwnget(): # Get physical and LPAR NPIV wwn
            ''' Write the get informations about NPIV WWNs'''

            file_change.write("\n\necho 'Getting Physical and LPAR %s-%s NPIV'" %
                             (self.prefix, self.lparname))

            file_change.write("\n\necho '' ")

            file_change.write("\n\necho '*************************************************************' ")

            file_change.write("\n\necho 'Physical HBA and LPAR %s-%s NPIV:'" %
                             (self.prefix, self.lparname))

            file_change.write("\n\necho 'Physical Adapter to LPAR fcs0: '$(ssh -l poweradm %s viosvrcmd -m %s -p %s "
                             "-c \"\'lsdev -dev %s -vpd\'\" | grep \'Network Address\' | cut -d. -f14)" %
            		    	 (hmcserver, self.system, self.vio1, self.npiv_vio1))

            file_change.write("\n\necho 'Physical Adapter to LPAR fcs1: '$(ssh -l poweradm %s viosvrcmd -m %s -p %s "
                             "-c \"\'lsdev -dev %s -vpd\'\" | grep \'Network Address\' | cut -d. -f14)" %
                             (hmcserver, self.system, self.vio2, self.npiv_vio2))

            file_change.write("\n\nssh -l poweradm %s lssyscfg -r prof -m %s -F virtual_fc_adapters --filter "
                              "lpar_names=\'%s-%s\' | awk -F \'/\' \'{ print \"fcs0 (active,inactive):\\t\"$6\"\\nfcs1 "
                              "(active,inactive):\\t\"$12 }\'" % (hmcserver, self.system,
                                self.prefix, self.lparname))

            file_change.write("\n\necho '*************************************************************' ")

            file_change.write("\n\necho '' ")


        #
        # End Of wchg_...
        #

        #
        # Function writechange() starts here
        #

        print ('Writing file %s-%s.sh ... ' % (self.change, timestr))

        file_change.write("\n\n#LPARID %s" % (self.lparid))

        if self.vscsi == 'y' and self.vfc == 'y':

            wchg_creating_lpar()
            wchg_lpar_fc_scsi()
            wchg_vio_mkscsi()
            wchg_vio_mknpiv()
            wchg_vio_cfgdev()
            wchg_vio_vfcmap()
            if active_ssp.lower() == 'yes':
                print (self.add_disk)
                if (self.add_disk == 'y'):
                    wchg_vio_mkbdsp()
            wchg_hmc_savecurrentconf()
            if self.nim_deploy == 'y':
                wchg_lpar_deploy_nim_enable()
            wchg_lpar_fc_wwnget()

        if self.vscsi == 'y' and self.vfc == 'n':

            wchg_creating_lpar()
            wchg_lpar_scsi()
            wchg_vio_mkscsi()
            wchg_vio_cfgdev()
            if active_ssp.lower() == 'yes':
                print (self.add_disk)
                if (self.add_disk == 'y'):
                    wchg_vio_mkbdsp()
            wchg_hmc_savecurrentconf()
            if self.nim_deploy == 'y':
                wchg_lpar_deploy_nim_enable()

        if self.vscsi == 'n' and self.vfc == 'y':

            wchg_creating_lpar()
            wchg_lpar_fc()
            wchg_vio_mknpiv()
            wchg_vio_cfgdev()
            wchg_vio_vfcmap()
            wchg_hmc_savecurrentconf()
            if self.nim_deploy == 'y':
                wchg_lpar_deploy_nim_enable()
            wchg_lpar_fc_wwnget()

        if self.vscsi == 'n' and self.vfc == 'n':

            wchg_creating_lpar()
            wchg_lpar()
            if self.nim_deploy == 'y':
                wchg_lpar_deploy_nim_enable()

        file_reservedids_tmp = open('%s/poweradm/tmp/reserved_ids_%s' %(pahome, timestr), 'ab')
        file_reservedids_tmp.write('%s\n' % (self.lparid))
        file_reservedids_tmp.close()

    def closechange(self):
        ''' Close the file and move to correct directory '''

        file_change.write('\n\n# File closed with success by PowerAdm\n')
        file_change.close()
        os.system('mv %s/poweradm/tmp/%s_%s.sh %s/poweradm/changes/' % (pahome, self.change, timestr, pahome))
        os.system('cat %s/poweradm/tmp/reserved_ids_%s >> %s/poweradm/data/reserved_ids' % (pahome, timestr, pahome))


    def returnChange(self):
        ''' return the change file '''

        return('%s/poweradm/changes/%s_%s.sh' % (pahome, self.change, timestr))

