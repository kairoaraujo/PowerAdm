#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
npiv.py

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
import os
import config
import systemvios
import commands
import cachefile
##############################################################################################
#
# Class NPIV
##############################################################################################

class NPIV:
    ''' Get informations about NPIV on the VIOS. '''

    def lsnportsVIO(self, systemp, vio_server):
        ''' Get the 'lsnports' and NPIV notes (if have).

            Attributes:
            systemp     the system p name.
            vio_server  the vio do you want use:
                        options:
                            vio1 for #1 VIOS NPIV
                            vio2 for #2 VIOS NPIV
                            * this informations is used from the config file.
        '''

        # get informations about the VIOS from config file
        find_vios = systemvios.SystemVios()
        if vio_server == 'vio1':
            vios = find_vios.returnVio1('%s' % (systemp))
        elif vio_server == 'vio2':
            vios = find_vios.returnVio2('%s' % (systemp))
        else:
            print 'Option for VIO invalid. Use vio1 or vio2.'

        def lsnports_cmd():
            ''' Command to get the lsnports and NPIV notes '''

            # get information on hmc
            lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' %
                    (config.hmcserver, systemp, vios))

            # if exists file npiv notes get
            if os.path.isfile('%s/npiv/%s-%s' % ( config.pahome, systemp, vios)):
                npiv_notes = commands.getoutput('cat %s/npiv/%s-%s' % ( config.pahome, systemp, vios))
            else:
                npiv_notes = ""


            return  ("%s \n %s" % (lsnports, npiv_notes))

        # if cache file (CacheFile()) is enabled use that
        if config.npiv_cache == 'enable':

            lsnports = cachefile.CacheFile('%s/poweradm/npiv_cache/lsnports_%s_%s.cache' % (config.pahome,
                systemp, vios), config.npiv_cache_time, lsnports_cmd, 't_print')
            lsnports.cache()

        else:

            print lsnports_cmd()


    def numberFCVIO(self, systemp, vio_server):
        ''' Get the number of FCs available to the vios.

            Attributes:
            systemp     the system p name.
            vio_server  the vio do you want use:
                        options:
                            vio1 for #1 VIOS NPIV
                            vio2 for #2 VIOS NPIV
                            * this informations is used from the config file.
        '''

        # get informations about the VIOS from config file
        find_vios = systemvios.SystemVios()
        if vio_server == 'vio1':
            vios = find_vios.returnVio1('%s' % (systemp))
        elif vio_server == 'vio2':
            vios = find_vios.returnVio2('%s' % (systemp))
        else:
            print 'Option for VIO invalid. Use vio1 or vio2.'

        def numfc_cmd():
            ''' The command to get the number of FCs available '''

            # get information on hmc from VIO
            lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"'
                    '| grep ^fcs | awk \'{ print $1 }\' | wc -l' %
                    (config.hmcserver, systemp, vios))

            return int(lsnports)

        # if cache file (CacheFile()) is enabled use that
        if config.npiv_cache == 'enable':

            lsnports = cachefile.CacheFile('%s/poweradm/npiv_cache/num_fc_%s_%s.cache' % (config.pahome,
                systemp, vios), config.npiv_cache_time, numfc_cmd, 't_print')
            lsnports.cache()

        else:

            print numfc_cmd()


    def printFCVIO(self, systemp, vio_server):
        ''' Get the array with FCs available from the VIO.

            Attributes:
            systemp     the system p name.
            vio_server  the vio do you want use:
                        options:
                            vio1 for #1 VIOS NPIV
                            vio2 for #2 VIOS NPIV
                            * this informations is used from the config file.
        '''

        # get informations about the VIOS from config file
        find_vios = systemvios.SystemVios()
        if vio_server == 'vio1':
            vios = find_vios.returnVio1('%s' % (systemp))
        elif vio_server == 'vio2':
            vios = find_vios.returnVio2('%s' % (systemp))
        else:
            print 'Option for VIO invalid. Use vio1 or vio2.'

        def printfc_cmd():
            ''' The command to get the list of FCs available '''

            # get information on hmc
            lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"'
                    '| grep ^fcs | awk \'{ print $1 }\'' %
                    (config.hmcserver, systemp, vios))
            lsnports_fc_list = lsnports
            return lsnports_fc_list

        # if cache file (CacheFile()) is enabled use that
        if config.npiv_cache == 'enable':

            lsnports = cachefile.CacheFile('%s/poweradm/npiv_cache/list_fcs_%s_%s.cache' % (config.pahome,
                systemp, vios), config.npiv_cache_time, printfc_cmd, 't_return')
            lsnports_fc_list = lsnports.cache()

        else:

            lsnports_fc_list = printfc_cmd()

        # make the array and returns
        list_fcs = []
        for line in lsnports_fc_list.split('\n'):
            list_fcs.append(line)
        return list_fcs

