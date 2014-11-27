#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
#
# config file
#
# Copyright (c) 2014 Kairo Araujo
#
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
