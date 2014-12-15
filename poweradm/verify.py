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

class CheckOK:

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def mkCheck(self):
        check_ok = 0
        while check_ok == 0:
            self.answer = raw_input("%s" % (self.question))
            if (self.answer == 'y') or (self.answer == 'Y'):
                self.answer = 'y'
                check_ok = 1
            elif (self.answer == 'n') or (self.answer == 'N'):
                self.answer = 'n'
                check_ok = 1
            else:
                print ("Please use y or n!")
                check_ok = 0

    def answerCheck(self):
        return self.answer
