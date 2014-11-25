#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
#
# Configuration
###############################################################################################
# hmc server
hmcserver = 'hmctvttsm01'
# Put here the minimum and maximum memory percent to lpars
mem_min = 50
mem_max = 50
# Put here the minimum and maximum cpu percent to lpars
cpu_min = 50
cpu_max = 100
# Systems and VIOS NPIV
# Important: Require two vios. If you have only one vios repeat the vios.
# Syntax: systems = {'SYSTEM_NAME1':['vio1','vio2'], 'SYSTEM_NAME2':['vio1','vio2']}
systems = {'P1-8205-E6D-SN06A07AT':['VIO1A','VIO2A'], 'P1-8205-E6D-SN06A07BT':['VIO1B','VIO2B'],
           'P1-8205-E6D-SN06A07CT':['VIO1B','VIO2B']}
# Virtual Switches
virtual_switches = ['VSW-GERENCIA-01', 'VSW-DADOS-01', 'VSW-BACKUP-01']
#
##############################################################################################
#     !! CAUTION !!  Only modify below if you are sure what you are doing !! CAUTION !!      #
##############################################################################################
#
# Importing classes/modules
import time
import os.path
##############################################################################################
#
# Global Variables
timestr = time.strftime("%d%m%Y-%H%M%S")
version = '0.1b'
#
# Classes
##############################################################################################

# get a next free id on systems
class newId:
    def __init__(self, newid):
        self.newid = newid

    # methods

    def mkId(self):
        ids = []
        systems_keys = list(systems.keys())
        systems_length = (len(systems.keys()))-1
        count = 0
        while count <= systems_length:
            #os.system('lssyscfg -m %s -r lpar -F lpar_id >> tmp/ids_%s' % (systems[count], timestr))
            os.system('cat simulacao/%s >> tmp/ids_%s' % (systems_keys[count], timestr))
            count += 1
        fileids = open('tmp/ids_%s' % (timestr), 'r')
        ids = fileids.readlines()
        ids.sort(key=int)
        lastid = len(ids)-1
        self.newid = int(ids[lastid])+1
        fileids.close()
        os.system('rm tmp/ids_%s' % (timestr))

    def getId(self):
        return self.newid

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



# Main

os.system('clear')
print ("\n\n[ Power Adm ]\n[ Version: %s - © 2014 Kairo Araujo - BSD License ]\n\n" % version)

print ("[LPAR Configuration ]\n")
change = raw_input("Change or Ticket number: ")

freeid = newId('newid')
freeid.mkId()
freeid.getId()

system_vio = systemVios('system', 'vio1', 'vio2')
system_vio.selectSystemVios()
system_vio.getSystem()
system_vio.getVio1()
system_vio.getVio1()


print (freeid.getId())
print (system_vio.getSystem())
print (system_vio.getVio1())
print (system_vio.getVio2())


