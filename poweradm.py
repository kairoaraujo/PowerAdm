#!/usr/bin/env python
#
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
# Systems
systems = ['P1-8205-E6D-SN06A07AT', 'P1-8205-E6D-SN06A07BT', 'P1-8205-E6D-SN06A07CT']
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
    def __init__(self, ids, newid):
        self.ids = ids
        self.newid = newid

    # methods

    def mkId(self):
        ids = []
        systems_length = (len(systems))-1
        count = 0
        while count <= systems_length:
            #os.system('lssyscfg -m %s -r lpar -F lpar_id >> tmp/ids_%s' % (systems[count], timestr))
            os.system('cat simulacao/%s >> tmp/ids_%s' % (systems[count], timestr))
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


# Main

os.system('clear')
print ("\n\n[ Power Adm ]\n[ Version: %s - © 2014 Kairo Araujo - BSD License ]\n\n" % version)

print ("[LPAR Configuration ]\n")
change = input("Change or Ticket number: ")

freeid = newId('nids', 'nnewid')
freeid.mkId()
freeid.getId()

print ("\nSelect the system host for LPAR")
systems_length = (len(systems))-1
count = 0
while count <= systems_length:
    print ("%s : %s" % (count, systems[count]))
    count += 1
system_option = int(input("System: "))
#print ("%s" % systems[system_option]) - test



