#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# tbenv.py
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
import systemvios
import config
import lsnpivs
##############################################################################################

class TBEnv:

    def lsseas(self):
        print ("\n[Troubleshooting - SEA] Select Server]\n"
               "\nSelect Server to check SEA")
        netvios = systemvios.SystemVios()
        netvios.selectSystemVios()
        system = netvios.getSystem()
        netvios1 = netvios.getVioNet1()
        netvios2 = netvios.getVioNet2()
       
  	print ('\n\n') 
	print ('\033[94m#\033[1;00m' * 80)
        print ('# \033[94m %s \033[1;00m - Check SEA configuration and state' % netvios1)
        print ('\033[94m#\033[1;00m' * 80)

        os.system("ksh %s/poweradm/tools/lsseas -c %s %s %s" % (config.pahome, config.hmcserver, system, netvios1))

  	print ('\n\n') 
	print ('\033[94m#\033[1;00m' * 80)
        print ('# \033[94m %s \033[1;00m - Check SEA configuration and state' % netvios2)
        print ('\033[94m#\033[1;00m' * 80)

        os.system("ksh %s/poweradm/tools/lsseas -c %s %s %s" % (config.pahome, config.hmcserver, system, netvios2))

    def lsnpivs(self):
        print ("\n[Troubleshooting - NPIV] Select Server]\n"
               "\nSelect Server to check NPIV")
        vios = systemvios.SystemVios()
        vios.selectSystemVios()
        system = vios.getSystem()
        vios1 = vios.getVio1()
        vios2 = vios.getVio2()
       
  	print ('\n\n') 
	print ('\033[94m#\033[1;00m' * 80)
        print ('# \033[94m %s \033[1;00m - Check NPIV configuration and state' % vios1)
        print ('\033[94m#\033[1;00m' * 80)
	
	lsnpivs.run(config.hmcserver, system, vios1, 'all')	

  	print ('\n\n') 
	print ('\033[94m#\033[1;00m' * 80)
        print ('# \033[94m %s \033[1;00m - Check NPIV configuration and state' % vios2)
        print ('\033[94m#\033[1;00m' * 80)

	
	lsnpivs.run(config.hmcserver, system, vios2, 'all')	



