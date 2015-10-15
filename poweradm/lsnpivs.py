#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
PowerAdm
lsnpivs.py

Copyright (c) 2015 Kairo Araujo

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
import commands
##############################################################################################

def run(hmcserver, system, vios, fc):
    ''' Run NPIV check on VIOS.

        Args:
          hmcserver (str): HMC Address or hostname.
          system (str): exactly system name of Power System.
          VIOS (str): exactly name of VIOS LPAR.
          fc (str): 'all' for all FCs or specific FC (sample: fcs0).
    '''
    if fc == 'all':
        os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c "'lsnports'" | grep fcs > /tmp/%s.%s.lsnports" % (hmcserver, system, vios, system, vios))
        os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c "'errlog'" | grep fcs > /tmp/%s.%s.fcs.errlog" % (hmcserver, system, vios, system, vios))
    else:
        os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c "'lsnports'" | grep '%s ' > /tmp/%s.%s.lsnports" % (hmcserver, system, vios, fc, system, vios))
        os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c "'errlog'" | grep '%s ' > /tmp/%s.%s.fcs.errlog" % (hmcserver, system, vios, fc, system, vios))


    with open('/tmp/%s.%s.lsnports' % (system, vios)) as lsnports:
        for line in lsnports:
            line.replace('\n', '')
            column=line.split()
            info_npiv = ''
            info_use = ''

            # get number of clients
            num_client = (64-int(column[4]))
            # clintes IDs
            os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsmap -all -npiv -field ClntID \"FC name\" -fmt :\'\" |"
                      " grep %s > /tmp/%s.%s.lsparids.%s"
                      % (hmcserver, system, vios, column[0], system, vios, column[0]))

	        # get last five FC erros
            last_errlog = commands.getoutput("cat /tmp/%s.%s.fcs.errlog | grep %s | head -n 5" % (system, vios, column[0]))

            # get link status
            fscsi = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsdev -dev %s -child\'\" | grep fscsi | awk \'{ print $1 }\'" %
                    (hmcserver, system, vios, column[0]))
            fc_link = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'lsdev -dev %s -attr attach\'\" | grep -E \'^al|^switch\'" %
                    (hmcserver, system, vios, fscsi))
            fc_stat = commands.getoutput("ssh -l poweradm %s viosvrcmd -m %s "
            "-p %s -c \"\'fcstat -e %s\'\" | grep \"Attention Type:\" "
            "| awk -F: \'{ print $2 }\'" % (hmcserver, system, vios, column[0]))

            # get other fc informations
            os.system("ssh -l poweradm %s viosvrcmd -m %s -p %s -c \"\'fcstat %s\'\" > /tmp/%s.%s.fcstat.%s" %
                    (hmcserver, system, vios, column[0], system, vios, column[0]))

            with open('/tmp/%s.%s.fcstat.%s' % (system, vios, column[0])) as fcstat:
                for l_fcstat in fcstat:
                    if "Port Speed (supported)" in l_fcstat:
                        speed_port = l_fcstat.replace('\n', '')
                        speed_port = speed_port.split()

                    if "Port Speed (running):" in l_fcstat:
                        speed_running = l_fcstat.replace('\n', '')
                        speed_running = speed_running.split()

                    if "World Wide Port Name" in l_fcstat:
                        wwpn = l_fcstat.replace('\n', '')

            lpar_id_list = []
            with open('/tmp/%s.%s.lsparids.%s' % (system, vios, column[0])) as lparidslist:
                for l_lparidslist in lparidslist:
                    lparid_split = l_lparidslist.split(':')
                    lpar_id_list.append('%s(%s)' % (lparid_split[0], lparid_split[1]))

            if column[2] in ('0') and column[4] in ('64'):
                column[0] = ("\033[1;33m%s\033[1;00m" % column[0])
                column[2] = ("\033[1;33m%s\033[1;00m" % column[2])
                info_npiv = info_npiv.join("\033[1;33m`-\033[1;00m don't enabled to NPIV but don't has connections configured!")

            elif column[2] in ('0') and column[4] != ('64'):
                column[0] = ("\033[1;31m%s\033[1;00m" % column[0])
                column[2] = ("\033[1;31m%s\033[1;00m" % column[2])
                info_npiv = info_npiv.join("\033[1;31m`-\033[1;00m don't enabled to NPIV and has connections configured!")

            if  column[4] in ('7','8','9','10','11','12'):
                column[0] = ("\033[1;33m%s\033[1;00m" % column[0])
                column[4] = ("\033[1;33m%s\033[1;00m" % column[4])
                info_use = info_use.join("\033[1;33m`-\033[1;00m between 10% and 20% free for new connections")

            elif column[4] in ('0','1','2','3','4','5','6'):
                column[0] = ("\033[1;31m%s\033[1;00m" % column[0])
                column[4] = ("\033[1;31m%s\033[1;00m" % column[4])
                info_use = info_use.join("\033[1;31m`-\033[1;00m between 0% and 10% free for new connections")

            print "=" * 80
            print ("NAME\tPHYSLOC\t\t\t\tFABRIC\tTPORTS\tAPORTS\tSWWPNS\tAWWPNS")
            print "=" * 80

            print '\t'.join(column)

            if info_npiv != '':
                print info_npiv

            if info_use != '':
                print info_use

            print ("\nUse of NPIV")
            print ("--- -- ----")
            print ("Number of clients using this port: %s" % num_client)

            if len(lpar_id_list) > 0:
                print ("LPAR clients ID(vfchost): %s" % ', '.join(lpar_id_list))
            else:
                print ("LPAR clients ID(vfchost): none")

            print "\nAdapter Status"
            print "------- ------"
            if fc_link == 'al' or '   Link Down' == fc_stat:
                fc_link = "\033[1;31mDOWN\033[1;00m"
            elif fc_link == 'switch' or '   Link Up' == fc_stat:
                fc_link = "\033[1;32mUP\033[1;00m"
            print "Link Status: %s" % fc_link

            if speed_port[3] != speed_running[3]:
                print ("Speed Port (supported): \033[1;34m%s\033[1;00m %s" % (speed_port[3], speed_port[4]))
                print ("Speed Port (running): \033[1;33m%s\033[1;00m %s" % (speed_running[3], speed_running[4]))
            else:
                print ("Speed Port (supported): \033[1;34m%s\033[1;00m %s" % (speed_port[3], speed_port[4]))
                print ("Speed Port (running): \033[1;34m%s\033[1;00m %s" % (speed_running[3], speed_running[4]))

            print wwpn

            if last_errlog != '':
                print "\nLast Adapter Erros in ERRPT/ERRLOG:"
                print "----- ------- ----  -- -------------"
                print "CODE\t   MMDDHHMMYY T C RESOURCE	 DESCRIPTION"
                print last_errlog+"\n"
            else:
                print '\n'

