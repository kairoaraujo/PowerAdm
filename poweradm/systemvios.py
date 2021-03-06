#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
systemvios.py

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
import os.path
import config
##############################################################################################
#
# Class systemVios
##############################################################################################

class SystemVios:
    ''' Select, List and Show Systems and VIOs from configuration. '''

    def selectSystemVios(self):
        ''' Selection in ASCII mode Systems and VIOS. '''

        print ("\n[LPAR host Configuration]\n"
               "\nSelect the system host for LPAR")
        systems_keys = list(config.systems.keys())
        systems_length = (len(config.systems.keys()))-1
        count = 0
        while count <= systems_length:
            print ("%s : %s" % (count, systems_keys[count]))
            count += 1

        while True:
            try:
                system_option = int(raw_input("System: "))
                self.system = (systems_keys[system_option])
                break
            except (IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (systems_length))

        number_vios = len(config.systems[('%s' % systems_keys[system_option])])

        self.vio1 = config.systems[('%s' % systems_keys[system_option])][0]
        self.vio2 = config.systems[('%s' % systems_keys[system_option])][1]

        if number_vios == 4:
            self.vionet1 = config.systems[('%s' % systems_keys[system_option])][2]
            self.vionet2 = config.systems[('%s' % systems_keys[system_option])][3]

        elif number_vios == 2:
            self.vionet1 = self.vio1
            self.vionet2 = self.vio2

    def getSystem(self):
        ''' Get the System selected on selectSystemVios(). '''
        return self.system

    def getVio1(self):
        ''' Get the NPIV/SCSI VIO1 by Systemselected on selectSystemVios(). '''
        return self.vio1

    def getVio2(self):
        ''' Get the NPIV/SCSI VIO2 by System selected on selectSystemVios(). '''
        return self.vio2

    def getVioNet1(self):
        ''' Get the network VIO1 by System selected on selectSystemVios(). '''
        return self.vionet1

    def getVioNet2(self):
        ''' Get the network VIO2 by System selected on selectSystemVios(). '''
        return self.vionet2

    def printSystemList(self):
        ''' printthe list of Systems '''
        systems_keys = list(config.systems.keys())
        systems_length = (len(config.systems.keys()))-1
        count = 0
        while count <= systems_length:
            print ("%s" % (systems_keys[count]))
            count += 1

    def getSystemList(self):
        ''' Get the list of Systems. '''
        return config.systems.keys()

    def returnVio1 (self, system_option):
        ''' Indicating the system, returns the NPIV/SCSI VIO1. '''
        return (config.systems[system_option][0])

    def returnVio2 (self, system_option):
        ''' Indicating the system, returns the NPIV/SCSI VIO2. '''
        return (config.systems[system_option][1])

    def returnNetVio1 (self, system_option):
        ''' Indicating the system, returns the NETWORK VIO1. '''

        number_vios = len(config.systems.get(system_option))

        self.vio1 = config.systems.get(system_option)[0]
        self.vio2 = config.systems.get(system_option)[1]

        if number_vios == 4:
            self.vionet1 = config.systems.get(system_option)[2]
            self.vionet2 = config.systems.get(system_option)[3]

        elif number_vios == 2:
            self.vionet1 = self.vio1
            self.vionet2 = self.vio2

        return self.vionet1


    def returnNetVio2 (self, system_option):
        ''' Indicating the system, returns the NETWORK VIO2 '''

        number_vios = len(config.systems.get(system_option))

        self.vio1 = config.systems.get(system_option)[0]
        self.vio2 = config.systems.get(system_option)[1]

        if number_vios == 4:
            self.vionet1 = config.systems.get(system_option)[2]
            self.vionet2 = config.systems.get(system_option)[3]

        elif number_vios == 2:
            self.vionet1 = self.vio1
            self.vionet2 = self.vio2

        return self.vionet2
