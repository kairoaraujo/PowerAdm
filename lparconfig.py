#!/usr/bin/env python
#
# Copyright (c) 2014 Kairo Araujo
#
# vvu is vio vhost utility
# This program was created to help in managing vhost devices and its hdisks
# in PowerVM (vios) servers. It was created for personal use. There are no
# guarantees of the author. Use at your own risk.
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

# import modules
###############################################################################################
import os.path
import time
from globalvar import *
from config import *
from newid import *
from systemVios import *
from verify import *



file_change.write("mksyscfg -r lpar -m %s -i 'name=%s-%s, "
               "lpar_id=%s ,profile_name=%s, lpar_env=aixlinux, min_mem=%s "
               "desired_mem=%s, max_mem=%s, proc_mode=shared, min_procs=%s,"
               "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
               "max_proc_units=%s, sharing_mode=uncap, uncap_weight=128, conn_monitoring=1, "
               "boot_mode=norm, max_virtual_slots=40, "
               "\'virtual_eth_adapters=%s"
               "\'virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\' '\n"
               % ( systems[system_option], self.prefix, self.lparname, nextid, self.lparname,
               lparmenmin, self.lparmem, lparmenmax, lparvcpumin, self.lparvcpu,
               lparvcpumax,lparentcpumin, self.lparentcpu, lparentcpumax,
               virtual_eth_adapters, vios[0], nextid, vios[1], nextid))






