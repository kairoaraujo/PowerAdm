#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
apimain.py

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
import os
import commands
import sys
import globalvar
import config
import newid
import systemvios
import execchange
import nim
import mklparconf
import mkosdeploy
import npiv
##############################################################################################

#
# Pre load variables
#
##############################################################################################
#

# NIM available files/LPARs configs to deploy
cfgdeploylist = nim.NIMFileFind()
deploy_list = cfgdeploylist.listDeploy()

# NIM available OS versions
osdeploylist = nim.NIMGetVer()
os_list = osdeploylist.listOSVersion()

# NIM available Servers

nimserverlist = nim.NIMServer()
nim_list = nimserverlist.listNIM()


try:

#
# Systems hosts
#
##############################################################################################

    if sys.argv[1] == "-sn":
        ''' Number of systems '''
        lensystems = (len(config.systems))
        print lensystems

    elif sys.argv[1] == "-sp":
        ''' Print system [position] in array'''
        systems = list(config.systems.keys())

        if len(sys.argv) < 3:
            print('-sp requires the position in array. Use -sn to show number of systems')
            exit(1)
        else:
            try:
                system_option = int(sys.argv[2])
                print(systems[system_option])
            except(IndexError,ValueError):
                print('The -sp [position] is a number existent on the array.\n'
                      'Use -sn to show number of systems.')
                exit(1)



#
# Shared Storage Pool
#
##############################################################################################


    elif sys.argv[1] == "-sspstatus":
        ''' Show if Shared Storage Pool is enabled or disabled '''
        print (config.active_ssp)

    elif sys.argv[1] == "-pooln":
        ''' List shared storage pools array size (number of shared storage pools)'''

        ssp_len = (len(config.storage_pools))
        if config.active_ssp == 'no':
            print ('Shared Storage Pool is disabled.\n%s' % ssp_len)
        else:
            print (ssp_len)

    elif sys.argv[1] == "-poolp":
        ''' Print shared storage pool [position] name in array'''

        if len(sys.argv) < 3:
            print('-poolp requires the position in array. Use -pooln to show number of systems')
            exit(1)
        else:
            try:
                ssp_option = int(sys.argv[2])
                print(config.storage_pools[ssp_option])
            except(IndexError,ValueError):
                print('The -poolp [position] is a number existent on the array.\n'
                      'Use -pooln to show number of shared storage pools')

#
# Virtual Switches
#
##############################################################################################

    elif sys.argv[1] == "-vswn":
        ''' List Virtual Switches array size (number of virtual switches) '''
        lenvsw = (len(config.virtual_switches))
        print lenvsw

    elif sys.argv[1] == "-vswp":
        ''' Print virtual switch [position] '''

        if len(sys.argv) < 3:
            print('-vswp requires the position in array. Use -vswn to show number of systems')
            exit(1)
        else:
            try:
                vsw_option = int(sys.argv[2])
                print(config.virtual_switches[vsw_option])
            except(IndexError,ValueError):
                print('The -vswp [position] is a number existent on the array.\n'
                      'Use -vswn to show number of virtual switches on array')

#
# Get NPIVs
#
##############################################################################################

    elif sys.argv[1] == "-npiv1":
        ''' Print lsnports and NPIV Notes (if you are using) from VIOS #1 of NPIV. '''

        if len(sys.argv) < 3:
            print('-npiv1 [system]. Requeries the name of system.')
        else:
            npivs = npiv.NPIV()
            npivs.lsnportsVIO(sys.argv[2], 'vio1')

    elif sys.argv[1] == "-npiv2":
        ''' Print lsnports and NPIV Notes (if you are using) from VIOS #2 of NPIV. '''

        if len(sys.argv) < 3:
            print('-npiv1 [system]. Requeries the name of system.')
        else:
            npivs = npiv.NPIV()
            npivs.lsnportsVIO(sys.argv[2], 'vio2')

    elif sys.argv[1] == "-npiv1n":
        ''' Print the number of NPIVs FCs available from VIOS #1 NPIV '''

        if len(sys.argv) < 3:
            print('-npiv1n [system]. Requeries the name of system.')
        else:
            npivs = npiv.NPIV()
            npivs.numberFCVIO(sys.argv[2], 'vio1')

    elif sys.argv[1] == "-npiv2n":
        ''' Print the number of NPIVs FCs available from VIOS #2 NPIV '''

        if sys.argv[2] < 3:
            print('-npiven [system]. Requeries the name of system.')

        else:
            npivs = npiv.NPIV()
            npivs.numberFCVIO(sys.argv[2], 'vio2')


    elif sys.argv[1] == "-npiv1p":
        ''' Print the FC on specific position on array of VIOS #1 NPIV.
            Use the -npiv1n to see the size of the array '''

        if len(sys.argv) < 4:
            print('-npiv1p [system] [position]. Requeries the name of system and position.')
        else:
            npivs = npiv.NPIV()
            print npivs.printFCVIO(sys.argv[2], 'vio1')[int(sys.argv[3])]

    elif sys.argv[1] == "-npiv2p":
        ''' Print the FC on specific position on array of VIOS #1 NPIV.
            Use the -npiv1n to see the size of the array '''

        if len(sys.argv) < 4:
            print('-npiv1 [system] [position]. Requeries the name of system and position.')
        else:
            npivs = npiv.NPIV()
            print npivs.printFCVIO(sys.argv[2], 'vio2')[int(sys.argv[3])]


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

        if config.api_debug == "yes" :
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
        if nim_deploy == "false":
            nim_deploy = "n"
        elif nim_deploy == "null":
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
        if config.active_ssp == "no":
            add_disk = "n"
            stgpool = "none"

        # get free id from newID.py
        nextid = newid.NewID()
        lparid = nextid.mkID()

        # get system VIOs
        listvios = systemvios.SystemVios()
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
        else:
            # the final and deploy is the same if NIM Deploys options is 'no'.
            if net_length == 1:
                veth = ("10/0/%s//0/0/%s" % (net_vlan1, net_vsw1))
                veth_final = ("10/0/%s//0/0/%s" % (net_vlan1, net_vsw1))
            elif net_length == 2:
                veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan2_1, net_vsw2_1,
                            net_vlan2_2,net_vsw2_2))
                veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s" % (net_vlan2_1, net_vsw2_1,
                   net_vlan2_2, net_vsw2_2))
            elif net_length == 3:
                veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                        (net_vlan3_1, net_vsw3_1, net_vlan3_2, net_vsw3_2, net_vlan3_3, net_vsw3_3))
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

            '''
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
            '''

            """ Make a file change """
            newchange = mklparconf.MakeLPARConf(change, prefix, lparname, lparid, nim_deploy, lparmem,
                                 lparentcpu, lparvcpu, vscsi, add_disk, stgpool, disk_size, vfc,
                                 npiv_vio1, npiv_vio2, veth, veth_final, system_option, vio1, vio2)
            newchange.headerchange()
            newchange.writechange()
            newchange.closechange()

            """ Print and get created change file """
            change_file = newchange.returnChange()
            print (change_file)

            """ Run change **** LPAR creation **** """
            mkchange = execchange.Exe(change_file)
            mkchange.runChange()

#
# NIM Deploy
#
##############################################################################################

    elif sys.argv[1] == "-nimstatus":
        ''' Show if NIM is enabled or disabled '''
        print (config.enable_nim_deploy)

#
# Deploy OS
#
##############################################################################################

# Avaiable LPAR configs to deploy
    elif sys.argv[1] == "-osn":
         ''' Get array size of available files/LPAR to NIM deploy '''

         print (len(deploy_list))

    elif sys.argv[1] == "-osp":
        ''' Print config deploy [position] in array'''

        if len(sys.argv) < 3:
            print('-osp requires the position in array. Use -osn to show number of config deploys')
            exit(1)
        else:
            try:
                print(deploy_list[int(sys.argv[2])])
            except(IndexError,ValueError):
                print('The -osp [position] is a number existent on the array.\n'
                      'The number starts with 0.\n'
                      'Use -osn to show number of array.')
                exit(1)

# Get NIM Server OS Versions available

    elif sys.argv[1] == '-osvn':
        ''' Get array size of available OS versions on NIM Deploy '''

        print(len(os_list))

    elif sys.argv[1] == '-osvp':
        ''' Print OS NIM Deploys version in array. Use osvl to show number of OS version '''

        if len(sys.argv) < 3:
            print('-osvp requires the position in array. Use -osvn to show number available size')
            exit(1)
        else:
            try:
                print(os_list[int(sys.argv[2])])
            except(IndexError,ValueError):
                print('The -osvp [position] is a number existent on the array.\n'
                      'The number starts with 0.\n'
                      'Use -osvn to show number of array.')
                exit(1)

# Get NIM Server informations
    elif sys.argv[1] == '-nimn':
        ''' Get array size of available NIM Servers '''

        print (len(nim_list))

    elif sys.argv[1] == '-nimp':
        ''' Print OS NIM Server in array. Use -nimn to show number of NIM Servers '''

        if len(sys.argv) < 3:
            print('-nimp requires the position in array. Use -nimn to show number available size')
            exit(1)
        else:
            try:
                print(nim_list[int(sys.argv[2])])
            except(IndexError,ValueError):
                print('The -nimp [position] is a number existent on the array.\n'
                      'The number starts with 0.\n'
                      'Use -nimn to show number of array.')
                exit(1)

# Deploy OS
    elif sys.argv[1] == '-nimdeploy':
        ''' Deploy OS using NIM.
            This command require full parameters.
            apimain.py -nimosdeploy 'NIM File' 'NIM OS Version' 'NIM Server' 'y or n'

            Attributes:

            NIM File            use -osn and -osp
            NIM OS Version      use -osvn and -osvp
            NIM Server          use -nimn and -nimp
            NIM Deploy          y or n

            Sample:
            apimain.py -nimdeploy 'foo-bar.nim' 'AIX 7.1 TL03 SP04' 'nimsrv01' 'y'
        '''

        if len(sys.argv) < 5:
            print('-nimdeploy requires \'NIM File\' \'NIM OS Version\' \'NIM Server\' \'y or n\'\n'
                  'Use -h to help')
            exit(1)
        else:
            nimfile = nim.NIMFileFind()
            nim_file = ('%s/poweradm/nim/%s' % (config.pahome, sys.argv[2]))
            nimfile.fileData(nim_file)
            # get variables
            lparprefix = nimfile.returnDeployPrefix()
            lparname = nimfile.returnDeployLPARName()
            lparframe = nimfile.returnDeployFrame()
            lparvlans = nimfile.returnDeployVLANFinal()

            # select version to install
            #
            nimcfg = nim.NIMGetVer()
            nimcfg.OSVersion(sys.argv[3])
            nim_cfg_ver = nimcfg.getOSVersion()
            nim_cfg_spot = nimcfg.getSpot()
            nim_cfg_mksysbspot = nimcfg.getMksysbLpp()


            # select nim and get variables
            #
            nimvars = nim.NIMServer()
            nimvars.getNIM(sys.argv[4])
            nim_address = nimvars.getNIMAddress()
            nim_ipstart = nimvars.getIPStart()
            nim_ipend = nimvars.getIPEnd()
            nim_ipnet = nimvars.getIPNet()
            nim_server = nimvars.getNIMServer()
            nim_ipdeploy = nimvars.getNIMIPDeploy()

            # Deploy
            deploy = sys.argv[5]

            ''' Convert boolean to y/n '''
            if deploy == 'true':
                deploy = 'y'
            else:
                deploy = 'n'

            if deploy == 'n':
                ''' If deploy is 'n' just print config verification '''
                print('Config verification:\n\n'
                      'LPAR Prefix: %s\n'
                      'LPAR Name: %s\n'
                      'LPAR Frame: %s\n'
                      'LPAR Final VLAN: %s\n'
                      'LPAR NIM File: %s\n'
                      'NIM config OS Version: %s\n'
                      'NIM config OS spot: %s\n'
                      'NIM config OS mksysb/spot: %s\n'
                      'NIM IP Address: %s\n'
                      'NIM start IP of range: %s\n'
                      'NIM end IP of range: %s\n'
                      'NIM IP Network: %s\n'
                      'NIM Server: %s\n'
                      'NIM IP Deploy (server): %s\n'
                      'Deploy: %s\n'
                      % (lparprefix, lparname, lparframe, lparvlans, nim_file, nim_cfg_ver, nim_cfg_spot,
                      nim_cfg_mksysbspot, nim_address, nim_ipstart, nim_ipend, nim_ipnet,
                      nim_server, nim_ipdeploy, deploy))

            else:
                ''' If deploy is 'y' make deploy '''
                deploy_os = mkosdeploy.MakeNIMDeploy(lparprefix, lparname, lparframe, lparvlans, nim_file,
                        nim_cfg_ver, nim_cfg_spot, nim_cfg_mksysbspot, nim_address, nim_ipstart, nim_ipend,
                        nim_ipnet, nim_server, nim_ipdeploy, deploy)
                ''' Start deployment '''
                deploy_os.createNIMDeploy()


#
# HELP
#
##############################################################################################
    elif sys.argv[1] == "-h":
        print('%s is part of PowerAdm %s - http://www.poweradm.org\n'
              'This is a project of API for Web Interface and VMware vCenter Orchestrator.\n\n'
              'usage: %s [options]\n\n'
              'Arguments:\n'
              '-sn \t\t\t\tList systems array size (number of systems).\n'
              '-sp [position] \t\t\tPrint system position name in array.\n'
              ' \t\t\t\tPosition in array. Position start with 0. Use -sn to check array size.\n'
              '-nimstatus \t\t\tReturn NIM enable status [yes|no].\n'
              '-sspstatus \t\t\tReturn Shared Storage Pool enable status [yes|no].\n'
              '-pooln \t\t\t\tList shared storage pools array size (number of shared storage pools).\n'
              '-poolp [positon] \t\tPrint shared storage pool position name in array.\n'
              ' \t\t\t\tPosition in array. Position start with 0. Use -pooln to check array size.\n'
              '-vswn \t\t\t\tList Virtual Switches array size (number of virtual switches).\n'
              '-vswp [postion] \t\tPrint virtual switch position name in array.\n'
              ' \t\t\t\tPosition in array. Position start with 0. Use -vswn to check array size.\n'
              '-npiv1 [system] \t\tPrint informations about NPIV (lsmap and notes) on Primary NPIV VIOS.\n'
              ' \t\t\t\tRequeries the name of system.\n'
              '-npiv2 [system] \t\tPrint informations about NPIV (lsmap and notes) on Secondary NPIV VIOS.\n'
              ' \t\t\t\tRequeries the name of system.\n'
              '-npiv1n [system] \t\tList FCs array size (number of FCs available) on Primary NPIV VIOS.\n'
              ' \t\t\t\tRequeries the name of system\n'
              '-npiv1p [system] [position]\tPrint FC name in specific position\n'
              ' \t\t\t\tRequeries the name of system\n'
              ' \t\t\t\tPosition start with 0. Use -npiv1n to check array size.\n'
              '-npiv2n [system] \t\tList FCs array size (number of FCs available) on Secondary NPIV VIOS.\n'
              ' \t\t\t\tRequeries the name of system.\n'
              '-npiv2p [system] [position]\tList FCs array size (number of FCs available) on Secondary NPIV VIOS.\n'
              ' \t\t\t\tRequeries the name of system.\n'
              ' \t\t\t\tPosition start with 0. Use -npiv2n to check array size.\n'
              '-osn \t\t\t\tGet array size of available files/LPAR to NIM deploy.\n'
              '-osp [position] \t\tPrint config deploy [position] in array.\n'
              ' \t\t\t\tPosition in array. Position start with 0. Use -osn to check array size.\n'
              '-osvn \t\t\t\tGet array size of available OS versions on NIM Deploy\n'
              '-osvp [position] \t\tPrint OS NIM Deploys version in array. Use osvl to show number of OS version\n'
              '-nimn \t\t\t\tGet array size of available NIM Servers\n'
              '-nimp [position] \t\tPrint OS NIM Server in array.\n'
              ' \t\t\t\tPosition in array. Position start with 0. Use -nimn to check array size.\n'
              '-mklparcfg [arguments] \t\tCreate LPAR\n'
              '\t\t\t\tArguments in order:\n'
              '\t\t\t\tchange prefix lparname nim_deploy lparmem lparentcpu lparvcpu vscsi add_disk stgpool\n'
              '\t\t\t\tdisk_size vfc npiv_vio1 npiv_vio2 vlan_deploy vsw_deploy net_vlan1 net_vlan2_1 net_vlan2_2\n'
              '\t\t\t\tnet_vlan3_1 net_vlan3_2 net_vlan3_3 net_vsw1 net_vsw2_1 net_vsw2_2 net_vsw3_1 net_vsw3_2 net_vsw3_3\n'
              '\t\t\t\tnet_length system_option action\n'
              '\t\t\t\tCheck the documentation about API in http://poweradm.org/apimain.html\n'
              '-nimdeploy [arguments] \t\tDeploy OS using NIM. Requires arguments.\n'
              '\t\t\t\tArguments in order:\n'
              '\t\t\t\tnim_file os_version nim_server y|n\n'
              '\t\t\t\tCheck the documentation about API in http://poweradm.org/apimain.html\n'
              % (sys.argv[0], globalvar.version, sys.argv[0]))
    else:
        print ('Option not found. Use -h to help.')

except(AttributeError,IndexError):
    print ('Please use %s [option] [parameters]. Use -h to help.' % sys.argv[0])
    exit(1)
