#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# nimfilefind.py
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
# Class FindNIMFile
##############################################################################################

class NIMFileFind:

    def __init__(self, title, filedir, action):
        self.title = title
        self.filedir = filedir
        self.action = action

    def selectDeploy(self):

        print ("\n[Deploy OS NIM: %s]\n"
               "\nSelect the Deploy:\n" % (self.title))
        listDeploys = fnmatch.filter(os.listdir("%s" % (self.filedir)), "*.nim")
        listDeploys_length = len(listDeploys)-1
        if listDeploys_length == -1:
            print ('\033[1;31mNo Deploys found.\033[1;00m\n\n'
                   '- No LPAR was configured to perform deploy.\n'
                   '- The LPAR has not yet been created.\n'
                   '\nExiting\n')
            exit()
        count = 0
        while count <= listDeploys_length:
            print ("%s : %s" % (count, listDeploys[count]))
            count += 1

        while True:
            try:
                deploy_option = int(raw_input("\nWhat's OS Deploy NIM you want %s?: " % (self.action)))
        	self.deploy_exec = (listDeploys[deploy_option])
                break
            except(IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (listDeploys_length))


    def getDeploy(self):
        return self.deploy_exec
