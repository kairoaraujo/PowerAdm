#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# createlpar.py
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
import os
import fnmatch
from globalvar import *
##############################################################################################
#
# Class findChange
##############################################################################################

class findChange:

    def __init__(self, change_exec):
        self.change_exec = change_exec

    def selectChange(self):

        print ("\n[LPAR creation]\n"
               "\nSelect the Change/Ticket to execute:\n")
        listChanges = fnmatch.filter(os.listdir("poweradm/changes/"), "*.sh")
        listChanges_length = len(listChanges)-1
        if listChanges_length == -1:
            print ('No changes found. Exiting\n')
            exit()
        count = 0
        while count <= listChanges_length:
            print ("%s : %s" % (count, listChanges[count]))
            count += 1
        change_option = int(raw_input("\nWhat's change/ticket id you want execute?: "))
        self.change_exec = (listChanges[change_option])

    def getChange(self):
        return self.change_exec
