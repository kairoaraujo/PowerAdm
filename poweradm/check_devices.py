#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
check_devices.py

Copyright (c) 2015 Kairo Araujo.

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
'''

# Imports
###############################################################################
import commands
import globalvar
import config
import os.path


def check(dev_type, hmc, psystem, vio, dev_id):
    '''
        This function check if a ID is used by devices in Virtual I/O (VIOS).
        This requires some arguments:

        dev_type    : vscsi for Virtual SCSI or vfc for Virtual Fiber Channel
        hmc         : Hardware Management (HMC) address
        psystem     : pSystem name (frame name)
        vio         : Virtual I/O name (the same name on HMC)
        dev_id      : The device ID, example: 201

        This function returns:
        used -> The device id is used.
        free -> The device id is free.
    '''

    # Verify the dev type is vscsi or vfc
    if dev_type == 'vscsi':

        cmd_check = ('ssh -l poweradm %s viosvrcmd -m %s -p %s -c '
                     '\"\'lsmap -all\'\"' % (hmc, psystem, vio))

    elif dev_type == 'vfc':

        cmd_check = ('ssh -l poweradm %s viosvrcmd -m %s -p %s -c '
                     '\"\'lsmap -all -npiv\'\"' % (hmc, psystem, vio))

    else:

        print 'Error: the dev_type needs be vscsi or vfc'

    # This a type of cache file per session.
    # All the time the PowerAdm runs a time string is generated in timestr in
    #globalvar.py and the files are created by session.
    # First it checks if exist a file with name frame-vio-device_type-timestr
    #and if not exists ir collected by this function. Else the timestr is the
    #same it doesn't need collect again. It's works well :)
    #
    if os.path.isfile('%s/poweradm/tmp/%s-%s-%s-%s.lst' %
            (config.pahome, psystem, vio, dev_type, globalvar.timestr)):

        check_output = commands.getoutput('cat %s/poweradm/tmp/%s-%s-%s-%s.lst'
                % (config.pahome, psystem, vio, dev_type, globalvar.timestr))

    else:

        check_output = commands.getoutput(cmd_check)
        vscsi_file = open('%s/poweradm/tmp/%s-%s-%s-%s.lst' %
                (config.pahome, psystem, vio, dev_type, globalvar.timestr), 'w')
        vscsi_file.write(check_output + '\n')
        vscsi_file.close()

    # check if exist some virtual device with the ID. If exist returns used,
    #else free.
    dev_status = 'free'
    for l_output in check_output.split('\n'):
        if ('-C1%s ' % dev_id) in l_output:
            dev_status = 'used'
        elif ('-C2%s ' % dev_id) in l_output:
            dev_status = 'used'
        elif ('-C3%s ' % dev_id) in l_output:
            dev_status = 'used'
        elif ('-C4%s ' % dev_id) in l_output:
            dev_status = 'used'

    return dev_status
