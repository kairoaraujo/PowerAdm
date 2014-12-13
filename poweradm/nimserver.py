#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# createdeploynim.py
#
# Copyright (c) 2014 Kairo Araujo
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
# Class NimServer
##############################################################################################

class NimServer:
    def selectNim(self):

        print ("\n[Deploy NIM: NIM Server Select]\n"
               "\nSelect the NIM Server")
        nimservers_keys = list(nimservers.keys())
        nimservers_length = (len(nimservers.keys()))-1
        count = 0
        while count <= nimservers_length:
            print ("%s : %s" % (count, nimservers_keys[count]))
            count += 1
        nimserver_option = int(raw_input("NIM Server: "))
        self.nimserver = (nimservers_keys[nimserver_option])
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
        return self.nimserver

    def getNimAddress(self):
        return self.address

    def getNimIPDeploy(self):
        return self.ipdeploy

    def getNIMGWDeploy(self):
        return self.gwdeploy

    def getIPRange(self):
        return self.iprange

    def getIPNet(self):
        return self.ipnet

    def getIPStart(self):
        return self.ipstart

    def getIPEnd(self):
        return self.ipend
