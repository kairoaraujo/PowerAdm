#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PowerAdm
newid.py

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

# Imports
###############################################################################
import os.path
import globalvar
import config
import check_devices
import commands


# get a next free id on systems
class NewID:
    """ Find the next LPAR ID free to use. """

    def __init__(self):
        self.newid = None

    def mkid(self, systemp=None):
        """ Find the next LPAR ID """
        systems_keys = list(config.systems.keys())
        systems_length = (len(config.systems.keys()))-1

        count = 0
        if config.vslot_std:
            while count <= systems_length:
                os.system('ssh -l poweradm %s lssyscfg -m %s -r lpar -F '
                          'lpar_id >> %s/poweradm/tmp/ids_%s'
                          % (config.hmcserver, systems_keys[count],
                             config.pahome, globalvar.timestr))
                os.system('cat %s/poweradm/data/reserved_ids >> '
                          '%s/poweradm/tmp/ids_%s'
                          % (config.pahome, config.pahome, globalvar.timestr))
                if os.path.isfile(
                                '%s/poweradm/tmp/reserved_ids_%s'
                                % (config.pahome, globalvar.timestr)):
                    os.system('cat %s/poweradm/tmp/reserved_ids_%s >> '
                              '%s/poweradm/tmp/ids_%s'
                              % (config.pahome, globalvar.timestr,
                                 config.pahome, globalvar.timestr))
                count += 1

            fileids = open('%s/poweradm/tmp/ids_%s'
                           % (config.pahome, globalvar.timestr), 'r')

        else:
            os.system('ssh -l poweradm %s lssyscfg -m %s -r lpar -F lpar_id '
                      '>> %s/poweradm/tmp/ids_%s_%s'
                      % (config.hmcserver, systemp, config.pahome, systemp,
                         globalvar.timestr))
            if os.path.isfile(
                            '%s/poweradm/data/reserved_ids_%s'
                            % (config.pahome, systemp)):
                os.system('cat %s/poweradm/data/reserved_ids_%s >> '
                          '%s/poweradm/tmp/ids_%s_%s'
                          % (config.pahome, systemp, config.pahome, systemp,
                             globalvar.timestr))
            if os.path.isfile(
                            '%s/poweradm/tmp/reserved_ids_%s_%s'
                            % (config.pahome, systemp, globalvar.timestr)):
                os.system(
                    'cat %s/poweradm/tmp/reserved_ids_%s_%s >> '
                    '%s/poweradm/tmp/ids_%s_%s'
                    % (config.pahome, systemp, globalvar.timestr,
                       config.pahome, systemp, globalvar.timestr))

            fileids = open('%s/poweradm/tmp/ids_%s_%s'
                           % (config.pahome, systemp, globalvar.timestr), 'r')

        ids = fileids.readlines()
        ids.sort(key=int)
        lastid = len(ids)-1
        if config.vslot_std:
            psystem_list = config.systems.keys()
        else:
            psystem_list = [systemp]

        # the minimun LPAR ID
        newid = 10

        # checks while new LPAR ID is minor the last LPARD + 1
        while newid <= (int(ids[lastid])+1):
            if str(newid)+"\n" in ids:
                newid += 1
            else:
                # if id < 10 add 0 left, view ticket #5 github
                if newid < 10:
                    newid = ('0%s' % newid)
                system_keys = psystem_list

                # This is a variable to check if check_devics.py verifyied in
                # all VIOS and frames (pSystems)
                count_check = 0

                # uses the check_devices.py to verify if ID is free or used by
                # some virtual device in VIOS
                if config.vslot_std is False:
                    os.system('rm %s/poweradm/tmp/ids_%s_%s'
                              % (config.pahome, systemp, globalvar.timestr))
                    self.newid = newid
                    return self.newid

                else:

                    for psystems in psystem_list:
                        if (
                            check_devices.check('vscsi',
                                                config.hmcserver,
                                                psystems,
                                                config.systems[psystems][0],
                                                '1%s' % newid) == 'used'
                            or
                            check_devices.check('vscsi',
                                                config.hmcserver,
                                                psystems,
                                                config.systems[psystems][1],
                                                '2%s' % newid) == 'used'
                            or
                            check_devices.check('vfc',
                                                config.hmcserver,
                                                psystems,
                                                config.systems[psystems][0],
                                                '3%s' % newid) == 'used'
                            or
                            check_devices.check('vfc',
                                                config.hmcserver,
                                                psystems,
                                                config.systems[psystems][1],
                                                '4%s' % newid) == 'used'):

                            # If the ID is used on a virtual device,
                            # go to next ID.
                            # The variables count back to the 0
                            newid += 1
                            break

                        else:

                            # else, the virtual slot standar is not used,
                            # the ID is not used by any virtual device is
                            # incremented +1 and if is free in all
                            # pSystems/frames and variable count is equal the
                            # number of pSystem/frames it found the next ID!
                            # Remove the tmp files and go ahead.
                            count_check += 1

                            if count_check == len(system_keys):

                                os.system('rm %s/poweradm/tmp/ids_%s'
                                          % (config.pahome, globalvar.timestr))
                                self.newid = newid
                                return self.newid

        return self.newid


class Vadpt:
    """ Get the next available ID for Virtual Slot """

    def __init__(self, vios1, vios2, systemp):
        self.vios1 = vios1
        self.vios2 = vios2
        self.systemp = systemp

    def get_new(self):

        # get the maximum slots avaiable
        list_max_virtul_slots = []
        list_max_virtul_slots.append(int(commands.getoutput(
            "ssh -l poweradm %s lssyscfg -r prof -m %s --filter "
            "\'lpar_names=%s\' -F max_virtual_slots"
            % (config.hmcserver, self.systemp, self.vios1)).split('\n')[0]))

        list_max_virtul_slots.append(int(commands.getoutput(
            "ssh -l poweradm %s lssyscfg -r prof -m %s --filter "
            "\'lpar_names=%s\' -F max_virtual_slots"
            % (config.hmcserver, self.systemp, self.vios2)).split('\n')[0]))

        max_virtual_slots = max(list_max_virtul_slots)

        os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c "
                  "\"\'lsdev -slots\'\" | grep C[0-9] | awk \'{ print $1 }\' "
                  "| awk -F \'-C\' \'{ print $2 }\' > "
                  "%s/poweradm/tmp/vslots_vios_%s_%s" % (
                    config.hmcserver, self.systemp, self.vios1, config.pahome,
                    self.systemp, globalvar.timestr))

        os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c "
                  "\"\'lsdev -slots\'\" | grep C[0-9] | awk \'{ print $1 }\' "
                  "| awk -F \'-C\' \'{ print $2 }\' >> "
                  "%s/poweradm/tmp/vslots_vios_%s_%s"
                  % (config.hmcserver, self.systemp, self.vios2, config.pahome,
                     self.systemp, globalvar.timestr))

        if os.path.isfile('%s/poweradm/tmp/reserved_vslots_%s_%s'
                          % (config.pahome, self.systemp, globalvar.timestr)):
            os.system("cat %s/poweradm/tmp/reserved_vslots_%s_%s >> "
                      "%s/poweradm/tmp/vslots_vios_%s_%s"
                      % (config.pahome, self.systemp, globalvar.timestr,
                         config.pahome, self.systemp, globalvar.timestr))

        if os.path.isfile('%s/poweradm/data/reserved_vslots_%s'
                          % (config.pahome, self.systemp)):
            os.system("cat %s/poweradm/data/reserved_vslots_%s >> "
                      "%s/poweradm/tmp/vslots_vios_%s_%s"
                      % (config.pahome, self.systemp, config.pahome,
                         self.systemp, globalvar.timestr))

        file_used_vdapts = open(
            '%s/poweradm/tmp/vslots_vios_%s_%s' % (config.pahome,
                                                   self.systemp,
                                                   globalvar.timestr), 'r')
        used_vdapts = file_used_vdapts.read().splitlines()
        while 'None' in used_vdapts:
            used_vdapts.remove('None')
        used_vdapts.sort(key=int)
        used_vdapts = map(int, used_vdapts)
        full_vdapts = range(int(max_virtual_slots))

        free_vdapts = list(set(full_vdapts) - set(used_vdapts))

        return free_vdapts
