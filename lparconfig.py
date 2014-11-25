#!/usr/bin/env python
#
# Copyright (c) 2014 Kairo Araujo
#
# vvu is vio vhost utility
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

# import modules
###############################################################################################
import os.path
import time

# Configuration
###############################################################################################
# Put here the minimum and maximum memory percent to lpars
mem_min = 50
mem_max = 50
# Put here the minimum and maximum cpu percent to lpars
cpu_min = 50
cpu_max = 100
# Systems
systems = ['P1-8205-E6D-SN06A07AT', 'P1-8205-E6D-SN06A07BT', 'P1-8205-E6D-SN06A07CT']
# Virtual Switches
virtual_switches = ['VSW-GERENCIA-01', 'VSW-DADOS-01', 'VSW-BACKUP-01']

# Global Variables
###############################################################################################
timestr = time.strftime("%d%m%Y-%H%M%S")
version = '0.1b'

# functions
###############################################################################################


class Server:
    def __init__(self, prefix, lparname, lparentcpu, lparvcpu, lparmem):
        self.prefix = prefix
        self.lparname = lparname
        self.lparentcpu = lparentcpu
        self.lparvcpu = lparvcpu
        self.lparmem = lparmem

    def lparconf(self):
        self.prefix = input("Prefix (XXXX-lparname): ")
        self.lparname = input("LPAR Hostname: ")
        self.lparentcpu = float(input("LPAR Entitled CPU desired: "))
        lparentcpumin = self.lparentcpu-(self.lparentcpu*cpu_min/100)
        lparentcpumax = (self.lparentcpu*cpu_max/100)+self.lparentcpu
        self.lparvcpu = int(input("LPAR Virtual CPU desired: "))
        lparvcpumin = self.lparvcpu-(self.lparvcpu*cpu_min/100)
        if lparvcpumin < 1:
            lparvcpumin = 1
        lparvcpumax = (self.lparvcpu*cpu_max/100)+self.lparvcpu
        self.lparmem = int(input("LPAR Memory desired: "))
        lparmenmin = self.lparmem-(self.lparmem*mem_min/100)
        lparmenmax = (self.lparmem*mem_max/100)+self.lparmem


        # Select System
        print ("\nSelect the system host for LPAR")
        systems_length = (len(systems))-1
        count = 0
        while count <= systems_length:
            print ("%s : %s" % (count, systems[count]))
            count += 1
        system_option = int(input("System: "))
        #print ("%s" % systems[system_option])

        # Get the next free ID -- to be add
        ids = ['1', '2', '3', '100', '135', '90', '80']
        ids.sort(key=int)
        lastid = len(ids)-1
        nextid = int(ids[lastid])+1

        answer = 'y'
        net_vsw = []
        net_vlan = []

        while (answer == 'y') or (answer == 'Y'):

            print ("\nNetwork Configuration:\n")
            vsw_length = (len(virtual_switches))-1

            count = 0
            while count <= vsw_length:
                print ("%s : %s" % (count, virtual_switches[count]))
                count +=1
            vsw_option = int(input("Virtual Switch: "))

            net_vsw.append(virtual_switches[vsw_option])
            net_vlan.append(input("Ethernet VLAN (%s): " % virtual_switches[vsw_option]))

            check_ok = 0
            while check_ok == 0:
                answer = input("Do you want another network interface? (y/n): ")
                if len(net_vsw) == 3:
                    print ("Maximum Ethernet adapter is 3 to initial config. Sorry")
                    answer = 'n'
                    break
                if (answer == 'y') or (answer == 'Y'):
                    answer = 'y'
                    check_ok = 1

                elif (answer == 'n') or (answer == 'N'):
                    answer = 'n'
                    check_ok = 1
                else:
                    print ("Please use y or n!")
                    check_ok = 0

        net_length = len(net_vsw)-1


        print ("\nCheck configuration last LPAR:\n\n"
               "LPAR name: %s-%s hosted in %s with ID %s\n"
               "Entitled CPU: Minimum: %.1f , Desired: %.1f, Maximum: %.1f\n"
               "Virtual CPU : Minimum: %s , Desired: %s, Maximum: %s\n"
               "Memory      : Minimum: %s , Desired: %s, Maximum: %s"
               % (self.prefix, self.lparname, systems[system_option], nextid,
                  lparentcpumin, self.lparentcpu, lparentcpumax, lparvcpumin,
                  self.lparvcpu, lparvcpumax, lparmenmin, self.lparmem, lparmenmax ))
        count = 0
        while count <= net_length:
            print ("Network %s: Virtual Switch: %s - VLAN: %s" % (count, net_vsw[count], net_vlan[count]))
            count += 1

        if net_length == 0:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,\'" % (net_vlan[0],net_vsw[0]))
        elif net_length == 1:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,\'" % (net_vlan[0],net_vsw[0],
                                    net_vlan[1],net_vsw[1]))
        elif net_length == 2:
            virtual_eth_adapters = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s\'," % (net_vlan[0],
                                    net_vsw[0], net_vlan[1], net_vsw[1], net_vlan[2], net_vsw[2]))

        # Getting vios --- to be add
        vios = ['vio1tvttsm01','vio2tvttms01']

        answer = 'y'
        check_ok = 0
        while (answer == 'y') or (answer == 'Y'):
            while check_ok == 0:
                answer = input("\nThe configuration of last LPAR is OK?(y/n) ")
                if (answer == 'y') or (answer == 'Y'):
                    answer = 'n'
                    check_ok = 1
                    f_change = open("changes/%s_%s.sh" % (change, timestr) , 'w')
                    f_change.write("#!/bin/sh\n"
                                   "# change %s\n" % (change))
                    f_change.write("mksyscfg -r lpar -m %s -i 'name=%s-%s, "
                                   "lpar_id=%s ,profile_name=%s, lpar_env=aixlinux, min_mem=%s "
                                   "desired_mem=%s, max_mem=%s, proc_mode=shared, min_procs=%s,"
                                   "desired_procs=%s, max_procs=%s, min_proc_units=%s, desired_proc_units=%s, "
                                   "max_proc_units=%s, sharing_mode=uncap, uncap_weight=128, conn_monitoring=1, "
                                   "boot_mode=norm, max_virtual_slots=40, "
                                   "\'virtual_eth_adapters=%s"
                                   "\'virtual_fc_adapters=33/client//%s/3%s//0,34/client//%s/4%s//0\' '\n"
                                   % ( systems[system_option], self.prefix, self.lparname, nextid, self.lparname,
                                       lparmenmin, self.lparmem, lparmenmax, lparvcpumin, self.lparvcpu,
                                       lparvcpumax,lparentcpumin, self.lparentcpu, lparentcpumax,
                                       virtual_eth_adapters, vios[0], nextid, vios[1], nextid))
                    print ("File changes/%s-%s.sh write with success!" % (change, timestr))
                elif (answer == 'n') or (answer == 'N'):
                    answer = 'n'
                    check_ok = 1
                    print ("Configuration not saved!")
                    exit
                else:
                    print ("Please use y or n!")
                    check_ok = 0

def mklpar():
    newlpar = Server('nprefix', 'nlparname', 'nlparentcpu', 'nlparcpu', 'nlparmem')
    newlpar.lparconf()


# main
###############################################################################################

os.system('clear')
print ("\n\n[ Power Adm ]\n[ Version: %s - © 2014 Kairo Araujo - BSD License ]\n\n" % version)

print ("[LPAR Configuration ]\n")
change = input("Change or Ticket number: ")
mklpar()

answer = 'y'
while (answer == 'y') or (answer == 'Y'):
    check_ok = 0
    while check_ok == 0:
        answer = input("Do you want add another LPAR on Changer or Ticket %s: " % change)
        if (answer == 'y') or (answer == 'Y'):
            answer = 'y'
            check_ok = 1
            mklpar()
        elif (answer == 'n') or (answer == 'N'):
            answer = 'n'
            check_ok = 1
        else:
            print ("Please use y or n!")
            check_ok = 0









