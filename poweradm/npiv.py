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
##############################################################################################
#
# Class NPIV
##############################################################################################

class NPIV:
    ''' Get informations about NPIV on the VIOS. '''


    def lsnportsVIO1(self, systemp):
        ''' Select the change/ticket file. '''

        find_vios = systemvios.SystemVios()
        vio1 = find_vios.returnVio1('%s' % (systemp))

        # get information on hmc
        lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' %
                (config.hmcserver, systemp, vio1))

        # if exists file npiv notes get
        if os.path.isfile('%s/npiv/%s-%s' % ( config.pahome, systemp, vio1)):
            npiv_notes = commands.getoutput('cat %s/npiv/%s-%s' % ( config.pahome, systemp, vio1))
        else:
            npiv_notes = ""

        print ("%s \n %s" % (lsnports, npiv_notes))

    def lsnportsVIO2(self, systemp):
        ''' Select the change/ticket file. '''

        find_vios = systemvios.SystemVios()
        vio2 = find_vios.returnVio2('%s' % (systemp))

        # get information on hmc
        lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"' %
                (config.hmcserver, systemp, vio2))

        # if exists file npiv notes get
        if os.path.isfile('%s/npiv/%s-%s' % ( config.pahome, systemp, vio2)):
            npiv_notes = commands.getoutput('cat %s/npiv/%s-%s' % ( config.pahome, systemp, vio2))
        else:
            npiv_notes = ""

        print ("%s \n %s" % (lsnports, npiv_notes))


    def numberFCVIO1(self, systemp):
        ''' Select the change/ticket file. '''

        find_vios = systemvios.SystemVios()
        vio1 = find_vios.returnVio1('%s' % (systemp))

        # get information on hmc
        lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"'
                '| grep ^fcs | awk \'{ print $1 }\' | wc -l' %
                (config.hmcserver, systemp, vio1))

        return int(lsnports)

    def numberFCVIO2(self, systemp):
        ''' Select the change/ticket file. '''

        find_vios = systemvios.SystemVios()
        vio2 = find_vios.returnVio2('%s' % (systemp))

        # get information on hmc
        lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"'
                '| grep ^fcs | awk \'{ print $1 }\' | wc -l' %
                (config.hmcserver, systemp, vio2))

        return int(lsnports)

    def printFCVIO1(self, systemp):
        ''' Select the change/ticket file. '''

        find_vios = systemvios.SystemVios()
        vio1 = find_vios.returnVio1('%s' % (systemp))

        # get information on hmc
        lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"'
                '| grep ^fcs | awk \'{ print $1 }\'' %
                (config.hmcserver, systemp, vio1))

        list_fcs = []
        for line in lsnports.split('\n'):
            list_fcs.append(line)

        return list_fcs


    def printFCVIO2(self, systemp):
        ''' Select the change/ticket file. '''

        find_vios = systemvios.SystemVios()
        vio2 = find_vios.returnVio2('%s' % (systemp))

        # get information on hmc
        lsnports = commands.getoutput('ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsnports\'\"'
                '| grep ^fcs | awk \'{ print $1 }\'' %
                (config.hmcserver, systemp, vio2))

        list_fcs = []
        for line in lsnports.split('\n'):
            list_fcs.append(line)

        return list_fcs



