#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# systemVios.py
#
# Copyright (c) 2014, 2015 Kairo Araujo
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
from globalvar import *
from config import *
##############################################################################################
#
# Class systemVios
##############################################################################################

class SystemVios:
    ''' Select, List and Show Systems and VIOs from configuration. '''

    def selectSystemVios(self):
        ''' Selection in ASCII mode Systems and VIOS '''

        print ("\n[LPAR host Configuration]\n"
               "\nSelect the system host for LPAR")
        systems_keys = list(systems.keys())
        systems_length = (len(systems.keys()))-1
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

        number_vios = len(systems[('%s' % systems_keys[system_option])])

        self.vio1 = systems[('%s' % systems_keys[system_option])][0]
        self.vio2 = systems[('%s' % systems_keys[system_option])][1]

        if number_vios == 4:
            self.vionet1 = systems[('%s' % systems_keys[system_option])][2]
            self.vionet2 = systems[('%s' % systems_keys[system_option])][3]

        elif number_vios == 2:
            self.vionet1 = self.vio1
            self.vionet2 = self.vio2

    def getSystem(self):
        ''' Get the System selected on selectSystemVios() '''
        return self.system

    def getVio1(self):
        ''' Get the NPIV/SCSI VIO1 by Systemselected on selectSystemVios() '''
        return self.vio1

    def getVio2(self):
        ''' Get the NPIV/SCSI VIO2 by System selected on selectSystemVios() '''
        return self.vio2

    def getVioNet1(self):
        ''' Get the network VIO1 by System selected on selectSystemVios() '''
        return self.vionet1

    def getVioNet2(self):
        ''' Get the network VIO2 by System selected on selectSystemVios() '''
        return self.vionet2

    def printSystemList(self):
        ''' Get the list of Systems '''
        systems_keys = list(systems.keys())
        systems_length = (len(systems.keys()))-1
        count = 0
        while count <= systems_length:
            print ("%s" % (systems_keys[count]))
            count += 1

    def returnVio1 (self, system_option):
        ''' Indicating the system, returns de NPIV/SCSI VIO1 '''
        return (systems[system_option][0])

    def returnVio2 (self, system_option):
        ''' Indicating the system, returns de NPIV/SCSI VIO1 '''
        return (systems[system_option][1])

