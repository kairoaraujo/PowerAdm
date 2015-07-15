#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
findlpar.py

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
import os
import fnmatch
import config
##############################################################################################
#
# Class FindChange
##############################################################################################

class FindChange:
    ''' Find existents changes/ticket to execute. '''

    def selectChange(self):
        ''' Select the change/ticket file. '''

        print ("\n[LPAR creation]\n"
               "\nSelect the Change/Ticket to execute:\n")
        listChanges = fnmatch.filter(os.listdir("%s/poweradm/changes/" % config.pahome), "*.sh")
        listChanges_length = len(listChanges)-1
        if listChanges_length == -1:
            print ('No changes found. Exiting\n')
            exit()
        count = 0
        while count <= listChanges_length:
            print ("%s : %s" % (count, listChanges[count]))
            count += 1

        while True:
            try:
	    	change_option = int(raw_input("\nWhat's change/ticket id you want execute?: "))
        	self.change_exec = (listChanges[change_option])
                break
            except(IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (listChanges_length))


    def getChange(self):
        ''' Returns the file change/ticket. '''
        return self.change_exec
