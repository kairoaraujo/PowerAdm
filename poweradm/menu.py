#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PowerAdm
menu.py

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
import config
import globalvar
import createlparconf
import findchange
import execchange
import nimmain
import nimclear
import tbmain
import os
import verify
import getpass


def main_poweradm():
    """ Main text menu of PowerAdm. """

    os.system('clear')
    print("\n\n"
          "[ Power Adm ]\n"
          "[ Version: %s - © 2014-2016 Kairo Araujo - BSD License ]\n"
          % globalvar.version)

    poweradm = raw_input("\nPower Adm options\n"
                         "1. LPAR configuration.\n"
                         "2. Execute the LPAR creation.\n"
                         "3. Deploy OS on an existing LPAR.\n"
                         "4. Clear NIM OS deploy configs.\n"
                         "5. Troubleshooting.\n"
                         "6. Quit.\n\n"
                         "Use Ctrl+C to left without save\n\n"
                         "Please choose an option: ")

    if poweradm == '1':
        """ LPAR configuration. """
        lock_file = '%s/poweradm/data/lock' % config.pahome
        if os.path.isfile(lock_file):
            print('\nA LPAR configuration process is running.')
            print('The %s was created by:' % lock_file)
            with open(lock_file, 'r') as l_f:
                print(l_f.read())
            exit()

        else:
            l_f = open(lock_file, 'w')
            l_f.write(getpass.getuser())
            l_f.close()
            try:
                createlparconf.exec_createlparconf()
            except KeyboardInterrupt:
                os.system('rm %s' % lock_file)
                print("\n\nCtrl+C pressed! Exiting without save.\n")

    elif poweradm == '2':
        """ Execute the LPAR creation."""

        # Find the File Change/Ticket using class FindChange()
        exec_findlpar = findchange.FindChange()
        exec_findlpar.selectChange()
        check_exec_findlpar = verify.CheckOK(
            '\nDo you want execute change/ticket %s? (y/n): '
            % (exec_findlpar.getChange()), 'n')
        check_exec_findlpar.mkCheck()
        if check_exec_findlpar.answerCheck() == 'y':
            exec_change = execchange.Exe(
                '%s/poweradm/changes/%s'
                % (config.pahome, exec_findlpar.getChange()))
            exec_change.runChange()
        else:
            print('Aborting change/ticket %s...\nExiting!'
                  % (exec_findlpar.getChange()))
            exit()

    elif poweradm == '3':
        """ Deploy OS on an existing LPAR. """

        nimmain.main()

    elif poweradm == '4':
        """ Clear NIM OS deploy configs. """

        nimclear.clear()

    elif poweradm == '5':

        tbmain.main()

    elif poweradm == '6':
        print("6. Quit")
        print("Quiting...")
        exit()

    else:
        print("Invalid option. Quiting")
        exit()


