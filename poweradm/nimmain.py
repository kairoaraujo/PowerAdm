#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
# nimmain.py
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
# Imports
###############################################################################################
import time
import os
from globalvar import *
from verify import *
from nimfilefind import *
from getnimver import *
from nimserver import *
##############################################################################################

def nimmain():

    # select a machine to deploy
    newdeploy = NIMFileFind('Select Deploy', 'poweradm/nim/', 'execute')
    newdeploy.selectDeploy()


    # select version to install
    selectnimver = GetNimVer()
    selectnimver.selectOsVersion()


    # select nim to use
    newnim = NimServer()
    newnim.selectNim()

    # find next IP on the range
    os.system("ssh -l poweradm %s cat /etc/hosts >> poweradm/tmp/hosts_%s" %
            (newnim.getNimAddress(), timestr))
    os.system("cat poweradm/data/reserved_ips >> poweradm/tmp/hosts_%s" % (timestr))
    def verifyIP(ipaddress):
        f_nim_hosts = open("poweradm/tmp/hosts_%s" % (timestr), 'r')
        for line_hosts in f_nim_hosts.readlines():
            if line_hosts.startswith('%s' % (ipaddress)):
                f_nim_hosts.close()
                return True
        f_nim_hosts.close()
        return False

    ip_start = int(newnim.getIPStart())
    ip_end = int(newnim.getIPEnd())
    while ip_start <= ip_end:
        if verifyIP('%s%s' % (newnim.getIPNet(), ip_start)):
            ip_start +=1
        else:
            new_ip = ('%s%s' % (newnim.getIPNet(), ip_start))
            break

    # get prefix and lpar name
    f_nim_deploy = open("poweradm/nim/%s" % (newdeploy.getDeploy()), 'r')

    for line in f_nim_deploy.readlines():
        if line.startswith('#PREFIX'):
            lpar = line.split()
            lparprefix = lpar[1]
        if line.startswith('#LPARNAME'):
            lpar = line.split()
            lparname = lpar[1]
        if line.startswith('#FRAME'):
            lpar = line.split()
            lparframe = lpar[1]
    f_nim_deploy.close()

    # verify the config
    print ('\n[Deploy SO NIM: Check deploy]\n')
    print ('*' * 80)
    print ('Server: %s-%s (IP Client: %s)\n'
           'NIM Server: %s (IP Server: %s)\n'
           'OS Version: %s' % (lparprefix, lparname, new_ip, newnim.getNimServer(),
               newnim.getNimIPDeploy(), selectnimver.getOsVersion()))
    print ('*' * 80)

    deploy = CheckOK('\nProceed to Deploy?(y/n): ', 'n')
    deploy.mkCheck()

    if deploy.answerCheck() == 'y':

        f_nim_exe = open('poweradm/changes/deploy_nim_%s-%s.nim' % (lparprefix, lparname), 'w')

        def f_nimexe_chksh():
            f_nim_exe.write("\nif [ $? != 0 ];"
                            "then\n"
                            "\techo 'An error has occurred. Check the actions taken.'; \n"
                            "\texit;\n"
                            "else\n"
                            "\techo 'Command OK. Continuing';\n"
                            "fi\n")

        f_nim_exe.write('\n\necho "Adding host %s-%s on NIM Server /etc/hosts"\n' % (lparprefix, lparname))

        f_nim_exe.write('\n\nssh -l poweradm %s sudo hostent -a %s -h %s' % (newnim.getNimAddress(),
            new_ip, lparname))
        f_nimexe_chksh()

        f_nim_exe.write('\n\necho "Creating machine %s-%s on NIM Server"\n' % (lparprefix, lparname))

        f_nim_exe.write('\n\nssh -l poweradm %s sudo nim -o define -t standalone -a platform=chrp '
                '-a netboot_kernel=mp -a if1=\\"$(ssh -l poweradm %s sudo lsnim -t ent | awk \'{ print $1 }\' '
                '| head  -1) %s 0\\" -a cable_type1=tp %s\n' % (newnim.getNimAddress(), newnim.getNimAddress(),
                    lparname, lparname))
        f_nimexe_chksh()

        f_nim_exe.write('\n\necho "Resource alocations and perform operations to %s-%s on NIM Server"\n' %
                (lparprefix, lparname))

        if nim_deploy_mode.lower() == 'mksysb':

            f_nim_exe.write('\n\nssh -l poweradm %s sudo nim -o bos_inst -a source=mksysb -a spot=%s '
                '-a mksysb=%s -a no_client_boot=yes -a accept_licenses=yes %s\n' % (newnim.getNimAddress(),
                    selectnimver.getSpot(), selectnimver.getMksysbLpp(), lparname))

            f_nimexe_chksh()

        elif nim_deploy_mode.lower() == 'lpp':

            f_nim_exe.write('\n\nssh -l poweradm %s sudo nim -o bos_inst -a source=spot -a spot=%s '
                '-a lpp_source=%s -a no_client_boot=yes -a accept_licenses=yes %s\n' %
                (newnim.getNimAddress(), selectnimver.getSpot(), selectnimver.getMksysbLpp(), lparname))
            f_nimexe_chksh()

        f_nim_exe.write('\n\necho "Getting the Mac Address from %s-%s"\n' % (lparprefix, lparname))
        f_nim_exe.write('echo "This might take a few minutes..."\n')

        f_nim_exe.write('\n\nmac_address=$(ssh -l poweradm %s lpar_netboot -M -A -n -T off -t '
                        'ent %s-%s %s %s | grep C10-T1 | awk \'{ print $3 }\')\n' % (hmcserver, lparprefix,
			            lparname, lparname, lparframe))
        f_nimexe_chksh()

        f_nim_exe.write('\n\necho "Booting LPAR %s-%s on NIM Server"\n' % (lparprefix, lparname))
        f_nim_exe.write('echo "This might take a few minutes..."\n')
        f_nim_exe.write('\n\nssh -l poweradm %s lpar_netboot -m $mac_address -T off -t ent -s '
                'auto -d auto -S %s -C %s %s-%s %s %s\n' % (hmcserver, newnim.getNimIPDeploy(), new_ip,
                    lparprefix, lparname, lparname, lparframe))
        f_nimexe_chksh()

        f_nim_exe.close()

        print ('\n\nInitializing deploy OS...')

        f_nim_reserved_ips = open ('poweradm/data/reserved_ips', 'a')
        f_nim_reserved_ips.write('%s\n' % (new_ip))
        f_nim_reserved_ips.close()
        f_nim_deploy = open("poweradm/nim/%s" % (newdeploy.getDeploy()), 'a')
        f_nim_deploy.write('#IP %s\n' % (new_ip))
        f_nim_deploy.write('#NIMSERVER %s\n' % (newnim.getNimServer()))
        f_nim_deploy.write('#NIMADDRESS %s\n' % (newnim.getNimAddress()))
        f_nim_deploy.close()

        os.system('sh poweradm/changes/deploy_nim_%s-%s.nim' % (lparprefix, lparname))
        os.system('mv poweradm/nim/%s-%s.nim poweradm/nim_executed/' % (lparprefix, lparname))
        os.system('mv poweradm/changes/deploy_nim_%s-%s.nim poweradm/changes_executed/' % (lparprefix, lparname))

        print ('\nPlease, access HMC %s and run command below to finis OS install. '
               '\n\t\'mkvterm -m %s -p %s-%s\' ' % (hmcserver, lparframe, lparprefix, lparname))

        access_hmc = CheckOK('\nDo you want access HMC on this session?(y/n): ', 'n')
        access_hmc.mkCheck()
        if access_hmc.answerCheck() == 'y':

            print ('\n\n\trun command \'mkvterm -m %s -p %s-%s\'\n\n' % (lparframe, lparprefix, lparname))
            print ('\n\n\tTip: maybe you need press \'1 Enter\'\n\n')
            os.system('ssh -l poweradm %s' % (hmcserver))
        else:
            print ('\nExiting...\n\n')
            exit

    else:

        print ('\nAborting.\n\n')
        exit

