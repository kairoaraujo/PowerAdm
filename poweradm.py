#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
'''
PowerAdm
poweradm.py

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
from poweradm.poweradm import main_poweradm
import poweradm.config
import commands

print "\nChecking HMC connection..."
chk_hmc_connection = commands.getstatusoutput('ssh -l poweradm %s lshmc -V' %
        poweradm.config.hmcserver)

if chk_hmc_connection[0] -= 0:
    print "\nConnection to HMC passed!"
    try:
        main_poweradm()
        ''' Import the main of PowerAdm '''
    except(KeyboardInterrupt):
        print ("\n\nCtrl+C pressed! Exiting without save.\n")
else:
    print "\nConnection to HMC failed!"
    print "  Error:\n\t %s\n" % chk_hmc_connection[1]
