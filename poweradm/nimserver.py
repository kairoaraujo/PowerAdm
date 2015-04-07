#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
nimserver.py

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
import time
import os.path
from globalvar import *
from config import *
##############################################################################################
#
# Class NimServer
##############################################################################################

class NimServer:
    def selectNim(self):
        ''' Text interactive menu to select informations of NIM Server from 
            config.
        '''

        print ("\n[Deploy NIM: NIM Server Select]\n"
               "\nSelect the NIM Server")
        nimservers_keys = list(nimservers.keys())
        nimservers_length = (len(nimservers.keys()))-1
        count = 0
        while count <= nimservers_length:
            print ("%s : %s" % (count, nimservers_keys[count]))
            count += 1

        while True:
            try:
		nimserver_option = int(raw_input("NIM Server: "))
        	self.nimserver = (nimservers_keys[nimserver_option])
                break
            except(IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (nimservers_length))

        self.address = nimservers[('%s' % nimservers_keys[nimserver_option])][0]
        self.ipdeploy = nimservers[('%s' % nimservers_keys[nimserver_option])][1]
        self.gwdeploy = nimservers[('%s' % nimservers_keys[nimserver_option])][2]
        self.iprange = nimservers[('%s' % nimservers_keys[nimserver_option])][3]
        ipstartend = self.iprange.split('-')
        self.ipnet = ipstartend[0].split('.')
        self.ipstart = self.ipnet[3]
        self.ipnet = ('%s.%s.%s.' % (self.ipnet[0], self.ipnet[1], self.ipnet[2]))
        self.ipend = ipstartend[1]

    def getNimServer(self):
        ''' return NIM Server from selectNim(). '''

        return self.nimserver

    def getNimAddress(self):
        ''' return NIM address from selectNim(). '''

        return self.address

    def getNimIPDeploy(self):
        ''' return NIM IP Deploy from selectNim(). '''

        return self.ipdeploy

    def getNIMGWDeploy(self):
        ''' return NIM gateway from selectNim(). '''

        return self.gwdeploy

    def getIPRange(self):
        ''' return NIM IP range from selectNim(). '''

        return self.iprange

    def getIPNet(self):
        ''' return NIM IP network from selectNim(). '''

        return self.ipnet

    def getIPStart(self):
        ''' return NIM IP start from selectNim(). '''

        return self.ipstart

    def getIPEnd(self):
        ''' return NIM End from selectNim(). '''

        return self.ipend
