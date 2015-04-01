#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# tblpar.py
#
# Copyright (c) 2015 Kairo Araujo
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
import os
import commands
import globalvar
import systemvios
import config
import lsnpivs
##############################################################################################

# get all systems available in config
list_system = systemvios.SystemVios()
systems = list_system.getSystemList()


def vscsi():
    ''' Execute virtual SCSI troubleshooting for LPAR '''

    print "\n\033[94mSCSI\033[1;00m"
    print "\033[94m----\033[1;00m"

    # get the information from find_lpar with somes splits.
    lpardata = find_lpar.split('virtual_scsi_adapters')
    lpardata_spl1 = lpardata[1].split('=')
    lpardata_spl2 = lpardata_spl1[1].split('",')
    lpardata_spl3 = lpardata_spl2[0].split(',')
    lpar_vscsi = lpardata_spl3
    # verify if virtual scsi exists, if not output is a simple none,
    # if exists get all informations
    if lpar_vscsi[0] == 'none':
        print lpar_vscsi[0]
    else:
        # looping for all scsi
        for l_lpar_vscsi in lpar_vscsi:
            scsi_configs = l_lpar_vscsi.split('/')
            print "+ C%s" % scsi_configs[0]
            print "`.... VIOS: %s" % scsi_configs[3]
            print "`.... VIOS adapter ID: %s" % scsi_configs[4]

            # get vhost on VIOS
    	    vhost = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s "
                "-p %s -c \"\'lsmap -all\'\" | grep 'C%s ' | awk '{ print $1 }'" %
                (config.hmcserver, system, scsi_configs[3], scsi_configs[4]))
    	    print "`.... vhost: %s" % vhost

            # get informations on vhost on VIOS and save on temporaly file
    	    os.system("ssh -l poweradm %s viosvrcmd -m %s "
                "-p %s -c \"\'lsmap -vadapter %s\'\" > /tmp/%s.lsmap.%s" %
                (config.hmcserver, system, scsi_configs[3], vhost, system, lpar_search))

            # open temp file to get VTD informations
    	    with open("/tmp/%s.lsmap.%s" % (system, lpar_search )) as lsmap:
     	        vtd_list = []
                for l_lsmap in lsmap:
                    if l_lsmap.startswith( 'VTD' ):
                        new_vtd = l_lsmap.split()
                        if new_vtd[1] == 'NO':
                            break
                        vtd_list.append(new_vtd[1])
                if len(vtd_list) != 0:
                    print "`.... VTD allocated list: %s " % (', '.join(vtd_list))
                else:
                    print "`.... VTD allocated list: none"

            # open temp file to get Backing device informations
    	    with open("/tmp/%s.lsmap.%s" % (system, lpar_search)) as lsmap:

                backing_device_list = []
                for l_lsmap in lsmap:

                    if l_lsmap.startswith( 'Backing' ):
                        new_backing_device = l_lsmap.split()

                        # if Backing device is empty (as a vtopt) dont't try add on array
                        if len(new_backing_device) > 2:
                            backing_device_list.append(new_backing_device[2])

                    # if Backing Device is empty without devices print none or the list
                if len(backing_device_list) != 0:
                    print "`.... Backing Device allocated list: %s \n" % (', '.join(backing_device_list))
                else:
                    print "`.... Backing Device allocated list: none\n"

def vfc():
    ''' Execute the virtual FC troubleshooting '''

    print "\n\033[94mNPVI\033[1;00m"
    print "\033[94m----\033[1;00m"


    # get the information from find_lpar with somes splits.
    lpardata = find_lpar.split('virtual_fc_adapters')
    lpardata_spl1 = lpardata[1].split('"""')
    lpardata_spl2 = lpardata_spl1[0].split('=""')
    try:
        lpar_fcs = lpardata_spl2[1].split('"",""')
    except(IndexError):
        print "LPAR withtout FC/HBA"
        exit()
    len_lpar_fcs = len(lpar_fcs)-1
    count = 0
    # check all fcs existent on LPAR
    while count <= len_lpar_fcs:
        fcs_configs = lpar_fcs[count].split('/')
        print "+ C%s" % fcs_configs[0]
        print "`.... WWNS (active,inactive): %s" % fcs_configs[5]
        print "`.... VIOS: %s" % fcs_configs[3]
        print "`.... VIOS adapter ID: %s" % fcs_configs[4]

        # get the vfchost on VIOS
        vfchost = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s "
                "-p %s -c \"\'lsmap -all -npiv\'\" | grep 'C%s ' | awk '{ print $1 }'" %
                (config.hmcserver, system, fcs_configs[3], fcs_configs[4]))

        # get the vfchost informations on VIOS and put on temp file
        print "`.... vfchost: %s" % vfchost
        os.system("ssh -l poweradm %s viosvrcmd -m %s "
                "-p %s -c \"\'lsmap -npiv -vadapter %s\'\" > /tmp/%s.lsmap.npiv.%s" %
                (config.hmcserver, system, fcs_configs[3], vfchost, system, lpar_search))

        # open the temp file with vfchost informations
        with open("/tmp/%s.lsmap.npiv.%s" % (system, lpar_search)) as lsmap_npiv:
            for l_lsmap_npiv in lsmap_npiv:
                if l_lsmap_npiv.startswith('Status'):
                    fc_status = l_lsmap_npiv.split(':')
                    if fc_status[1] == 'LOGGED_IN\n':
                        fc_status = ("\033[32m%s\033[1;00m" % fc_status[1].replace('\n',''))
                    else:
                        fc_status = ("\033[31m%s\033[1;00m" % fc_status[1].replace('\n',''))

                # get the fcp (physical FC) used by LPAR
                elif l_lsmap_npiv.startswith('FC name'):
                    l_lsmap_npiv_spl1 = l_lsmap_npiv.split()
                    fcp = l_lsmap_npiv_spl1[1].split(':')
                    # if empty put none
                    if fcp[1] == '':
                        fcp[1] = ("\033[31mnone\033[1;00m")
                # get number of paths for this vfchost
                elif l_lsmap_npiv.startswith('Ports logged in'):
                    num_ports_logged = l_lsmap_npiv.split(':')
                    num_ports_logged =  num_ports_logged[1].replace('\n','')

            # output informations
            print "`.... VIOS Physical Adapter: %s" % fcp[1]
            print "`.... Client FC status %s" % fc_status
            print "`.... Number of ports logged in: %s" % num_ports_logged

            print "\n\033[94mVerify NPIV state\033[1;00m"
            print "\033[94m------ ---- -----\033[1;00m"
            print ("Checking the NPIV \033[36m%s\033[1;00m state on VIO \033[36m%s\033[1;00m" %
                  (fcp[1], fcs_configs[3]))

            # run lsnpiv on specific NPIV interface
            if fcp[1] != '\033[31mnone\033[1;00m':
                 lsnpivs.run(config.hmcserver, system, fcs_configs[3], fcp[1])

            else:
                 print ("\n\033[31mDon't have connection to NPIV on VIO \033[36m%s\033[1;00m\n" % (fcs_configs[3]))
        count += 1

def vnet():
    print "\n\033[94mNetwork\033[1;00m"
    print "\033[94m-------\033[1;00m\n"

    # get the ethernet configurations
    # it's necessary some splits here
    lpardata = find_lpar.split('virtual_eth_adapters')
    lpardata_spl1 = lpardata[1].split('=')
    lpardata_spl2 =  lpardata_spl1[1].split('",')
    lpar_eths = lpardata_spl2[0].split(',')
    vsw = '' # it's used to check if is the same VSW, if it's don't print again the SEA status, unecessary.
    # looping to get ethernet informations
    for l_lpar_eths in lpar_eths:
        eth_configs = l_lpar_eths.split('/')
        print "+ C%s" % eth_configs[0]
        print "`.... VLAN: %s" % eth_configs[2]
        print "`.... VIRTUAL SWITCH: %s" % eth_configs[6]
        net_vio = systemvios.SystemVios()
        # sea array
        seas = []
        # looping to get SEAS on the VIOS
        for l_net_vios in (net_vio.returnNetVio1(system), net_vio.returnNetVio2(system)):
            find_sea_vio = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s -p %s "
                           "-c \"\'lsdev -type adapter\'\" | grep \'Shared Ethernet Adapter\' | awk \'{ print $1 }\'" %
                           (config.hmcserver, system, l_net_vios))
            # looping to check de VSW and VLAN on SEA
            find_sea_vio_data = find_sea_vio.split()
            for l_find_sea_vio in find_sea_vio_data:
                find_vsw = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s "
                        "-p %s -c \"\'entstat -all %s\'\" | grep -E \'%s|^    ent\'" % (config.hmcserver, system, l_net_vios, l_find_sea_vio, eth_configs[6]))
                if eth_configs[2] in find_vsw:
                    seas.append(l_find_sea_vio)
        print ("`.... VIOS(SEA): %s(%s), %s(%s)\n" % (net_vio.returnNetVio1(system), seas[0], net_vio.returnNetVio2(system), seas[1]))

        print "\033[94mSEA status\033[1;00m"
        print "\033[94m--- ------\033[1;00m\n"

        # use the lsseas to check SEA status
        if vsw != eth_configs[6]:

            print ("Checking the \033[36m%s\033[1;00m on VIOS \033[36m%s\033[1;00m ...\n" % ( seas[0], net_vio.returnNetVio1(system)))

            os.system ("ksh %s/poweradm/tools/lsseas -c %s %s %s %s" %
                    (config.pahome, config.hmcserver, system, net_vio.returnNetVio1(system), seas[0]))

            print ("\nChecking the \033[36m%s\033[1;00m on VIOS \033[36m%s\033[1;00m ...\n" % ( seas[1], net_vio.returnNetVio2(system)))

            os.system ("ksh %s/poweradm/tools/lsseas -c %s %s %s %s" %
                    (config.pahome, config.hmcserver, system, net_vio.returnNetVio2(system), seas[1]))

            print ("\n")

        else:
            print ("\n This SEA has the same configuration of the last adapter.\n")
            vsw = eth_configs[6]

def run( id_search, tb_option):
    ''' Run the initial search for LPAR by ID '''


    global find_lpar, system, lpar_search
    lpar_search = id_search
    # find lpar by the ID
    for system in systems:
        find_lpar = commands.getoutput('ssh -l poweradm %s lssyscfg -r prof -m %s --filter lpar_ids=%s' % (config.hmcserver, system, id_search))
        if ("lpar_id=%s" % id_search) in find_lpar:
            break
    if ('HSCL8011 The partition ID "%s" was not found.' % id_search) == find_lpar:
        print "\n\nLPAR not found."
	exit()


    # get some informations about lpar
    lpardata = find_lpar.split(',')
    for l_lpardata in lpardata:
        lpar_info = l_lpardata.split('=')

        # lpar name
        if lpar_info[0] in ('lpar_name'):
    	    lpar_name = lpar_info[1]

        # entitled cpu
        elif lpar_info[0] in ('desired_proc_units'):
        	lpar_ent_cpu = lpar_info[1]
        elif lpar_info[0] in ('min_proc_units'):
        	min_proc_units = lpar_info[1]
        elif lpar_info[0] in ('max_proc_units'):
        	max_proc_units = lpar_info[1]

        # virtual processor
        elif lpar_info[0] in ('desired_procs'):
        	desired_procs = lpar_info[1]
        elif lpar_info[0] in ('min_procs'):
        	min_procs = lpar_info[1]
        elif lpar_info[0] in ('max_procs'):
        	max_procs = lpar_info[1]

        # memory
        elif lpar_info[0] in ('desired_mem'):
        	desired_mem = lpar_info[1]
        elif lpar_info[0] in ('max_mem'):
        	max_mem = lpar_info[1]
        elif lpar_info[0] in ('min_mem'):
        	min_mem = lpar_info[1]

        # vscsi
        elif lpar_info[0] in ('virtual_scsi_adapters'):
        	virtual_scsi_adapters = lpar_info[1]

    lpar_status_data = commands.getoutput("ssh -l poweradm %s lssyscfg -m %s -r lpar -F state:rmc_state:boot_mode:curr_profile --filter lpar_names=%s" %
            (config.hmcserver, system, lpar_name))

    lpar_status = lpar_status_data.split(':')
    # lpar status
    lpar_state = lpar_status[0]

    if lpar_state == 'Running':
        lpar_state = ("\033[32m%s\033[1;00m" % lpar_state)
    else:
        lpar_state = ("\033[31m%s\033[1;00m" % lpar_state)
    lpar_rmc = lpar_status[1]

    # lpar hmc(dlpar) satus
    if lpar_rmc == 'active':
        lpar_rmc = ("\033[32m%s\033[1;00m" % lpar_rmc)
    else:
        lpar_rmc = ("\033[31m%s\033[1;00m" % lpar_rmc)

    # lpar boot mode
    lpar_boot_mode = lpar_status[2]
    if lpar_boot_mode == 'norm':
        lpar_boot_mode = ("\033[32mNormal\033[1;00m")
    else:
        lpar_boot_mode = ("\033[31m%s\033[1;00m" % lpar_boot_mode)

    lpar_curr_profile = lpar_status[3]

    print "\n\n"
    print "\033[94m#\033[1;00m" * 84
    print ("\033[94m# LPAR NAME: %s - ID: %s - getting LPAR information and state\033[1;00m" % (lpar_name, lpar_search))
    print "\033[94m#\033[1;00m" * 84

    print ("\n+ LPAR NAME: %s\t| Current Profile: %s\n+ Host Server: %s" % (lpar_name, lpar_curr_profile, system))
    print ("+ LPAR Status")
    print ("`.... Current Status: %s\n`.... RMC Status (DLPAR): %s\n`.... Boot Mode: %s\n" % (lpar_state, lpar_rmc, lpar_boot_mode))

    print "\033[94mConfiguration\033[1;00m"
    print "\033[94m-\033[1;00m" * 84

    print "+ ID: %s\n" % lpar_search
    print "+ Virtual CPU: %s" % desired_procs
    print "`.... Min Virtual CPU (DLPAR): %s" % min_procs
    print "`.... Max Virtual CPU (DLPAR): %s\n" % min_procs
    print "+ Entitled CPU: %s " % lpar_ent_cpu
    print "`.... Min Entitled CPU (DLPAR): %s" % min_proc_units
    print "`.... Max Entitled CPU (DLPAR): %s\n" % max_proc_units
    print "+ Memory: %s " % desired_mem
    print "`.... Min Memory (DLPAR): %s" % min_mem
    print "`.... Max Memory (DLPAR): %s\n" % max_mem

    # get the vios, not used yet :P
    npiv_vios = systemvios.SystemVios()
    npiv_vios_list = [npiv_vios.returnVio1(system), npiv_vios.returnVio2(system)]

    # run all checks (vscsi, vfc and vnet)
    if tb_option == 'all':
        vscsi()
        vfc()
        vnet()

    # run vscsi check
    elif tb_option == 'vscsi':
        vscsi()

    # run vfc check
    elif tb_option == 'vfc':
        vfc()
    # run fc check
    elif tb_option == 'vnet':
        vnet()

