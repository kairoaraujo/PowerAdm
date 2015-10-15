#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Power Adm
 nimmain.py

 Copyright (c) 2014 Kairo Araujo

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

 Important:
 IBM, PowerVM (a.k.a. vios) are registered trademarks of IBM Corporation in
 the United States, other countries, or both.
"""

# Imports
###############################################################################################
import os
import config
import verify
import nim
import mkosdeploy
import commands
##############################################################################################

def main():
    """ NIM main file to PowerAdm text mode (menu) """

    # select a machine to deploy
    #
    nimfile = nim.NIMFileFind()
    nimfile.selectDeploy('Select Deploy', 'poweradm/nim/', 'EXECUTE')
    nim_file = ('%s/poweradm/nim/%s' % (config.pahome, nimfile.getDeploy()))
    nimfile.fileData(nim_file)
    # get variables
    lparprefix = nimfile.returnDeployPrefix()
    lparname = nimfile.returnDeployLPARName()
    lparframe = nimfile.returnDeployFrame()
    lparvlans = nimfile.returnDeployVLANFinal()

    # select version to install
    #
    nimcfg = nim.NIMGetVer()
    nimcfg.selectOSVersion()
    nim_cfg_ver = nimcfg.getOSVersion()
    nim_cfg_spot = nimcfg.getSpot()
    nim_cfg_mksysbspot = nimcfg.getMksysbLpp()

    # select nim and get variables
    #
    nimvars = nim.NIMServer()
    nimvars.selectNIM()
    nim_address = nimvars.getNIMAddress()
    nim_ipstart = nimvars.getIPStart()
    nim_ipend = nimvars.getIPEnd()
    nim_ipnet = nimvars.getIPNet()
    nim_server = nimvars.getNIMServer()
    nim_ipdeploy = nimvars.getNIMIPDeploy()

    # verify the config
    print ('\n[DEPLOY SO NIM: Check deploy]\n')
    print ('*' * 80)
    print ('Server: %s-%s\n'
           'NIM Server: %s (IP Server: %s)\n'
           'OS Version: %s' % (lparprefix, lparname, nim_server, nim_ipdeploy, nim_cfg_ver))
    print ('*' * 80)

    # try nim connections
    print ('\n\nTesting the NIM Server connections!')
    chk_nim_connections = commands.getstatusoutput('ssh -l poweradm %s sudo lsnim' % nim_server)
    if chk_nim_connections[0] != 0:
        print ('\nConnect to NIM Server failed!')
        exit("\tError: "+chk_nim_connections[1])
    else:
        print ('\nNIM Server connection passed!\n')

    deploy = verify.CheckOK('\nProceed to Deploy?(y/n): ', 'n')
    deploy.mkCheck()
    deploy = deploy.answerCheck()

    if deploy == 'y':
        mkdeploy = mkosdeploy.MakeNIMDeploy(lparprefix, lparname, lparframe,
                lparvlans, nim_file, nim_cfg_ver, nim_cfg_spot,
                nim_cfg_mksysbspot, nim_address, nim_ipstart, nim_ipend, nim_ipnet,
                nim_server, nim_ipdeploy, deploy)
        mkdeploy.createNIMDeploy()

        access_hmc = verify.CheckOK('\nDo you want access HMC on this session?(y/n): ', 'n')
        access_hmc.mkCheck()

        if access_hmc.answerCheck() == 'y':

            print ('\n\n\trun command \'mkvterm -m %s -p %s-%s\'\n\n' % (lparframe, lparprefix, lparname))
            print ('\n\n\tTip: maybe you need press \'1 Enter\'\n\n')
            os.system('ssh -l poweradm %s' % (config.hmcserver))

        else:
            print ('\nExiting...\n\n')
            exit

    else:
        print ('\nExiting...\n\n')
        exit


