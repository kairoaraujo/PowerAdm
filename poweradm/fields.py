#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# verify.py
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
#
# Importing classes/modules
import time
import os.path
from globalvar import *
from config import *
from poweradm import *


class Fields:

    def __init__(self, variable, field, textField):
        self.variable = variable
        self.field = field
        self.textField = textField

    def chkFieldStr(self):

        while True:

            self.variable = raw_input('%s' % (self.textField))
            if (self.variable.isspace() == True) or ( self.variable == '') or (' ' in self.variable):
                print ("%s can not be blank or contain spaces" % (self.field))
            else:
                break

    def srtVarOut(self):
        return self.variable

    # get and check a field with float value
    def chkFieldFloat(self):

        while True:

            self.variable = raw_input('%s' % (self.textField))
            if (self.variable.isspace() == True) or ( self.variable == '') or (' ' in self.variable):
                print ("%s can not be blank or contain spaces" % (self.field))
            else:
                checkstring = True
                break

    def floatVarOut(self):
        return self.variable

