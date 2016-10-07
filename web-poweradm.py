#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Power Adm
"""
PowerAdm
web-poweradm.py

Copyright (c) 2015-2016 Kairo Araujo.

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

# imports
###############################################################################
import poweradm.globalvar
import poweradm.config
import poweradm.npiv
import poweradm.newid
import poweradm.config
import commands
from www.bottle import *

# global variables from the classes and functions of poweradm
version = poweradm.globalvar.version
web_port = poweradm.config.web_port
web_address = poweradm.config.web_address
enable_nim_deploy = poweradm.config.enable_nim_deploy.lower()
virtual_switches = poweradm.config.virtual_switches
psystems = list(poweradm.config.systems.keys())
active_ssp = poweradm.config.active_ssp.lower()
storage_pools = poweradm.config.storage_pools
npivs = poweradm.npiv.NPIV()
system_vio = poweradm.systemvios.SystemVios()
freeid = poweradm.newid.NewID()


@route('<filename:path>')
def server_static(filename):
    """ This is for static files """
    return static_file(filename, root='www/static/')


@route('/')
def poweradm():
    """ Index page """

    output = template('www/index', version=version)
    return output


@route('/lpar_config', method='GET')
def lpar_config():
    """ LPAR configuration. """

    output = template('www/lpar_config', version=version)
    return output


@route('/lpar_config_sys_net', method='GET')
def lpar_config_sys_net():
    """ LPAR configuration.
        - OS NIM Deploy options
        - pSystem/host server option
        - Network options
    """

    # global variables of this page
    global change, prefix, lparname, lparentcpu, lparvcpu, lparmem

    # colect the GET request variables
    change = request.GET.get('change', '')
    prefix = request.GET.get('prefix', '')
    lparname = request.GET.get('lparname', '')
    lparentcpu = float(request.GET.get('lparentcpu', ''))
    lparvcpu = int(request.GET.get('lparvcpu', ''))
    lparmem = int(request.GET.get('lparmem', ''))

    # output with the variables
    output = template('www/lpar_config_sys_net', version=version,
                      change=change, prefix=prefix, lparname=lparname,
                      lparentcpu=lparentcpu, lparvcpu=lparvcpu,
                      lparmem=lparmem, psystems=psystems,
                      active_ssp=active_ssp, storage_pools=storage_pools,
                      enable_nim_deploy=enable_nim_deploy,
                      virtual_switches=virtual_switches)
    return output


@route('/lpar_config_npiv', method='GET')
def lpar_config_npiv():
    # import poweradm modules
    import poweradm.config

    """ LPAR configuration.
        - Select NPIV configurations
    """

    # global variables of this page
    global nim_deploy, vsw_deploy, vlan_deploy, psystem, vscsi, add_disk
    global disk_size, net_length, stgpool, net_vlan1, net_vlan2_1, net_vlan2_2
    global net_vlan3_1, net_vlan3_2, net_vlan3_3, net_vsw1, net_vsw2_1
    global net_vsw2_2, net_vsw3_1, net_vsw3_2, net_vsw3_3, vio1, vio2

    # colect the GET request variables
    nim_deploy = request.GET.get('nim_deploy', '')
    vsw_deploy = request.GET.get('vsw_deploy', '')
    vlan_deploy = request.GET.get('vlan_deploy', '')
    psystem = request.GET.get('psystem', '')
    vscsi = request.GET.get('vscsi', '')
    add_disk = request.GET.get('add_disk', '')
    disk_size = request.GET.get('disk_size', '')
    stgpool = request.GET.get('stgpool', '')
    net_length = request.GET.get('net_length', '')

    # if nim_deploy is not selected, the vsw_deploy and vlan_deploy is null
    if nim_deploy == 'n':
        vsw_deploy = 'null'
        vlan_deploy = 'null'

    # if add_disk is different of yes, the disk size is 0 and stgpool is null
    if add_disk != 'y':
        disk_size = '0'
        stgpool = 'null'

    # if number of ethernets is 1
    if net_length == '1':
        net_vlan1 = request.GET.get('net_vlan1', '')
        net_vlan2_1 = 'null'
        net_vlan2_2 = 'null'
        net_vlan3_1 = 'null'
        net_vlan3_2 = 'null'
        net_vlan3_3 = 'null'
        net_vsw1 = request.GET.get('net_vsw1', '')
        net_vsw2_1 = 'null'
        net_vsw2_2 = 'null'
        net_vsw3_1 = 'null'
        net_vsw3_2 = 'null'
        net_vsw3_3 = 'null'

    # if number of ethernets is 2
    elif net_length == '2':
        net_vlan1 = 'null'
        net_vlan2_1 = request.GET.get('net_vlan2_1', '')
        net_vlan2_2 = request.GET.get('net_vlan2_2', '')
        net_vlan3_1 = 'null'
        net_vlan3_2 = 'null'
        net_vlan3_3 = 'null'
        net_vsw1 = 'null'
        net_vsw2_1 = request.GET.get('net_vsw2_1', '')
        net_vsw2_2 = request.GET.get('net_vsw2_2', '')
        net_vsw3_1 = 'null'
        net_vsw3_2 = 'null'
        net_vsw3_3 = 'null'

    # if number of ethernets is 3
    elif net_length == '3':
        net_vlan1 = 'null'
        net_vlan2_1 = 'null'
        net_vlan2_2 = 'null'
        net_vlan3_1 = request.GET.get('net_vlan3_1', '')
        net_vlan3_2 = request.GET.get('net_vlan3_2', '')
        net_vlan3_3 = request.GET.get('net_vlan3_3', '')
        net_vsw1 = 'null'
        net_vsw3_1 = request.GET.get('net_vsw3_1', '')
        net_vsw3_2 = request.GET.get('net_vsw3_2', '')
        net_vsw3_3 = request.GET.get('net_vsw3_3', '')
        net_vsw2_1 = 'null'
        net_vsw2_2 = 'null'

    # get informations about VIOs
    npiv_vio1 = npivs.printFCVIO(psystem, 'vio1')
    npiv_vio2 = npivs.printFCVIO(psystem, 'vio2')
    vio1 = system_vio.returnVio1(psystem)
    vio2 = system_vio.returnVio2(psystem)

    if os.path.isfile('%s/npiv/%s-%s' % (poweradm.config.pahome, psystem,
                                         vio1)):
        vio1_lsnports = commands.getoutput('cat %s/npiv/%s-%s'
                                           % (poweradm.config.pahome, psystem,
                                              vio1))
    else:
        vio1_lsnports = ""

    if os.path.isfile('%s/npiv/%s-%s' % (poweradm.config.pahome, psystem,
                                         vio1)):
        vio2_lsnports = commands.getoutput('cat %s/npiv/%s-%s'
                                           % (poweradm.config.pahome, psystem,
                                              vio2))
    else:
        vio2_lsnports = ""

    # output with the variables
    output = template('www/lpar_config_npiv', version=version, change=change,
                      prefix=prefix, lparname=lparname, lparentcpu=lparentcpu,
                      lparvcpu=lparvcpu, lparmem=lparmem, psystem=psystem,
                      active_ssp=active_ssp, storage_pools=storage_pools,
                      vsw_deploy=vsw_deploy, vlan_deploy=vlan_deploy,
                      enable_nim_deploy=enable_nim_deploy,
                      virtual_switches=virtual_switches, vscsi=vscsi,
                      add_disk=add_disk, disk_size=disk_size,
                      net_length=net_length, stgpool=stgpool,
                      nim_deploy=nim_deploy, net_vlan1=net_vlan1,
                      net_vlan2_1=net_vlan2_1, net_vlan2_2=net_vlan2_2,
                      net_vlan3_1=net_vlan3_1, net_vlan3_2=net_vlan3_2,
                      net_vlan3_3=net_vlan3_3, net_vsw1=net_vsw1,
                      net_vsw2_1=net_vsw2_1, net_vsw2_2=net_vsw2_2,
                      net_vsw3_1=net_vsw3_1, net_vsw3_2=net_vsw3_2,
                      net_vsw3_3=net_vsw3_3, npiv_vio1=npiv_vio1,
                      npiv_vio2=npiv_vio2, vio1=vio1,
                      vio1_lsnports=vio1_lsnports, vio2_lsnports=vio2_lsnports,
                      vio2=vio2)

    return output


@route('/lpar_config_validate', method='GET')
def lpar_config_validate():
    # global variables of this page
    global npiv_vio1, npiv_vio2, vfc

    # get the GET request
    vfc = request.GET.get('vfc', '')

    # if vfc is no the npiv_vio1 and npiv2 is 'none'
    if vfc == "n":
        npiv_vio1 = 'none'
        npiv_vio2 = 'none'
    else:
        npiv_vio1 = request.GET.get('npiv_vio1', '')
        npiv_vio2 = request.GET.get('npiv_vio2', '')

    # output with the variables
    output = template('www/lpar_config_validate', version=version,
                      change=change, prefix=prefix, lparname=lparname,
                      lparentcpu=lparentcpu, lparvcpu=lparvcpu,
                      lparmem=lparmem, psystem=psystem, active_ssp=active_ssp,
                      storage_pools=storage_pools, vsw_deploy=vsw_deploy,
                      vlan_deploy=vlan_deploy,
                      enable_nim_deploy=enable_nim_deploy,
                      virtual_switches=virtual_switches, vscsi=vscsi,
                      add_disk=add_disk, disk_size=disk_size,
                      net_length=net_length, stgpool=stgpool,
                      nim_deploy=nim_deploy, net_vlan1=net_vlan1,
                      net_vlan2_1=net_vlan2_1, net_vlan2_2=net_vlan2_2,
                      net_vlan3_1=net_vlan3_1, net_vlan3_2=net_vlan3_2,
                      net_vlan3_3=net_vlan3_3, net_vsw1=net_vsw1,
                      net_vsw2_1=net_vsw2_1, net_vsw2_2=net_vsw2_2,
                      net_vsw3_1=net_vsw3_1, net_vsw3_2=net_vsw3_2,
                      net_vsw3_3=net_vsw3_3, npiv_vio1=npiv_vio1,
                      npiv_vio2=npiv_vio2, vio1=vio1, vfc=vfc, vio2=vio2)

    return output


@route('/lpar_config_finish', method='GET')
def lpar_config_finish():
    # import classes/functions of the poweradm
    import poweradm.mklparconf
    import poweradm.execchange

    # global variables of this page
    global configlpar, createlpar, lpar_count, lparid, veth, veth_final

    # get variables GET request
    configlpar = request.GET.get('configlpar', '')
    createlpar = request.GET.get('createlpar', '')

    # get the next free id
    nextid = newid.NewID()
    if poweradm.config.vslot_std:
        lparid = nextid.mkid()
    else:
        lparid = nextid.mkid(psystem)

    # convert the ethernets for makelpar function
    if nim_deploy == 'y':
        if net_length == '1':
            veth = ("10/0/%s//0/0/%s" % (vlan_deploy, vsw_deploy))
            veth_final = ("10/0/%s//0/0/%s" % (net_vlan1, net_vsw1))
        elif net_length == '2':
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s"
                    % (vlan_deploy, vsw_deploy, net_vlan2_2, net_vsw2_2))
            veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s"
                          % (net_vlan2_1, net_vsw2_1, net_vlan2_2, net_vsw2_2))
        elif net_length == '3':
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                    (vlan_deploy, vsw_deploy, net_vlan3_2, net_vsw3_2,
                     net_vlan3_3, net_vsw3_3))
            veth_final = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                          (net_vlan3_1, net_vsw3_1, net_vlan3_2, net_vsw3_2,
                           net_vlan3_3, net_vsw3_3))
    else:
        if net_length == '1':
            veth = ("10/0/%s//0/0/%s" % (net_vlan1, net_vsw1))
            veth_final = veth
        elif net_length == '2':
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s"
                    % (net_vlan2_1, net_vsw2_1, net_vlan2_2, net_vsw2_2))
            veth_final = veth
        elif net_length == '3':
            veth = ("10/0/%s//0/0/%s,11/0/%s//0/0/%s,12/0/%s//0/0/%s" %
                    (net_vlan3_1, net_vsw3_1, net_vlan3_2, net_vsw3_2,
                     net_vlan3_3, net_vsw3_3))
            veth_final = veth

    # if configlpar is OK create the file
    if configlpar == 'yes':

        # create LPAR using function poweradm.mklparconf
        newchange = poweradm.mklparconf.MakeLPARConf(change, prefix, lparname,
                                                     lparid, nim_deploy,
                                                     lparmem, lparentcpu,
                                                     lparvcpu, vscsi, add_disk,
                                                     stgpool, disk_size, vfc,
                                                     npiv_vio1, npiv_vio2,
                                                     veth, veth_final, psystem,
                                                     vio1, vio2)

        # write reader
        newchange.headerchange()

        # write the file
        newchange.writechange()

        # close the file
        newchange.closechange()

        # colect file created
        change_file = newchange.returnchange()

        # if create createlpar is yes, run the creation.
        if createlpar == 'yes':
            mkchange = poweradm.execchange.Exe(change_file)
            mklog = mkchange.runChange()
        else:
            mklog = 'none'

        # output with the variables
        output = template('www/lpar_finish', version=version, change=change,
                          prefix=prefix, lparname=lparname,
                          lparentcpu=lparentcpu, lparvcpu=lparvcpu,
                          lparmem=lparmem, psystem=psystem,
                          active_ssp=active_ssp, storage_pools=storage_pools,
                          vsw_deploy=vsw_deploy, vlan_deploy=vlan_deploy,
                          enable_nim_deploy=enable_nim_deploy,
                          virtual_switches=virtual_switches, vscsi=vscsi,
                          add_disk=add_disk, disk_size=disk_size,
                          net_length=net_length, stgpool=stgpool,
                          nim_deploy=nim_deploy, net_vlan1=net_vlan1,
                          net_vlan2_1=net_vlan2_1, net_vlan2_2=net_vlan2_2,
                          net_vlan3_1=net_vlan3_1, net_vlan3_2=net_vlan3_2,
                          net_vlan3_3=net_vlan3_3, net_vsw1=net_vsw1,
                          net_vsw2_1=net_vsw2_1, net_vsw2_2=net_vsw2_2,
                          net_vsw3_1=net_vsw3_1, net_vsw3_2=net_vsw3_2,
                          net_vsw3_3=net_vsw3_3, npiv_vio1=npiv_vio1,
                          npiv_vio2=npiv_vio2, vio1=vio1, vfc=vfc, vio2=vio2,
                          change_file=change_file, configlpar=configlpar,
                          createlpar=createlpar, mklog=mklog)

        return output

    else:
        # if is not, just change_file and mklog is none and go to the page out.

        change_file = 'none'
        mklog = 'none'

        # output with the variables
        output = template('www/lpar_finish', version=version, change=change,
                          prefix=prefix, lparname=lparname,
                          lparentcpu=lparentcpu, lparvcpu=lparvcpu,
                          lparmem=lparmem, psystem=psystem,
                          active_ssp=active_ssp, storage_pools=storage_pools,
                          vsw_deploy=vsw_deploy, vlan_deploy=vlan_deploy,
                          enable_nim_deploy=enable_nim_deploy,
                          virtual_switches=virtual_switches, vscsi=vscsi,
                          add_disk=add_disk, disk_size=disk_size,
                          net_length=net_length, stgpool=stgpool,
                          nim_deploy=nim_deploy, net_vlan1=net_vlan1,
                          net_vlan2_1=net_vlan2_1, net_vlan2_2=net_vlan2_2,
                          net_vlan3_1=net_vlan3_1, net_vlan3_2=net_vlan3_2,
                          net_vlan3_3=net_vlan3_3, net_vsw1=net_vsw1,
                          net_vsw2_1=net_vsw2_1, net_vsw2_2=net_vsw2_2,
                          net_vsw3_1=net_vsw3_1, net_vsw3_2=net_vsw3_2,
                          net_vsw3_3=net_vsw3_3, npiv_vio1=npiv_vio1,
                          npiv_vio2=npiv_vio2, vio1=vio1, vfc=vfc, vio2=vio2,
                          change_file=change_file, configlpar=configlpar,
                          createlpar=createlpar, mklog=mklog)

        return output


@route('/lpar_exec')
def lpar_exec():
    # import findchange from poweradm
    import poweradm.findchange

    # Find the File Change/Ticket using class FindChange()
    exec_findlpar = poweradm.findchange.FindChange()
    change_files = exec_findlpar.listChanges()

    # output with the variables
    output = template('www/lpar_exec', version=version,
                      change_files=change_files)

    return output


@route('/lpar_do', method='GET')
def lpar_do():
    # import config and execchange of poweradm
    import poweradm.config
    import poweradm.execchange

    # global variables from this page
    global change_file, exec_lpar

    change_file = request.GET.get('change_file', '')
    exec_lpar = request.GET.get('exec_lpar', '')
    pahome = poweradm.config.pahome

    # if exec_lpar is yes, execute the file creation
    if exec_lpar == 'yes':
        mkchange = poweradm.execchange.Exe('%s/poweradm/changes/%s' %
                                           (pahome, change_file))
        mklog = mkchange.runChange()
    else:
        mklog = 'none'

    # output with the variables
    output = template('www/lpar_do', version=version, change_file=change_file,
                      exec_lpar=exec_lpar, pahome=pahome, mklog=mklog)

    return output


@route('/deploy')
def deploy():
    # import NIM Class from PowerAdm
    import poweradm.nim

    # NIM available files/LPARs configs to deplo
    cfgdeploylist = poweradm.nim.NIMFileFind()
    deploy_list = cfgdeploylist.listDeploy()

    # NIM available OS versions
    osdeploylist = poweradm.nim.NIMGetVer()
    os_list = osdeploylist.listOSVersion()

    # NIM available Servers
    nimserverlist = poweradm.nim.NIMServer()
    nimsrv_list = nimserverlist.listNIM()

    # output with the variables
    output = template('www/deploy', version=version, deploy_list=deploy_list,
                      os_list=os_list, nimsrv_list=nimsrv_list)

    return output


@route('/deploy_do', method='GET')
def deploy_do():
    # import NIM Class from PowerAdm
    import poweradm.nim
    import poweradm.config
    import poweradm.mkosdeploy

    deploy_file = request.GET.get('deploy_file', '')
    os_version = request.GET.get('os_version', '')
    nimsrv = request.GET.get('nimsrv', '')
    deploy_lpar = request.GET.get('deploy_lpar', '')

    nimfile = poweradm.nim.NIMFileFind()
    nim_file = ('%s/poweradm/nim/%s' % (poweradm.config.pahome, deploy_file))
    nimfile.fileData(nim_file)

    # get variables
    lparprefix = nimfile.returnDeployPrefix()
    lparname = nimfile.returnDeployLPARName()
    lparframe = nimfile.returnDeployFrame()
    lparvlans = nimfile.returnDeployVLANFinal()

    # select version to install
    #
    nimcfg = poweradm.nim.NIMGetVer()
    nimcfg.OSVersion(os_version)
    nim_cfg_ver = nimcfg.getOSVersion()
    nim_cfg_spot = nimcfg.getSpot()
    nim_cfg_mksysbspot = nimcfg.getMksysbLpp()

    # select nim and get variables
    #
    nimvars = poweradm.nim.NIMServer()
    nimvars.getNIM(nimsrv)
    nim_address = nimvars.getNIMAddress()
    nim_ipstart = nimvars.getIPStart()
    nim_ipend = nimvars.getIPEnd()
    nim_ipnet = nimvars.getIPNet()
    nim_server = nimvars.getNIMServer()
    nim_ipdeploy = nimvars.getNIMIPDeploy()

    # Deployment
    print(lparprefix, lparname, lparframe, lparvlans, nim_file, nim_cfg_ver,
          nim_cfg_spot, nim_cfg_mksysbspot, nim_address, nim_ipstart,
          nim_ipend, nim_ipnet, nim_server, nim_ipdeploy, deploy_lpar)

    deploy_os = poweradm.mkosdeploy.MakeNIMDeploy(
        lparprefix, lparname, lparframe, lparvlans, nim_file, nim_cfg_ver,
        nim_cfg_spot, nim_cfg_mksysbspot, nim_address, nim_ipstart, nim_ipend,
        nim_ipnet, nim_server, nim_ipdeploy, deploy_lpar)

    mklog = deploy_os.createNIMDeploy()

    output = template('www/deploy_do', version=version,
                      deploy_lpar=deploy_lpar, deploy_file=deploy_file,
                      lparframe=lparframe, os_version=os_version,
                      lparprefix=lparprefix, lparname=lparname, nimsrv=nimsrv,
                      nim_address=nim_address, nim_ipdeploy=nim_ipdeploy,
                      mklog=mklog)

    return output


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(host=web_address,
    port=web_port,
    reloader=True)
