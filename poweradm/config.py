#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PowerAdm
Config file

Copyright (c) 2014-2016 Kairo Araujo.

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

IBM, Power, PowerVM (a.k.a. VIOS) are registered trademarks of IBM Corporation
in the United States, other countries, or both.
VMware, vCenter, vCenter Orchestrator are registered trademarks of VWware Inc
in the United States, other countries, or both.
"""
# Configuration file
###############################################################################
#

#
# BASIC CONFIGS
#

# PowerAdm installation path
pahome='/home/poweradm/PowerAdm'

# HMC server (name or IP)
hmcserver = 'myhmcserver'

# Put here the default minimum and maximum memory percent.
# This value will be used to setup the LPAR profile.
# For example, using 50 for min and max. If LPAR is created with 10GB, the
# minimum will be 10GB-50% and maximum will be 10G+50%.
# It will be used by Dynamic LPAR (DLPAR).
mem_min = 50
mem_max = 50

# Put here the default minimum and maximum CPU percent.
# It works as works for memory.
cpu_min = 50
cpu_max = 100

# Virtual Slots IDs Standardize
# It will create the Virtual Adapter IDs standardized.
# To enable (True) it some requirements are necessary, please check out in
# http://poweradm.org/requirements.html section: Virtual Slots IDs Standardize.
# Using it as enable (True) the standard follows this:
# On VIOSes:
# - vSCSI: Primary VIOS: 1+LPAR ID | Secondary VIOS: 2+LPAR ID
# - vHBA : Primary VIOS: 3+LPAR ID | Secondary VIOS: 4+LPAR ID
# Using it as disable (False)
# It will use the first virtual slot ID available on VIOSes
vslot_std = False

# Systems and VIOSes
# Important: Requires minimum two VIOSes.
# If you have only one VIOS, duplicate the VIOS name.
#      i.e: 'P1-8205-E6D-SN06A07AT':['VIO1A','VIO1A'],
# If you have segregated VIOSes for vSCSI
# Syntax: 'SYSTEM NAME':['VIO1','VIO2']
# - SYSTEM NAME: Is exactly name of your managed system.
# - VIO1: is exactly name of your VIO Primary partition.
# - VIO2: is exactly name of your VIO Secundary partition.
systems = {
           'P1-8205-E6D-SN06A07AT':['VIO1A','VIO1A'],
           'P2-8205-E6D-SN06A07BT':['VIO3B','VIO4B'],
           'P3-8205-E6D-SN06A07CT':['VIO1C','VIO2C']
          }

# Virtual Switches
virtual_switches = ['VSW-MANAGER-01', 'VSW-DATA-01', 'VSW-BACKUP-01']

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

# Basic Operation System Install Data resource (bosinst_data)
# Syntax:
#    Use the resource name or '' for none
nim_bosinst_data_res = 'bosinst_data'

# List of OS to deploy
# Syntax:
#   'NAME OF VERSION':['MKSYSB or LPP','SPOT']
#
# - NAME OF VERSION: it is name to your version and comments or description
# - MKSYSB or LPP: it is the same resource name on your NIM Server (lsnim).
#                  The field respect the nim_deploy_mode mksysb to mksysb and
#                  lpp to lpp.
# - SPOT: it is the same resource name on your NIM Server (lsnim)
#
nim_os_deploy = {
                 'AIX 7.1 TL03 SP04 (Only in NIMSRV2)':['MKSYSB_AIX71TL03SP04','SPOT_AIX71TL03SP04'],
                 'AIX 6.1 TL09 SP04':['MKSYSB_AIX61TL09SP04','SPOT_AIX61TL09SP04'],
                 'AIX 5.3 TL12 SP04':['MKSYSB_AIX53TL12SP04','SPOT_AIX53TL03SP04']
                }

# NIM Serves
# Syntax:
#   'NAME OF NIM':['MANAGER IP/HOSTNAME', 'IP SERVER DEPLOY', 'IP GATEWAY DEPLOY', 'RANGE USED TO DEPLOY']
#
# NAME OF NIME: it is the name description and comments
# MANAGER IP/HOSTNAME: it is address to access nim server using ssh
# IP SERVER DEPLOY: IP Address of network deploy NIM (default nim interface)
# IP GATEWAY DEPLOY: Gateway IP address used by NIM Network.
# RANGE USED TO DEPLOY: range of IPs form your NIM Network.
#
#   Remark: supports max 24 bits network. 1-254 addresses
#
nimservers = {
              'NIMSRV01 (available for P1 only)':['nimserver1', '10.0.0.1', '10.0.0.254', '10.0.0.11-254'],
              'NIMSRV02':['200.185.178.30', '10.0.1.1', '10.0.1.254', '10.0.1.11-254']
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

# Debug api parser
api_debug = 'no'

# NPIV Cache
#
# running the 'lsnports' in some VIOS can take a few long seconds.
# the cache can be used.
#
# disable or enable option
npiv_cache = 'enable'
# time to update the cache files in seconds
npiv_cache_time = '86400'

# Web Interface - totally beta ;)
#
# Web port to listen
web_port = '8080'
# web IP to listen (0.0.0.0 listening all IPs)
web_address = '0.0.0.0'
