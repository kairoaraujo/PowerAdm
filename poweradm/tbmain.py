#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# tbmain.py
#
# Copyright (c) 2015 Kairo Araujo
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
import globalvar
import tbenv
import tblpar
import fields
##############################################################################################

def tbmain():
    ''' Menu for Troubleshooting option '''

    # main menu
    patb = raw_input("\n[Troubleshooting options]\n\n"
                  "Select an option\n\n"
                  "1. Verify environment.\n"
                  "2. Verify specific LPAR.\n\n"
                  "Please choose an option: ")

    # environment menu
    if patb == '1':
        envtb = raw_input("\n[Troubleshooting Environment]\n\n"
                          "Select an option\n\n"
                          "1. Check SEAs (by lsseas).\n"
            		      "2. Check NPIVs.\n\n"
                          "Please choose an option: ")
	    # environment actions SEA and NPIV
        if envtb == '1':
            env = tbenv.TBEnv()
            env.lsseas()

        elif envtb == '2':
            env = tbenv.TBEnv()
            env.lsnpivs()

    # LPAR menu
    if patb == '2':
        type_search = raw_input("\n[Troubleshooting LPAR]\n\n"
                            	"1. Specific LPAR ID.\n"
				                "2. Find LPAR. \n\n"
				                "Please choose an option: ")
        # LPAR by ID
        if type_search == '1':
	        lpar_search = raw_input("\nLPAR ID: ")
	        search_type = 'by_id'

        # LPAR by name
        elif type_search == '2':
            lpar_string = fields.Fields('The search', '\nLPAR name or part of name: ')
            lpar_string.chkFieldStr()
            lpar_search = lpar_string.strVarOut()
            search_type = 'by_str'
        else:
	        exit()

        # LPAR types of check
        tblpar_option = raw_input("\n[Troubleshooting LPAR]\n\n"
                                     "Select an option\n\n"
                                     "1. All (Info, vSCSI, vFC and vNetwork)\n"
                                     "2. Info (basic info as DLPAR, ID, memory, cpu etc)\n"
                                     "3. vSCSI \n"
                                     "4. vFC (NPIV)\n"
                                     "5. vNetwork\n"
                                     "Please choose an option: ")
        # all check
        if tblpar_option == '1':
            tblpar.run(lpar_search, search_type,  'all')

        # info check
        elif tblpar_option == '2':
            tblpar.run(lpar_search, search_type, 'info')

        # vscsi check
        elif tblpar_option == '3':
            tblpar.run(lpar_search, search_type, 'vscsi')

    	# vfc check
        elif tblpar_option == '4':
            tblpar.run(lpar_search, search_type, 'vfc')

        # vnet check
        elif tblpar_option == '5':
            tblpar.run(lpar_search, search_type, 'vnet')

