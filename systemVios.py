#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
# Importing classes/modules
import time
import os.path
from globalvar import *
from config import *
from newid import *
##############################################################################################
#
# Class systemVios
##############################################################################################

class systemVios:
    def __init__(self, system, vios1, vios2):
        self.system = system
        self.vios1 = vios1
        self.vios2 = vios2

    def selectSystemVios(self):

        print ("\nSelect the system host for LPAR")
        systems_keys = list(systems.keys())
        systems_length = (len(systems.keys()))-1
        count = 0
        while count <= systems_length:
            print ("%s : %s" % (count, systems_keys[count]))
            count += 1
        system_option = int(raw_input("System: "))
        self.system = (systems_keys[system_option])
        self.vio1 = systems[('%s' % systems_keys[system_option])][0]
        self.vio2 = systems[('%s' % systems_keys[system_option])][1]

    def getSystem(self):
        return self.system

    def getVio1(self):
        return self.vio1

    def getVio2(self):
        return self.vio2



