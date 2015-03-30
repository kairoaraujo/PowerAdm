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
##############################################################################################

def tbmain():

    patb = raw_input("\n[Troubleshooting options]\n\n"
                  "Select a option\n\n"
                  "1. Verify environment.\n"
                  "2. Verify specific LPAR.\n\n"
                  "Please choose an option: ")

    if patb == '1':
        envtb = raw_input("\n[Troubleshooting Environment]\n\n"
                          "Select a option\n\n"
                          "1. Check SEAs (by lsseas).\n"
			  "2. Check NPIVs.\n\n"
                          "Please choose an option: ")

        if envtb == '1':
           env = tbenv.TBEnv()
           env.lsseas()
        
	elif envtb == '2':
           env = tbenv.TBEnv()
           env.lsnpivs()




