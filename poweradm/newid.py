#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
newid.py

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
import os.path
import globalvar
import config
import check_devices

# get a next free id on systems
class NewID:
    ''' Find the next LPAR ID free to use. For more informations access http://poweradm.org '''

    def mkID(self):
        ''' Find the next LPAR ID '''

        ids = []
        systems_keys = list(config.systems.keys())
        systems_length = (len(config.systems.keys()))-1
        count = 0
        while count <= systems_length:
            os.system('ssh -l poweradm %s lssyscfg -m %s -r lpar -F lpar_id >> %s/poweradm/tmp/ids_%s'
                      % (config.hmcserver, systems_keys[count], config.pahome, globalvar.timestr))
            os.system('cat %s/poweradm/data/reserved_ids >> %s/poweradm/tmp/ids_%s' %
                    (config.pahome, config.pahome, globalvar.timestr))
            if os.path.isfile('%s/poweradm/tmp/reserved_ids_%s' % (config.pahome, globalvar.timestr)):
                os.system('cat %s/poweradm/tmp/reserved_ids_%s >> %s/poweradm/tmp/ids_%s' % (config.pahome,
                          globalvar.timestr, config.pahome, globalvar.timestr))
            count += 1
        fileids = open('%s/poweradm/tmp/ids_%s' % (config.pahome, globalvar.timestr), 'r')
        ids = fileids.readlines()
        ids.sort(key=int)
        lastid = len(ids)-1

        # the minimun LPAR ID
        newid = 10

        # checks while new LPAR ID is minor the last LPARD + 1
        while newid <= (int(ids[lastid])+1):
            if str(newid)+"\n" in ids:
                newid += 1
            else:
                # if id < 10 add 0 left, view ticket #5 github
                if newid < 10:
                    newid = ('0%s' % (newid))
                system_keys = config.systems.keys()

                # This is a variable to check if check_devics.py verifyied in
                #all VIOS and frames (pSystems)
                count_check = 0

                # uses the check_devices.py to verify if ID is free or used by
                #some virtual device in VIOS
                for psystems in config.systems.keys():

                    if (
                        check_devices.check('vscsi', config.hmcserver,
                        psystems, config.systems[psystems][0], newid) == 'used'
                        or
                        check_devices.check('vscsi', config.hmcserver,
                        psystems, config.systems[psystems][0], newid) == 'used'
                        or
                        check_devices.check('vfc', config.hmcserver,
                        psystems, config.systems[psystems][0], newid) == 'used'
                        or
                        check_devices.check('vfc', config.hmcserver,
                        psystems, config.systems[psystems][0], newid) == 'used'
                        ):

                        # If the ID is used on a virtual device, go to next ID.
                        # The variables count back to the 0
                        newid += 1
                        count_check = 0
                        break

                    else:

                        # else, the ID is not used by any virtual device is
                        #incremented +1 and if is free in all pSystems/frames
                        #and variable count is equal the number of pSystem/
                        #frames it found the next ID! Remove the tmp files and
                        #go ahead.
                        count_check +=1

                        if count_check == len(system_keys):

                            os.system('rm %s/poweradm/tmp/ids_%s' % (config.pahome, globalvar.timestr))
                            self.newid = newid
                            return self.newid
