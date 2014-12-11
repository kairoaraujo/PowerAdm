#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
#
# config file
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
# Configuration file
###############################################################################################
#

#
# BASIC CONFIGS
#

# hmc server
hmcserver = 'myhmcserver'

# Put here the minimum and maximum memory percent to lpars
mem_min = 50
mem_max = 50

# Put here the minimum and maximum cpu percent to lpars
cpu_min = 50
cpu_max = 100

# Systems and VIOS NPIV
# Important: Require two vios. If you have only one vio repeat the vio.
# Syntax: 'SYSTEM NAME':['VIO1','VIO2']
# - SYSTEM NAME: Is exactly name of your managed system.
# - VIO1: is exactly name of your VIO Primary partition.
# - VIO2: is exactly name of your VIO Secundary partition.
#
systems = {
           'P1-8205-E6D-SN06A07AT':['VIO1A','VIO2A'],
           'P1-8205-E6D-SN06A07BT':['VIO1B','VIO2B'],
           'P1-8205-E6D-SN06A07CT':['VIO1B','VIO2B']
          }

# Virtual Switches
virtual_switches = ['VSW-GERENCIA-01', 'VSW-DADOS-01', 'VSW-BACKUP-01']

#
# SHARED STORAGE POOL CONFIGS
#

# Do you have active Shared Storage Pool: yes or no
active_ssp = 'no'
# Cluster Name
cluster_name = 'cls01'
# Shared Storage Pools names
storage_pools = ['sp01', 'sp02']


#
# NIM OS DEPLOY CONFIGS
#

# Do you want enable deploy OS from NIM Server?
enable_nim_deploy = 'yes'

# Mode of deploy OS using nim
# Options:
#   mksysb = using mksysb and spot image
#      lpp = using lpp source and spot
nim_deploy_mode = 'mksysb'

# List of OS to deploy
# Syntax:
#   'NAME OF VERSION':['MKSYSB or LPP','SPOT']
#
# - NAME OF VERSION: is name to your version.
# - MKSYSB or LPP: is the same resource name on your NIM Server (lsnim). The field
#                  respect the nim_deploy_mode mksysb to mksysb and lpp to lpp.
# - SPOT: is the same resource name on your NIM Server (lsnim)
#
nim_os_deploy = {
                 'AIX 7.1 TL03 SP04 (Only NIM2)':['MKSYSB_AIX71TL03SP04','SPOT_AIX71TL03SP04'],
                 'AIX 6.1 TL09 SP04':['MKSYSB_AIX61TL09SP04','SPOT_AIX61TL09SP04'],
                 'AIX 5.3 TL12 SP04':['MKSYSB_AIX53TL12SP04','SPOT_AIX53TL03SP04']
                }


# NIM Serves
# Syntax:
#   'NAME OF NIM':['MANAGER IP/HOSTNAME', 'IP SERVER DEPLOY', 'RANGE USED TO DEPLOY']
#
# MANAGER IP/HOSTNAME: is address to access nim server using ssh
# IP SERVER DEPLOY: IP Addres of network deploy NIM (default nim interface)
# RANGE USED TO DEPLOY: range of IPs form your NIM Network.
#
#   Important: supports max 24 bits network. 1-254 addresses
#
nimservers = {
              'NIM1':['nimserver1', '10.0.0.1', '10.0.0.11-254'],
              'NIM2':['200.185.178.30', '10.0.1.1', '10.0.1.11-254']
             }

#
# OTHERS CONFIGS
# To change check the mksyscfg HMC help commands
# ** Important: only default settings below are tested.
#
# Processor Mode
proc_mode = 'shared'

# Shared Mode
sharing_mode = 'uncap'

# Shared Weigth
uncap_weight = '128'

# Boot Mode
boot_mode = 'norm'

# Enable/Disable monitoring
conn_monitoring = '1'

