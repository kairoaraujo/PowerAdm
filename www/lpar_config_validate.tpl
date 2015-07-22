<!DOCTYPE html>
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<LINK REL="stylesheet" TYPE="text/css" HREF="site.css">
<link rel="icon" type="image/png" href="/favicon.png">
</HEAD>
<BODY>

<DIV CLASS="header" ID="header">
<H1>PowerAdm - IBM Power/PowerVM Administration tool</H1>
<H2>Web Interface</H2>
</DIV>

<DIV CLASS="body" ID="body">
<P>[ PowerAdm Adm ]</P>
<P>[ Version: {{ version }} - © 2014, 2015 Kairo Araujo - BSD License ]</P>
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
<script type="text/javascript">
function id(el) {
        return document.getElementById(el);
}
// form configlpar
function show_form_configlpar() {
        id('configlpar_form').style.display = 'block';
}

function hide_form_configlpar() {
        id('configlpar_form').style.display = 'none';
}
</script>
<fieldset>
<legend>Previous configuration </legend>
<div><b>Change: </b>{{change}}</div>
<div><b>Prefix: </b>{{prefix}}</div>
<div><b>LPAR Name: </b>{{lparname}}</div>
<div><b>Entitled CPU: </b>{{lparentcpu}}</div>
<div><b>Virtual CPU: </b>{{lparvcpu}}</div>
<div><b>Memory: </b>{{lparmem}}</div>

<div><b>NIM Deploy enabled: </b>{{nim_deploy}}</div>
% if nim_deploy == 'yes':
    <div><b>NIM Deploy Virtual Switch: </b>{{vsw_deploy}}</div>
    <div><b>NIM Deploy VLAN: </b>{{vlan_deploy}}</div>
%end
<div><b>Host Server: </b>{{psystem}}</div>
<div><b>Virtual SCSI: </b>{{vscsi}}</div>

<div><b>Add disk:</b> {{add_disk}}</div>
% if add_disk == 'y':
    <div><b>Disk size: </b>{{disk_size}} GB</div>
    <div><b>Shared Storage Pool: </b>{{stgpool}}</div>
%end

<div><b>Number of Ethernets: </b>{{net_length}}</div>
% if net_length == '1':
    <div><b>Ethernet Virtual Switch 1: </b>{{net_vsw1}}</div>
    <div><b>Ethernet VLAN 1: </b>{{net_vlan1}}</div>
%end
% if net_length == '2':
    <div><b>Ethernet Virtual Switch 1: </b>{{net_vsw2_1}}</div>
    <div><b>Ethernet VLAN 1: </b>{{net_vlan2_1}}</div>
    <div><b>Ethernet Virtual Switch 2: </b>{{net_vsw2_2}}</div>
    <div><b>Ethernet VLAN 2: </b>{{net_vlan2_2}}</div>
%end
% if net_length == '3':
    <div><b>Ethernet Virtual Switch 1: </b>{{net_vsw3_1}}</div>
    <div><b>Ethernet VLAN 1: </b>{{net_vlan3_1}}</div>
    <div><b>Ethernet Virtual Switch 2: </b>{{net_vsw3_2}}</div>
    <div><b>Ethernet VLAN 2: </b>{{net_vlan3_2}}</div>
    <div><b>Ethernet Virtual Switch 3: </b>{{net_vsw3_3}}</div>
    <div><b>Ethernet VLAN 3: </b>{{net_vlan3_3}}</div>
%end

<div><b>Virtual Fibre Channel (NPIV): </b>{{vfc}}</div>
% if vfc == 'y':
   <div><b>FC VIO Server: {{vio1}} </b>{{npiv_vio1}}</div>
   <div><b>FC VIO Server: {{vio2}} </b>{{npiv_vio2}}</div>
%end
</fieldset>
<p></p>

<form action="/lpar_config_finish" class="form-horizontal" method="GET">
<fieldset>
<!-- script to hide if option to prepare to deploy using NIM is yes -->

<!-- Form Name -->
<legend>LPAR CONFIGURATION CONFIRMATION</legend>

<b><label class="control-label" for="configlpar">The configuration of the last LPAR is OK?</label></b>
<div class="controls">
    <label class="radio" for="configlpar_yes">
    <input type="radio" name="configlpar" id="configlpar_yes" value="yes" >
    yes
    </label></b>
    <label class="radio" for="configlpar_no">
    <input type="radio" name="configlpar" id="configlpar_no" value="no" checked="checked">
    no
    </label></b>
</div>
<p></p>
<b><label class="control-label" for="createlpar">Do you want create this LPAR now?</label></b>
<div class="controls">
    <label class="radio" for="createlpar_yes">
    <input type="radio" name="createlpar" id="createlpar_yes" value="yes" >
    yes (create LPAR when you confirm)
    </label></b>
    <label class="radio" for="createlpar_no">
    <input type="radio" name="createlpar" id="createlpar_no" value="no" checked="checked">
    no (save LPAR creation for further)
    </label></b>
</div>

<p></p>

<!-- Finish, goes to validation_lpar -->
<div class="control-group">
  <b><label class="control-label" for="confirmation"></label></b>
  <div class="controls">
    <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
    <button id="next" name="next" class="btn btn-primary">CONFIRM</button>
  </div>
</div>

</fieldset>
</form>

<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>

</DIV>
</BODY>
</HTML>
