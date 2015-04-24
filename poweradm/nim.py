#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
nim.py

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
import fnmatch
import globalvar
import config

##############################################################################################
#
# Class NIMServer
##############################################################################################

class NIMServer:
    ''' Get informations about NIM Servers from config.py '''

    def selectNIM(self):
        ''' Select NIM using text mode menu to get informations '''

        print ("\n[Deploy NIM: NIM Server Select]\n"
               "\nSelect the NIM Server")
        nimservers_keys = list(nimservers.keys())
        nimservers_length = (len(nimservers.keys()))-1
        count = 0
        while count <= nimservers_length:
            print ("%s : %s" % (count, nimservers_keys[count]))
            count += 1

        while True:
            try:
		nimserver_option = int(raw_input("NIM Server: "))
        	self.nimserver = (nimservers_keys[nimserver_option])
                break
            except(ValueError,IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (nimservers_length))

        self.address = nimservers[('%s' % nimservers_keys[nimserver_option])][0]
        self.ipdeploy = nimservers[('%s' % nimservers_keys[nimserver_option])][1]
        self.gwdeploy = nimservers[('%s' % nimservers_keys[nimserver_option])][2]
        self.iprange = nimservers[('%s' % nimservers_keys[nimserver_option])][3]
        self.ipstartend = self.iprange.split('-')
        self.ipnet = self.ipstartend[0].split('.')
        self.ipstart = self.ipnet[3]
        self.ipnet = ('%s.%s.%s.' % (self.ipnet[0], self.ipnet[1], self.ipnet[2]))
        self.ipend = self.ipstartend[1]

    def listNIM(self):
        ''' List all NIM Servers name (config) '''

        return list(config.nimservers.keys())


    def getNIM(self, nimserver):
        ''' Get direct NIM Server informations using getNIM()

        Attribute:
        nimserver       NIM Server name. Use listNIM to get all possible names.
        '''

        self.nimserver = nimserver
        self.address = nimservers[nimserver][0]
        self.ipdeploy = nimservers[nimserver][1]
        self.gwdeploy = nimservers[nimserver][2]
        self.iprange = nimservers[nimserver][3]
        self.ipstartend = self.iprange.split('-')
        self.ipnet = self.ipstartend[0].split('.')
        self.ipstart = self.ipnet[3]
        self.ipnet = ('%s.%s.%s.' % (self.ipnet[0], self.ipnet[1], self.ipnet[2]))
        self.ipend = self.ipstartend[1]


    def getNIMServer(self):
        ''' Return NIM Server name from selectNIM() or getNIM('NIM Server name') '''

        return self.nimserver

    def getNIMAddress(self):
        ''' Return NIM Server address/hostname from selectNIM() or getNIM('NIM Server name') '''

        return self.address

    def getNIMIPDeploy(self):
        ''' Return NIM Server IP Deploy from selectNIM() or getNIM('NIM Server name') '''

        return self.ipdeploy

    def getNIMGWDeploy(self):
        ''' Return NIM Server GW Deploy from selectNIM() or getNIM('NIM Server name') '''

        return self.gwdeploy

    def getIPRange(self):
        ''' Return NIM Server IP Range from selectNIM() or getNIM('NIM Server name') '''

        return self.iprange

    def getIPNet(self):
        ''' Return NIM Server IP Network from selectNIM() or getNIM('NIM Server name') '''

        return self.ipnet

    def getIPStart(self):
        ''' Return NIM Server IP Start from selectNIM() or getNIM('NIM Server name') '''

        return self.ipstart

    def getIPEnd(self):
        ''' Return NIM Server IP End from selectNIM() or getNIM('NIM Server name') '''

        return self.ipend

##############################################################################################
#
# Class NIMGetVer
##############################################################################################

class NIMGetVer:
    ''' Get OS version configurations from config '''

    def selectOSVersion(self):
        ''' Select OS version using text mode (menu)'''

        print ("\n[DEPLOY OS Nim Server Configuration]\n"
               "\nSelect the version OS for LPAR")
        nim_os_deploy_keys = list(nim_os_deploy.keys())
        nim_os_deploy_length = (len(nim_os_deploy.keys()))-1
        count = 0
        while count <= nim_os_deploy_length:
            print ("%s : %s" % (count, nim_os_deploy_keys[count]))
            count += 1

        while True:
            try:
	        nim_os_deploy_option = int(raw_input("Version: "))
        	self.osversion = (nim_os_deploy_keys[nim_os_deploy_option])
                break
            except(ValueError,IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (nim_os_deploy_length))
        self.mksysblpp = nim_os_deploy[('%s' % nim_os_deploy_keys[nim_os_deploy_option])][0]
        self.spot = nim_os_deploy[('%s' % nim_os_deploy_keys[nim_os_deploy_option])][1]

    def listOSVersion(self):
        ''' List all OS version names '''

        return list(config.nim_os_deploy.keys())

    def OSVersion(self, osversion):
        ''' Select OS version using OSVersion(osversion).

        Attribute:

        osversion       OS version name from config file. Use listOSVersion to List
                        all OS version name available.
        '''

        self.osversion = osversion
        self.mksysblpp = nim_os_deploy[self.osversion][0]
        self.spot = nim_os_deploy[self.osversion][1]


    def getOSVersion(self):
        ''' Return OS Version from selectOSVersion() or OSVersion('osversion')'''

        return self.osversion

    def getMksysbLpp(self):
        ''' Return MKSYSB or LPP SOURCE (check config) used by OS Version
        from selectOSVersion() or OSVersion('osversion')
        '''

        return self.mksysblpp

    def getSpot(self):
        '''Return SPOT used by OS Version from selectOSVersion() or OSVersion('osversion')'''

        return self.spot

##############################################################################################
#
# Class FindNIMFile
##############################################################################################

class NIMFileFind:
    ''' Find availables LPAR configs to deploy '''

    def selectDeploy(self, title, filedir, action):
        '''
        Text mode (menu) select file/LPAR to deploy

        Attributes:
        title       An title to menu.
        filedir     Directory to search a nim files (*.nim). By default:
                      - config.pahome'/poweradm/nim/ : files to make deploy
                      - 'config.pahome'/poweradm/nim_executed/ : files to remove deploy conf
        action      The action subtitle like a REMOVE, DEPLOY, FOOBAR.
        '''

        print ("\n[DEPLOY OS NIM: %s]\n"
               "\nSelect the Deploy:\n" % (title))
        listDeploys = fnmatch.filter(os.listdir("%s" % (filedir)), "*.nim")
        listDeploys_length = len(listDeploys)-1
        if listDeploys_length == -1:
            print ('\033[1;31mNo Deploys found.\033[1;00m\n\n'
                   '- No LPAR was configured to perform deploy.\n'
                   '- The LPAR has not yet been created.\n'
                   '\nExiting\n')
            exit()
        count = 0
        while count <= listDeploys_length:
            print ("%s : %s" % (count, listDeploys[count]))
            count += 1

        while True:
            try:
                deploy_option = int(raw_input("\nWhat's OS Deploy NIM you want %s?: " % (action)))
                self.deploy_file = (listDeploys[deploy_option])
                break
            except(ValueError,IndexError):
                print('\tERROR: Select an existing option between 0 and %s.' % (listDeploys_length))

    def listDeploy(self):
        ''' List available deploys files/LPAR to deploy'''

        filedir = ('%s/poweradm/nim/' % (config.pahome))
        listDeploy = fnmatch.filter(os.listdir("%s" % (filedir)), "*.nim")
        return listDeploy

    def getDeploy(self):
        ''' Return selected deploy in selectDeploy() '''

        return self.deploy_file

    def fileData(self, deploy_file):
        '''
        Get all Deploy file data

        Attribute:
        deploy_file     The full path and file. By default:
                          - 'config.pahome'/poweradm/nim/ : files to make deploy
                          - 'config.pahome'/poweradm/nim_executed/ : files to remove deploy conf

        To list file use listDeploy()
        To select file using text mode (menu) use selectDeploy()

        Use these functions to get return:

        returnDeployPrefix()        return LPAR Prefix
        returnDeployLPARName()      return LPAR Name
        returnDeployFrame()         return LPAR Frame hosted
        returnDeployVLANFinal()     return LPAR Final VLAN Configuration
        returnDeployIP()            return LPAR Deploy IP   (only remove config)
        returnDeployNIMServer()     return LPAR NIM Server  (only remove config)
        returnDeployNIMAddress()    return LPAR NIM Address (only remove config)

        '''

        f_nim_deploy = open(deploy_file, 'r')
        for line in f_nim_deploy.readlines():
            if line.startswith('#PREFIX'):
                lpar = line.split()
                self.lparprefix = lpar[1]
            if line.startswith('#LPARNAME'):
                lpar = line.split()
                self.lparname = lpar[1]
            if line.startswith('#FRAME'):
                lpar = line.split()
                self.lparframe = lpar[1]
            if line.startswith('#VLAN_FINAL'):
                lpar = line.split()
                self.lparvlans = lpar[1]
            if line.startswith('#IP'):
                lpar = line.split()
                self.lparip = lpar[1]
            if line.startswith('#NIMSERVER'):
                lpar = line.split()
                self.lparnim = lpar[1]
            if line.startswith('#NIMADDRESS'):
                lpar = line.split()
                self.lparnimaddress = lpar[1]

        f_nim_deploy.close()

    def returnDeployPrefix(self):
        ''' Return LPAR Prefix '''

        return self.lparprefix

    def returnDeployLPARName(self):
        ''' Return LPAR Name '''

        return self.lparname

    def returnDeployFrame(self):
        ''' Return LPAR Frame hosted  '''

        return self.lparframe

    def returnDeployVLANFinal(self):
        ''' Return LPAR VLAN Final configuration '''

        return self.lparvlans

    def returnDeployIP(self):
        ''' Return LPAR IP used (only remove config) '''

        return self.lparip

    def returnDeployNIMServer(self):
        ''' Return LPAR NIM Server used (only remove config)  '''

        return self.lparnim

    def returnDeployNIMAddress(self):
        ''' Return LPAR used NIM Address (only remove config) '''

        return self.lparnimaddress

##############################################################################################
#
# NIMNewIP Class
##############################################################################################

class NIMNewIP():
    ''' Get next free IP address to use with on NIM client '''

    def getNewIP(self, nim_address, nim_ipstart, nim_ipend, nim_ipnet):
        ''' Returns next free IP. See classes NIMServer and NIMFindFile

        Attributes:

        nim_address     NIM Server address. See poweradm.nimserver
        nim_ipstart     NIM IP Start. See poweradm.nimserver
        nim_ipend       NIM IP End. See poweradm.nimserver
        nim_ipnet       NIM IP Network. See poweradm.nimserver
        '''

        # find next IP on the range
        os.system("ssh -l poweradm %s cat /etc/hosts >> %s/poweradm/tmp/hosts_%s" %
                 (nim_address, config.pahome, config.timestr))
        os.system("cat %s/poweradm/data/reserved_ips >> %s/poweradm/tmp/hosts_%s" %
                 (config.pahome, config.pahome, config.timestr))

        # verify ip (get IP and find in unique host file create before)
        def verifyIP(ipaddress):
            ''' Verify IPs '''
            f_nim_hosts = open("%s/poweradm/tmp/hosts_%s" % (config.pahome, config.timestr), 'r')
            for line_hosts in f_nim_hosts.readlines():
                if line_hosts.startswith('%s' % (ipaddress)):
                    f_nim_hosts.close()
                    return True
            f_nim_hosts.close()
            return False

        # make loop find next free IP
        ip_start = int(nim_ipstart)
        ip_end = int(nim_ipend)
        while ip_start <= ip_end:
            if verifyIP('%s%s' % (nim_ipnet, ip_start)):
                ip_start +=1
            else:
                new_ip = ('%s%s' % (nim_ipnet, ip_start))
                return new_ip
                break
