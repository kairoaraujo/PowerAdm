#!/usr/bin/env python
## -*- coding: utf-8 -*-
#
# PowerAdm
#
# Configuration file
###############################################################################################
#
# hmc server
hmcserver = 'hmctvttsm01'
# Put here the minimum and maximum memory percent to lpars
mem_min = 50
mem_max = 50
# Put here the minimum and maximum cpu percent to lpars
cpu_min = 50
cpu_max = 100
# Systems and VIOS NPIV
# Important: Require two vios. If you have only one vios repeat the vios.
# Syntax: systems = {'SYSTEM_NAME1':['vio1','vio2'], 'SYSTEM_NAME2':['vio1','vio2']}
systems = {'P1-8205-E6D-SN06A07AT':['VIO1A','VIO2A'], 'P1-8205-E6D-SN06A07BT':['VIO1B','VIO2B'],
           'P1-8205-E6D-SN06A07CT':['VIO1B','VIO2B']}
# Virtual Switches
virtual_switches = ['VSW-GERENCIA-01', 'VSW-DADOS-01', 'VSW-BACKUP-01']
