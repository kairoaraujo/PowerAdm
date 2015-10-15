#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
mkosdeploy.py

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
import os
import nim
import config
import commands
##############################################################################################

class MakeNIMDeploy():
    """ Make Operation System NIM Deploy
        Attributes:

        lparprefix              LPAR Prefix - from nim see NIMFileFind()
        lparname                LPAR Name - from nim see NIMFileFind()
        lparframe               LPAR Frame - from nim seeNIMFileFind()
        lparvlans               LPAR VLAN Final configuration - from nim see NIMFileFind()
        nim_cfg_ver             NIM Config OS Version - from nim see NIMGetVer()
        nim_cfg_spot            NIM Config SPOT - from nim see NIMGetVer()
        nim_cfg_mksysbspot      NIM Config MKSYSB or SPOT - from nim see NIMGetVer()
        new_ip                  New IP used by LPAR client - from nim see NIMNewIP()
        nim_address             NIM Server IP Address/hostname - from nim see NIMServer()
        nim_ipstart             NIM start IP of range - from nim see NIMServer()
        nim_ipend               NIM end IP of range - from nim see NIMServer()
        nim_ipnet               NIM Network of range - from nim see NIMServer()
        nim_server              NIM Server Name - from nim see NIMServer()
        nim_ipdeploy            NIM Server IP of nim net - from nim see NIMServer()
        deploy                  Deploy action (yes / no )
    """

    def __init__(self, lparprefix, lparname, lparframe, lparvlans, nim_file, nim_cfg_ver,
                 nim_cfg_spot, nim_cfg_mksysbspot, nim_address, nim_ipstart,
                 nim_ipend, nim_ipnet, nim_server, nim_ipdeploy, deploy):

        self.lparprefix = lparprefix
        self.lparname = lparname
        self.lparframe = lparframe
        self.lparvlans = lparvlans
        self.nim_file = nim_file
        self.nim_cfg_ver = nim_cfg_ver
        self.nim_cfg_spot = nim_cfg_spot
        self.nim_cfg_mksysbspot = nim_cfg_mksysbspot
        self.nim_address = nim_address
        self.nim_ipstart = nim_ipstart
        self.nim_ipend = nim_ipend
        self.nim_ipnet = nim_ipnet
        self.nim_server = nim_server
        self.nim_ipdeploy = nim_ipdeploy
        self.deploy = deploy


    def createNIMDeploy(self):
        """ Do OS NIM Deploy """

        if self.deploy == 'y':

            # find next IP on the range
            #
            new_ip = nim.NIMNewIP()
            new_ip = new_ip.getNewIP(self.nim_address, self.nim_ipstart, self.nim_ipend, self.nim_ipnet)
            self.new_ip = new_ip
            f_nim_reserved_ips = open ('%s/poweradm/data/reserved_ips' % (config.pahome), 'a')
            f_nim_reserved_ips.write('%s\n' % (self.new_ip))
            f_nim_reserved_ips.close()

            f_nim_exe = open('%s/poweradm/changes/deploy_nim_%s-%s.nim' % (config.pahome, self.lparprefix,
                         self.lparname), 'w')

            def f_nimexe_chksh():
                f_nim_exe.write("\nif [ $? != 0 ];"
                                "then\n"
                                "\techo 'An error has occurred. Check the actions taken.'; \n"
                                "\texit;\n"
                                "else\n"
                                "\techo 'Command OK. Continuing';\n"
                                "fi\n")

            f_nim_exe.write('#!/bin/sh\n')

            f_nim_exe.write('\n\necho "Adding host %s-%s on NIM Server /etc/hosts"\n' % (self.lparprefix,
                        self.lparname))

            f_nim_exe.write('\n\nssh -l poweradm %s sudo hostent -a %s -h %s' % (self.nim_address,
                        self.new_ip, self.lparname))
            f_nimexe_chksh()

            f_nim_exe.write('\n\necho "Creating machine %s-%s on NIM Server"\n' % (self.lparprefix,
                            self.lparname))

            f_nim_exe.write('\n\nssh -l poweradm %s sudo nim -o define -t standalone -a platform=chrp '
                    '-a netboot_kernel=mp -a if1=\\"$(ssh -l poweradm %s sudo lsnim -t ent | awk \'{ print $1 }\' '
                    '| head  -1) %s 0\\" -a cable_type1=tp %s\n' % (self.nim_address, self.nim_address,
                        self.lparname, self.lparname))
            f_nimexe_chksh()

            f_nim_exe.write('\n\necho "Resource alocations and perform operations to %s-%s on NIM Server"\n' %
                    (self.lparprefix, self.lparname))

            if config.nim_deploy_mode.lower() == 'mksysb':

                f_nim_exe.write('\n\nssh -l poweradm %s sudo nim -o bos_inst -a source=mksysb -a spot=%s '
                    '-a mksysb=%s -a no_client_boot=yes -a accept_licenses=yes %s\n' % (self.nim_address,
                        self.nim_cfg_spot, self.nim_cfg_mksysbspot, self.lparname))

                f_nimexe_chksh()

            elif nim_deploy_mode.lower() == 'lpp':

                f_nim_exe.write('\n\nssh -l poweradm %s sudo nim -o bos_inst -a source=spot -a spot=%s '
                    '-a lpp_source=%s -a no_client_boot=yes -a accept_licenses=yes %s\n' %
                    (self.nim_address, self.nim_cfg_spot, self.nim_cfg_mksysbspot, self.lparname))
                f_nimexe_chksh()

            f_nim_exe.write('\n\necho "Getting the Mac Address from %s-%s"\n' % (self.lparprefix, self.lparname))
            f_nim_exe.write('echo "This might take a few minutes..."\n')

            f_nim_exe.write('\n\nmac_address=$(ssh -l poweradm %s lpar_netboot -M -A -n -T off -t '
                            'ent %s-%s %s %s | grep C10-T1 | awk \'{ print $3 }\')\n' % (config.hmcserver,
                                self.lparprefix, self.lparname, self.lparname, self.lparframe))
            f_nimexe_chksh()

            f_nim_exe.write('\n\necho "Booting LPAR %s-%s on NIM Server"\n' % (self.lparprefix, self.lparname))
            f_nim_exe.write('echo "This might take a few minutes..."\n')
            f_nim_exe.write('\n\nssh -l poweradm %s lpar_netboot -m $mac_address -T off -t ent -s '
                    'auto -d auto -S %s -C %s %s-%s %s %s\n' % (config.hmcserver, self.nim_ipdeploy, self.new_ip,
                        self.lparprefix, self.lparname, self.lparname, self.lparframe))
            f_nimexe_chksh()

            print ('\n\nChange VLAN on profile to final config')
            f_nim_exe.write('\n\nssh -l poweradm %s chsyscfg -r prof -m %s -i \'lpar_name=%s-%s, name=%s, '
                            '\\\"virtual_eth_adapters=%s\\\"\'' % (config.hmcserver, self.lparframe, self.lparprefix,
                                self.lparname, self.lparname, self.lparvlans))

            f_nim_exe.close()

            print ('\n\nInitializing deploy OS...')

            f_nim_deploy = open(self.nim_file, 'a')
            f_nim_deploy.write('#IP %s\n' % (self.new_ip))
            f_nim_deploy.write('#NIMSERVER %s\n' % (self.nim_server))
            f_nim_deploy.write('#NIMADDRESS %s\n' % (self.nim_address))
            f_nim_deploy.close()

            deploy_output = commands.getoutput('sh %s/poweradm/changes/deploy_nim_%s-%s.nim' %
                    (config.pahome, self.lparprefix, self.lparname))
            print deploy_output

            os.system('mv %s/poweradm/nim/%s-%s.nim %s/poweradm/nim_executed/' % (config.pahome, self.lparprefix,
                self.lparname, config.pahome))
            os.system('mv %s/poweradm/changes/deploy_nim_%s-%s.nim %s/poweradm/changes_executed/' % (config.pahome,
                self.lparprefix, self.lparname, config.pahome))

            print ('\nPlease, access HMC %s and run command below to finish OS install. '
                   '\n\t\'mkvterm -m %s -p %s-%s\' ' % (config.hmcserver, self.lparframe, self.lparprefix, self.lparname))

            return deploy_output
