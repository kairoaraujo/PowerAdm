#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
# Class newid.py
##############################################################################################
import time
import os.path
from globalvar import *
from config import *

# get a next free id on systems
class newId:
    def __init__(self, newid):
        self.newid = newid

    def mkId(self):
        ids = []
        systems_keys = list(systems.keys())
        systems_length = (len(systems.keys()))-1
        count = 0
        while count <= systems_length:
            #os.system('lssyscfg -m %s -r lpar -F lpar_id >> tmp/ids_%s' % (systems[count], timestr))
            os.system('cat simulation/%s >> tmp/ids_%s' % (systems_keys[count], timestr))
            os.system('cat data/reserved_ids >> tmp/ids_%s' % (timestr))
            if os.path.isfile('tmp/reserved_ids_%s' % (timestr)):
                os.system('cat tmp/reserved_ids_%s >> tmp/ids_%s' % (timestr, timestr))
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


