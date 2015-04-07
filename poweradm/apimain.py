#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
apimain.py

Copyright (c) 2015 Kairo Araujo

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
import os
import commands
import sys
from globalvar import *
from config import *
from newid import *
from systemvios import *
from execchange import *
from mklparconf import *
##############################################################################################
try:

#
# Systems hosts
#
##############################################################################################

    if sys.argv[1] == "-sl":
        ''' List systems array size (number of systems) '''
        lensystems = (len(systems))
        print lensystems

    elif sys.argv[1] == "-sp":
        ''' Print system [position] in array'''
        systems = list(systems.keys())

        if sys.argv[2] == " ":
            print('-sp requires the position in array. Use -sl to show number of systems')
        else:
            try:
                system_option = int(sys.argv[2])
                print(systems[system_option])
            except(IndexError,ValueError):
                print('The -sp [position] is a number existent on the array.\n'
                      'Use -sl to show number of systems')

#
# NIM Deploy
#
##############################################################################################

    elif sys.argv[1] == "-nimstatus":
        ''' Show if NIM is enabled or disabled '''
        print (enable_nim_deploy)


#
# Shared Storage Pool
#
##############################################################################################


    elif sys.argv[1] == "-sspstatus":
	''' Show if Shared Storage Pool is enabled or disabled '''
	print (active_ssp)

    elif sys.argv[1] == "-pooll":
        ''' List shared storage pools array size (number of shared storage pools)'''
        ssp_len = (len(storage_pools))
	print (ssp_len)

    elif sys.argv[1] == "-poolp":
        ''' Print shared storage pool [position] name in array'''

        if sys.argv[2] == " ":
            print('-poolp requires the position in array. Use -poolp to show number of pools')
        else:
            try:
                ssp_option = int(sys.argv[2])
                print(storage_pools[ssp_option])
            except(IndexError,ValueError):
                print('The -poolp [position] is a number existent on the array.\n'
		      'Use -pooll to show number of shared storage pools')

#
# Virtual Switches
#
##############################################################################################

    elif sys.argv[1] == "-vswl":
        ''' List Virtual Switches array size (number of virtual switches) '''
        lenvsw = (len(virtual_switches))
        print lenvsw

    elif sys.argv[1] == "-vswp":
        ''' Print virtual switch [position] '''
        if sys.argv[2] == " ":
            print('-vwp requires the position in array. Use -vwl to show number of systems')
        else:
            try:
                vsw_option = int(sys.argv[2])
                print(virtual_switches[vsw_option])
            except(IndexError,ValueError):
                print('The -vswp [position] is a number existent on the array.\n'
                      'Use -vswl to show number of virtual switches on array')

#
# Get VIOS
#
##############################################################################################
    elif sys.argv[1] == "-npiv1":


        if sys.argv[2] == "":
            print('-npiv1 [system]. Requeries the name of system.')

        else:
            # get values system and vios
            system = sys.argv[2]

            find_vios = SystemVios()
            vio1 = find_vios.returnVio1('%s' % (sys.argv[2]))

            # get information on hmc
	    lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
                                  system, vio1))

	    # if exists file npiv notes get
            if os.path.isfile('%s/npiv/%s-%s' % ( pahome, system, vio1)):
                npiv_notes = commands.getoutput('cat %s/npiv/%s-%s' % ( pahome, system, vio1))
	    else:
		npiv_notes = ""

	    print ("%s \n %s" % (lsnports, npiv_notes))

    elif sys.argv[1] == "-npiv2":


        if sys.argv[2] == "":
            print('-npiv1 [system]. Requeries the name of system.')

        else:
            # get values system and vios
            system = sys.argv[2]

            find_vios = SystemVios()
            vio2 = find_vios.returnVio2('%s' % (sys.argv[2]))

            # get information on hmc
	    lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' % (hmcserver,
                                  system, vio2))

	    # if exists file npiv notes get
            if os.path.isfile('%s/npiv/%s-%s' % ( pahome, system, vio2)):
                npiv_notes = commands.getoutput('cat %s/npiv/%s-%s' % ( pahome, system, vio2))
	    else:
		npiv_notes = ""

	    print ("%s \n %s" % (lsnports, npiv_notes))

#
# Make Config lpar
#
##############################################################################################

    elif sys.argv[1] == "-mklparcfg":
        change = sys.argv[2]
        prefix = sys.argv[3]
        lparname = sys.argv[4]
        nim_deploy = sys.argv[5]
        lparmem = sys.argv[6]
        lparentcpu = sys.argv[7]
        lparvcpu = sys.argv[8]
        vscsi = sys.argv[9]
        add_disk = sys.argv[10]
        stgpool = sys.argv[11]
        disk_size = sys.argv[12]
        vfc = sys.argv[13]
        npiv_vio1 = sys.argv[14]
        npiv_vio2 = sys.argv[15]
        vlan_deploy = sys.argv[16]
        vsw_deploy = sys.argv[17]
        net_vlan1 = sys.argv[18]
        net_vlan2_1 = sys.argv[19]
        net_vlan2_2 = sys.argv[20]
        net_vlan3_1 = sys.argv[21]
        net_vlan3_2 = sys.argv[22]
        net_vlan3_3 = sys.argv[23]
        net_vsw1 = sys.argv[24]
        net_vsw2_1 = sys.argv[25]
        net_vsw2_2 = sys.argv[26]
        net_vsw3_1 = sys.argv[27]
        net_vsw3_2 = sys.argv[28]
        net_vsw3_3 = sys.argv[29]
        net_length = sys.argv[30]
        system_option = sys.argv[31]
        action = sys.argv[32]

        if api_debug == "yes" :
            print('The parameters send is:\n'
                'Change: %s\n'
                'Prefix: %s\n'
                'LPAR Name: %s\n'
                'NIM Deploy: %s\n'
                'LPAR Memory: %s\n'
                'LPAR Entitled CPU: %s\n'
                'LPAR Virtual CPU: %s\n'
                'Virtual SCSI: %s\n'
                'Add Disk: %s\n'
                'Storage Pool: %s\n'
                'Disk Size: %s\n'
                'Virtual HBA: %s\n'
                'NPIV VIO1: %s\n'
                'NPIV VIO2: %s\n'
                'VLAN Deploy: %s\n'
                'Virtual Switch Deploy: %s\n'
                'Ethernet if number of ethernets is 1\n\n'
                'Virtual VLAN Ethernet  1 of 1: %s\n'
                'Virtual Virtual Switch 1 of 1: %s\n'
                '\nEthernets if number of ethernets is 2\n'
                'Virtual VLAN Ethernet  1 of 2: %s\n'
                'Virtual Virtual Switch 1 of 2: %s\n'
                'Virtual VLAN Ethernet  2 of 2: %s\n'
                'Virtual Virtual Switch 2 of 2: %s\n'
                '\nEthernets if number of ethernets is 3\n'
                'Virtual VLAN Ethernet  1 of 3: %s\n'
                'Virtual Virtual Switch 1 of 3: %s\n'
                'Virtual VLAN Ethernet  2 of 3: %s\n'
                'Virtual Virtual Switch 2 of 3: %s\n'
                'Virtual VLAN Ethernet  3 of 3: %s\n'
                'Virtual Virtual Switch 2 of 3: %s\n'
                '\nNumber of Ethernets: %s\n'
                'System host: %s\n'
                'Action: %s\n' %
                (change, prefix, lparname, nim_deploy, lparmem, lparentcpu, lparvcpu, vscsi,
                 add_disk, stgpool, disk_size, vfc, npiv_vio1, npiv_vio2, vlan_deploy, vsw_deploy,
                 net_vlan1, net_vsw1, net_vlan2_1, net_vsw2_1, net_vlan2_2, net_vsw2_2,
                 net_vlan3_1, net_vsw3_1, net_vlan3_2, net_vsw3_2, net_vlan3_3, net_vsw3_3, net_length,
                 system_option, action))


        # convert int and float variables
        lparentcpu = float(lparentcpu)
        lparvcpu = int(lparvcpu)
        lparmem = int(lparmem)
        net_length = int(net_length)

        # convert null to n
        #
        # nim_deploy
        if nim_deploy == "null":
            nim_deploy = "n"
        else:
            nim_deploy = "y"
        # disk_size
        if disk_size == "null":
            disk_size = 0

        # convert true and false to y or n
        #
        # vscsi
        if vscsi == "true":
            vscsi = "y"
        else:
            vscsi = "n"
        # add_disk (if n stgpool is none)
        if add_disk == "true":
            add_disk = "y"
        else:
            add_disk = "n"
        # vfc
        if vfc == "true":
            vfc = "y"
        else:
            vfc = "n"
        # active SSP
        if active_ssp == "no":
            add_disk = "n"
            stgpool = "none"

        # get free id from newID.py
        nextid = NewID()
        nextid.mkID()
        lparid = nextid.getID()

        # get system VIOs
        listvios = SystemVios()
        vio1 = listvios.returnVio1(system_option)
        vio2 = listvios.returnVio2(system_option)

        # network deploy and final
        if nim_deploy == 'y':
            if net_length == 1:
                veth = ("10/0/%s//0/0/%s" % (vlan_deploy, vsw_deploy))
                veth_final = ("10/0/%s//0/0/%s" % (net_vlan1, net_vsw1))
            elif net_length == 2:
                veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (vlan_deploy, vsw_deploy,
                            net_vlan2_2,net_vsw2_2))
                veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan2_1, net_vsw2_1,
                   net_vlan2_2, net_vsw2_2))
            elif net_length == 3:
                veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                        (vlan_deploy, vsw_deploy, net_vlan3_2, net_vsw3_2, net_vlan3_3, net_vsw3_3))
                veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                        (net_vlan3_1, net_vsw3_1, net_vlan3_2, net_vsw3_2, net_vlan3_3, net_vsw3_3))

        print ("*"*80)
        print('Config validation: \n\n'
              'Change/Ticket: %s\n'
              'LPAR: %s-%s\n'
              'LPAR ID: %s\n'
              'Deploy via NIM: %s\n'
              'LPAR Memory: %s\n'
              'LPAR Entitled CPU: %s\n'
              'LPAR Virtual CPU: %s\n'
              'Virtual SCSI: %s\n'
              'Add Disk: %s\n'
              'Storage Pool: %s\n'
              'Disk Size: %s\n'
              'Virtual HBA/NPIV: %s\n'
              'NPIV 1: %s\n'
              'NPIV 2: %s\n'
              'Ethernet temporaly: %s\n'
              'Ethernet final: %s\n'
              'Host System: %s\n'
              'Primary:     %s\n'
              'Secondary:   %s\n' %
              (change, prefix, lparname, lparid, nim_deploy, lparmem,
              lparentcpu, lparvcpu, vscsi, add_disk, stgpool, disk_size, vfc,
              npiv_vio1, npiv_vio2, veth, veth_final, system_option, vio1, vio2))
        print ("*"*80)

        """ Execute the LPAR creation """
        if action == "create":

            """ Print the lpar configuration final """
            print ("*"*80)
            print('Config validation: \n\n'
                  'Change/Ticket: %s\n'
                  'LPAR: %s-%s\n'
                  'LPAR ID: %s\n'
                  'Deploy via NIM: %s\n'
                  'LPAR Memory: %s\n'
                  'LPAR Entitled CPU: %s\n'
                  'LPAR Virtual CPU: %s\n'
                  'Virtual SCSI: %s\n'
                  'Add Disk: %s\n'
                  'Storage Pool: %s\n'
                  'Disk Size: %s\n'
                  'Virtual HBA/NPIV: %s\n'
                  'NPIV 1: %s\n'
                  'NPIV 2: %s\n'
                  'Ethernet temporaly: %s\n'
                  'Ethernet final: %s\n'
                  'Host System: %s\n'
                  'Primary:     %s\n'
                  'Secondary:   %s\n' %
                  (change, prefix, lparname, lparid, nim_deploy, lparmem,
                   lparentcpu, lparvcpu, vscsi, add_disk, stgpool, disk_size, vfc,
                   npiv_vio1, npiv_vio2, veth, veth_final, system_option, vio1, vio2))
            print ("*"*80)

            """ Make a file change """
            newchange = MakeLPARConf(change, prefix, lparname, lparid, nim_deploy, lparmem,
                                 lparentcpu, lparvcpu, vscsi, add_disk, stgpool, disk_size, vfc,
                                 npiv_vio1, npiv_vio2, veth, veth_final, system_option, vio1, vio2)
            newchange.headerchange()
            newchange.writechange()
            newchange.closechange()

            """ Print and get created change file """
            change_file = newchange.returnChange()
            print (change_file)

            """ Run change **** LPAR creation **** """
            mkchange = ExecChange(change_file)
            mkchange.runChange()

#
# HELP
#
##############################################################################################


    elif sys.argv[1] == "-h":
        print('%s is part of PowerAdm %s - http://www.poweradm.org\n'
              'This is a project of API for Web Interface and VMware vCenter Orchestrator.\n\n'
              'usage: %s [options]\n\n'
              'Arguments:\n'
              '-sl \t\t\tList systems array size (number of systems).\n'
              '-sp [position] \t\tPrint system [position] name in array..\n'
              ' \t\t\tPosition in array. Position start with 0.\n'
    	      '-nimstatus \t\tReturn NIM enable status.\n'
              '-sspstatus \t\tReturn Shared Storage Pool enable status.\n'
              '-pooll \t\t\tList shared storage pools array size (number of shared storage pools).\n'
              '-poolp [positon] \tPrint shared storage pool [position] name in array.\n'
              ' \t\t\tPosition in array. Position start with 0.\n'
              '-vswl \t\t\tList Virtual Switches array size (number of virtual switches).\n'
              '-vswp [postion] \tPrint virtual switch [polition] name in array.\n'
              ' \t\t\tPosition in array. Position start with 0.\n'
              '-npiv1 [system] \tPrint informations about NPIV (lsmap and notes) on Primary VIO.\n'
	          ' \t\t\tRequeries the name of system.\n'
              '-npiv2 [system] \tPrint informations about NPIV (lsmap and notes) on Secondary VIO.\n'
    	      ' \t\t\tRequeries the name of system.\n'
    	      '-mklparcfg [arguments] \tCheck the arguments on doc. http://poweradm.org\n'
              % (sys.argv[0], version, sys.argv[0]))
    else:
        print ('Option not found. Use -h to help.')

except(AttributeError,IndexError):
    print ('Please use %s [option] [parameters]. Use -h to help.' % sys.argv[0])
    exit(1)

