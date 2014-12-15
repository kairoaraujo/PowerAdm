#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# nimclear.py
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
from verify import *
from nimfilefind import *
from getnimver import *
from nimserver import *
##############################################################################################

def nimclear():

    # select a machine to deploy
    nimrm = NIMFileFind('Select Deploy', 'poweradm/nim_executed/', 'remove')
    nimrm.selectDeploy()

    # get variables
    f_nim_deploy = open("poweradm/nim_executed/%s" % (nimrm.getDeploy()), 'r')
    for line in f_nim_deploy.readlines():
        if line.startswith('#PREFIX'):
            lpar = line.split()
            lparprefix = lpar[1]
        if line.startswith('#LPARNAME'):
            lpar = line.split()
            lparname = lpar[1]
        if line.startswith('#IP'):
            lpar = line.split()
            lparip = lpar[1]
        if line.startswith('#NIMSERVER'):
            lpar = line.split()
            lparnim = lpar[1]
        if line.startswith('#NIMADDRESS'):
            lpar = line.split()
            lparnimaddress = lpar[1]

    rmhostnim = CheckOK('Proceed to Remove?(y/n): ', 'n')
    rmhostnim.mkCheck()

    if rmhostnim.answerCheck() == 'y':

        f_nim_rm = open('poweradm/changes/nim_rm_%s-%s_%s.nim' % (lparprefix, lparname, timestr), 'w')

        def f_nimrm_chksh():
            f_nim_rm.write("\nif [ $? != 0 ];"
                            "then\n"
                            "\techo 'An error has occurred. Check the actions taken.'; \n"
                            "\texit;\n"
                            "else\n"
                            "\techo 'Command OK. Continuing';\n"
                            "fi\n")

        f_nim_rm.write("#!/bin/sh")

        f_nim_rm.write("\n\necho 'Reseting machine %s in NIM Server'\n" % (lparname))
        f_nim_rm.write("\n\nssh -l poweradm %s sudo nim -o reset -a force=yes -a force=yes \'%s\'\n"
                % (lparnimaddress, lparname))
        f_nimrm_chksh()

        f_nim_rm.write("\n\necho 'Deallocate resources from machine %s in NIM Server'\n" % (lparname))
        f_nim_rm.write("\n\nssh -l poweradm %s sudo nim -Fo deallocate -a subclass=all -a force=yes \'%s\'\n" %
                (lparnimaddress, lparname))
        f_nimrm_chksh()

        f_nim_rm.write("\n\necho 'Removing machine %s from NIM Server'\n" % (lparname))
        f_nim_rm.write("\n\nssh -l poweradm %s sudo nim -o remove \'-F\' \'%s\'\n" % (lparnimaddress, lparname))
        f_nimrm_chksh()

        f_nim_rm.write("\n\necho 'Removing host %s from NIM Server /etc/hosts'\n" % (lparname))
        f_nim_rm.write("\n\nssh -l poweradm %s sudo hostent -d %s" % (lparnimaddress, lparip))
        f_nimrm_chksh()

        f_nim_rm.write("\n\nrm poweradm/nim_executed/%s" % (nimrm.getDeploy()))
        f_nimrm_chksh()

        f_nim_rm.close()

        print ('\n\nRemoving server %s-%s from NIM...' % (lparprefix, lparname))
        os.system('sh poweradm/changes/nim_rm_%s-%s_%s.nim' % (lparprefix, lparname, timestr))
        os.system('mv poweradm/changes/nim_rm_%s-%s_%s.nim poweradm/changes_executed/' % (lparprefix,
            lparname, timestr))

        print ('Removing ID %s from reserved IPs' % (lparip))
        file_reservedips = open('poweradm/data/reserved_ips', 'r')
        line_reservedips = file_reservedips.readlines()
        file_reservedips.close()
        file_reservedips = open('poweradm/data/reserved_ips', 'w')
        for lineips in line_reservedips:
            file_reservedips.write(lineips.replace((lparip), "#%s" % (lparip)))
            file_reservedips.close()

        print ('\nExiting.\n\n')
    else:
        print ('\nAborting.\n\n')
