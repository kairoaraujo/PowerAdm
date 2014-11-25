#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
# Importing classes/modules
import time
import os.path
from globalvar import *
from config import *
from newid import *
from systemVios import *

# Main
#
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


