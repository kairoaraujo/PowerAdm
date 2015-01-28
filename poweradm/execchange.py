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
from globalvar import *
##############################################################################################
#
# Class ExecChange
##############################################################################################

class ExecChange:

    def __init__(self, changefile):
        self.changefile = changefile

    def runChange(self):

        print ("\nRuning change/ticket %s" % (self.changefile))
        os.system("sh %s" % (self.changefile))
        f_change_executed = open(self.changefile, 'r')
        os.system('mv %s %s/poweradm/changes_executed/' % (self.changefile, pahome))
        print ('Change/ticket %s finished. Verfify configs on your environment.\nExiting!'
                % (self.changefile))
        for line in f_change_executed.readlines():
            if line.startswith('#LPARID'):
                lparidcreated = line.split()
                print ('Removing ID %s from reserved ids' % (lparidcreated[1]))
                file_reservedids = open('%s/poweradm/data/reserved_ids' % (pahome))
                line_reservedids = file_reservedids.readlines()
                file_reservedids.close()
                file_reservedids = open('%s/poweradm/data/reserved_ids' % (pahome), 'w')
                for lineids in line_reservedids:
                    file_reservedids.write(lineids.replace((lparidcreated[1]), "0"))
                file_reservedids.close()
        f_change_executed.close()
