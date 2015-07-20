<!DOCTYPE html>
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<LINK REL="stylesheet" TYPE="text/css" HREF="site.css">
<link rel="icon" type="image/png" href="/favicon.png">
</HEAD>
<BODY>

<DIV CLASS="header" ID="header">
</DIV>

<DIV CLASS="body" ID="body">

<H1>PowerAdm - IBM Power/PowerVM Administration tool</H1>
<H2>Web Interface</H2>

<CODE>[ PowerAdm Adm ]</P>
<P>[ Version: {{ version }} - © 2014, 2015 Kairo Araujo - BSD License ]</P>
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
<script type="text/javascript">
function id(el) {
        return document.getElementById(el);
}
// form vfc
function show_form_vfc() {
        id('vfc_form').style.display = 'block';
}

function hide_form_vfc() {
        id('vfc_form').style.display = 'none';
}
</script>

<fieldset>
<legend>Previous configuration</legend>
<!-- LPAR Configuration -->
<div><b>Change: </b>{{change}}</div>
<div><b>Prefix: </b>{{prefix}}</div>
<div><b>LPAR Name: </b>{{lparname}}</div>
<div><b>Entitled CPU: </b>{{lparentcpu}}</div>
<div><b>Virtual CPU: </b>{{lparvcpu}}</div>
<div><b>Memory: </b>{{lparmem}}</div>
<div><b>NIM Deploy enabled: </b>{{nim_deploy}}</div>
% if nim_deploy == 'y':
    <div><b>NIM Deploy Virtual Switch: </b>{{vsw_deploy}}</div>
    <div><b>NIM Deploy VLAN: </b>{{vlan_deploy}}</div>
%end
<div><b>Host Server: </b>{{psystem}}</div>
<div><b>Virtual SCSI: </b>{{vscsi}}</div>
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
</fieldset>
<p></p>

<form action="/lpar_config_validate" class="form-horizontal" method="GET">
<fieldset>
<!-- script to hide if option to prepare to deploy using NIM is yes -->

<!-- Form Name -->
<legend>LPAR CONFIGURATION (NPIV)</legend>

<b><label class="control-label" for="vfc">Do you want add Virtual Fiber Adapter (HBA/NPIV)?</label></b>
<div class="controls">
    <b><label class="radio" for="vfc_yes">
    <input type="radio" name="vfc" id="vfc_yes" value="y" onclick="javascript:show_form_vfc();" checked="checked">
    yes
    </label></b>
    <b><label class="radio" for="vfc_no">
    <input type="radio" name="vfc" id="vfc_no" value="n" onclick="javascript:hide_form_vfc();">
     no
    </label></b>
</div>
<p></p>

<!-- Select the vFC VIO1 hosts -->
<div id="vfc_form" >
    <div class="control-group">
        <b><label class="control-label" for="">Select the NPIV FC of {{vio1}}</label></b>
        <div class="controls">
            <select id="npiv_vio1" name="npiv_vio1" class="input-xlarge">
                %for fcs in npiv_vio1:
                    <option>{{fcs}}</option>
                %end
            </select>
        </div>
    </div>
    <div class="control-group">
        <b><label class="control-label" for="">Select the NPIV FC of {{vio2}} </label></b>
        <div class="controls">
            <select id="npiv_vio2" name="npiv_vio2" class="input-xlarge">
                %for fcs in npiv_vio2:
                    <option>{{fcs}}</option> 
                %end
            </select>
        </div>
    </div>

</div>

<!-- Finish, goes to validation_lpar -->
<p><div class="control-group">
  <b><label class="control-label" for="continue"></label></b>
  <div class="controls">
    <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
    <button id="next" name="next" class="btn btn-primary"> NEXT </button>
  </div>
</div></p>


</fieldset>
</form>

<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
</CODE>

</DIV>
</BODY>
</HTML>
