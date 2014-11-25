#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
# Importing classes/modules
import time
import os.path
from globalvar import *
from config import *

class checkOk:

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
                answer = 'n'
                check_ok = 1
            else:
                print ("Please use y or n!")
                check_ok = 0

    def answerCheck(self):
        return self.answer



