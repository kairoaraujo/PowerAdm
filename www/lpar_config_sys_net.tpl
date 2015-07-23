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

<fieldset>
<legend>Previous configuration</legend>
<!-- LPAR Configuration -->
<div><b>Change: </b>{{change}}</div>
<div><b>Prefix: </b>{{prefix}}</div>
<div><b>LPAR Name: </b>{{lparname}}</div>
<div><b>Entitled CPU: </b>{{lparentcpu}}</div>
<div><b>Virtual CPU: </b>{{lparvcpu}}</div>
<div><b>Memory: </b>{{lparmem}}</div>
<p></p>
</fieldset>
<p></p>
<form action="/lpar_config_npiv" class="form-horizontal" method="GET">
<fieldset>
<!-- script to hide if option to prepare to deploy using NIM is yes -->
<script type="text/javascript">
function id(el) {
    return document.getElementById(el);
}

// form deploy
function show_form_deploy() {
    id('vsw_deploy_form').style.display = 'block';
    id('vlan_deploy_form').style.display = 'block';
}

function hide_form_deploy() {
    id('vsw_deploy_form').style.display = 'none';
    id('vlan_deploy_form').style.display = 'none';

}

// form add_disk
function show_form_add_disk() {
    id('add_disk_form').style.display = 'block';
}

function hide_form_add_disk() {
    id('add_disk_form').style.display = 'none';
}

// form disk_size
function show_form_disk_size() {
    id('disk_size_form').style.display = 'block';
}

function hide_form_disk_size() {
    id('disk_size_form').style.display = 'none';
}

//
// Control the forms with net configurations
//

// form net_1 
function show_form_net_1() {
    id('net_1_form').style.display = 'block';
}

function hide_form_net_1() {
    id('net_1_form').style.display = 'none';
}

// form net_2 
function show_form_net_2() {
    id('net_2_form').style.display = 'block';
}

function hide_form_net_2() {
    id('net_2_form').style.display = 'none';
}

// form net_3 
function show_form_net_3() {
    id('net_3_form').style.display = 'block';
}

function hide_form_net_3() {
    id('net_3_form').style.display = 'none';
}

// end of net forms control

</script>
<!-- end of script -->

<!-- Form Name -->
<legend>LPAR CONFIGURATION (Prepare NIM Deploy | Virtual SCSI | SSP | Disk | Ethernets)</legend>

<!-- Deploy LPAR using NIM Server -->
<!-- Show only if enable_nim_deploy is enabled on config file -->
%if enable_nim_deploy == 'yes':  
    <!-- radio buttons for nim -->
    <div class="control-group">
    
        <b><label class="control-label" for="nim_deploy">Do you want prepare LPAR to deploy OS using NIM?</label></b>
        <div class="controls">
            <b><label class="radio" for="nim_deploy-0">
                <input type="radio" name="nim_deploy" id="nim_deploy-0" value="y" onclick="javascript:show_form_deploy();"
                checked="checked">
                yes
            </label></b>
            <b><label class="radio" for="nim_deploy-1">
                <input type="radio" name="nim_deploy" id="nim_deploy-1" value="n"  onclick="javascript:hide_form_deploy();">
                no
            </label></b>
        </div>
        <p></p>
        <!-- Virtual Switch to Deploy -->
        <div id="vsw_deploy_form" class="control-group">
            <label class="control-label" for="vsw_deploy">Virtual Switch to Deploy:</label>
            <div class="controls">
                <select id="vsw_deploy" name="vsw_deploy" class="input-xlarge">
                    <!-- list of virtual switches -->
                    %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                    %end
                </select>
            </div>
    </div>

        <!-- VLAN Deploy (text)-->
        <div id="vlan_deploy_form" class="control-group">
            <label class="control-label" for="vlan_deploy">VLAN Deploy:</label>
            <div class="controls">
                <input id="vlan_deploy" name="vlan_deploy" type="number" value="1" min="1" placeholder="2323" class="input-mini" required="">
                <p class="help-block">Help: VLAN ID, use numbers only.</p>
            </div>
        </div>
%end

<!-- Select the pSystems hosts -->

<div class="control-group">
    <b><label class="control-label" for="psystem">Select the psystem host for LPAR:</label></b>
    <div class="controls">
        <select id="psystem" name="psystem" class="input-xlarge" onchange="psystemChange(this);">
            %for psys in psystems:
                <option>{{psys}}</option>
            %end
        </select>
    </div>
</div>
<p></p>

<!-- Add vscsi -->
<b><label class="control-label" for="vscsi">Do you want add Virtual SCSI to LPAR?</label></b>
<div class="controls">
    <b><label class="radio" for="vscsi_yes">
    <input type="radio" name="vscsi" id="vscsi_yes" value="y" onclick="javascript:show_form_add_disk();">
    yes
    </label></b>
    <b><label class="radio" for="vscsi_no">
    <input type="radio" name="vscsi" id="vscsi_no" value="n" onclick="javascript:hide_form_add_disk();" checked="checked">
     no
    </label></b>
</div>
<p></p>

<!-- Add disk using SSP -->
<!-- Show only if active_ssp is enabled on config file -->
%if active_ssp == 'yes':
    <div id="add_disk_form" class="controls" style="display:none;">
        <b><label class="control-label" for="add_disk">Do you want add an disk from Storage Pool to LPAR?</label></b>
        <div class="controls">
            <b><label class="radio" for="add_disk_yes">
            <input type="radio" name="add_disk" id="add_disk_yes" value="y" onclick="javascript:show_form_disk_size();">
            yes
            </label></b>
            <b><label class="radio" for="add_disk_no">
            <input type="radio" name="add_disk" id="add_disk_no" value="n" onclick="javascript:hide_form_disk_size();"
            checked="checked">
            no
            </label></b>
        </div>
    </div>
        <!-- Disk size (text) and Storage Pool-->
        <p></p>
        <div id="disk_size_form" class="control-group" style="display:none;">
            <label class="control-label" for="disk_size">Disk size:</label>
            <div class="controls">
                <input id="disk_size" name="disk_size" type="number" min="10" value="50" placeholder="50" class="input-mini" >
                <p class="help-block">Help: The size of disk without GB. Example: 50 or 100</p>
            </div>
            <label class="control-label" for="stgpool">Select the Storage Pool to add the disk:</label>
            <div class="controls">
                <select id="disk_size" name="stgpool" class="input-xlarge">
                    %for stgpool in storage_pools:
                    <option>{{stgpool}}</option>
                    %end
                </select>
            </div>
        </div>
        <p></p>
%end

<!-- Number of virtual ethernets -->
<div class="control-group">
  <b><label class="control-label" for="net_length">Number of Ethernet</label></b>
  <div class="controls">
    <label class="radio inline" for="net_length-1">
      <input type="radio" name="net_length" id="net_length-1" value="1" onclick="javascript:show_form_net_1(); 
      javascript:hide_form_net_2(); javascript:hide_form_net_3()" checked="checked">
      1
    </label>
    <label class="radio inline" for="net_length-1">
      <input type="radio" name="net_length" id="net_length-2" value="2" onclick="javascript:show_form_net_2();
      javascript:hide_form_net_1(); javascript:hide_form_net_3()">
      2
    </label>
    <label class="radio inline" for="net_length-2">
      <input type="radio" name="net_length" id="net_length-3" value="3" onclick="javascript:show_form_net_3();
      javascript:hide_form_net_1(); javascript:hide_form_net_2()">
      3
    </label>
  <p><label class="control-label" for="stgpool">Help: Select the virtual switch and put the VLAN (number only)</label></p>
  </div>
</div>

<!-- NETWORK FORMS ######################################################### -->
<!-- Form for one Ethernet (net_1_form) -->
<p></p>
<div id="net_1_form">
    <!-- Virtual Switch to Network 1 -->
    <div class="control-group">
        <label class="control-label" for="net_vsw1">Virtual Switch Ethernet 1:</label>
        <div class="controls">
            <select id="net_vsw1" name="net_vsw1" class="input-xlarge">
                <!-- list of virtual switches -->
                %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                %end
            </select>
        </div>
    </div>

    <!-- VLAN Network 1 -->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vlan1">VLAN Ethernet 1:</label>
        <div class="controls">
            <input id="vlan_vlan1" name="net_vlan1" type="number" value="1" min="1" placeholder="2000" class="input-mini" >
        </div>
    </div>
</div>

<!-- Form for 2 Ethernet (net_2_form) -->
<p></p>
<div id="net_2_form" style="display:none;">
    <!-- Virtual Switch  Ethernet 1 of 2-->
    <div class="control-group">
        <label class="control-label" for="net_vsw2_1">Virtual Switch Ethernet 1:</label>
        <div class="controls">
            <select id="net_vsw2_1" name="net_vsw2_1" class="input-xlarge">
                <!-- list of virtual switches -->
                %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                %end
            </select>
        </div>
    </div>

    <!-- VLAN of Ethernet 1 of 2-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vlan2_1">VLAN Ethernet 1:</label>
        <div class="controls">
            <input id="net_vlan2_1" name="net_vlan2_1" type="number" min="1" placeholder="2000" class="input-mini" >
        </div>
    </div>

    <!-- Virtual Switch Ethernet 2 of 2-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vsw2_2">Virtual Switch Ethernet 2:</label>
        <div class="controls">
            <select id="net_vsw2_2" name="net_vsw2_2" class="input-xlarge">
                <!-- list of virtual switches -->
                %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                %end
            </select>
        </div>
    </div>

    <!-- VLAN Ethernet 2 of 2-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vlan2_2">VLAN Ethernet 2:</label>
        <div class="controls">
            <input id="net_vlan2_2" name="net_vlan2_2" type="number" min="1" placeholder="2000" class="input-mini" >
        </div>
    </div>

</div>

<!-- Form for 3 Ethernet (net_3_form) -->
<p></p>
<div id="net_3_form" style="display:none;">
    <!-- Virtual Switch to Ethernet 1 of 3 -->
    <div class="control-group">
        <label class="control-label" for="net_vsw3_1">Virtual Switch Ethernet 1:</label>
        <div class="controls">
            <select id="net_vsw3_1" name="net_vsw3_1" class="input-xlarge">
                <!-- list of virtual switches -->
                %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                %end
            </select>
        </div>
    </div>

    <!-- VLAN of Ethernet 1 of 3-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vlan3_1">VLAN Ethernet 1:</label>
        <div class="controls">
            <input id="net_vlan3_1" name="net_vlan3_1" type="number" min="1" placeholder="2000" class="input-mini" >
        </div>
    </div>

    <!-- Virtual Switch Ethernet 2 of 3-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vsw3_2">Virtual Switch Ethernet 2:</label>
        <div class="controls">
            <select id="net_vsw3_2" name="net_vsw3_2" class="input-xlarge">
                <!-- list of virtual switches -->
                %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                %end
            </select>
        </div>
    </div>

    <!-- VLAN of Ethernet 2 of 3-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vlan3_2">VLAN Ethernet 2:</label>
        <div class="controls">
            <input id="net_vlan3_2" name="net_vlan3_2" type="number" min="1" placeholder="2000" class="input-mini" >
        </div>
    </div>

    <!-- Virtual Switch to Deploy Ethernet 3 of 3-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vsw3_3">Virtual Switch Ethernet 3:</label>
        <div class="controls">
            <select id="net_vsw3_3" name="net_vsw3_3" class="input-xlarge">
                <!-- list of virtual switches -->
                %for vsw in virtual_switches:
                    <option>{{vsw}}</option>
                %end
            </select>
        </div>
    </div>

    <!-- VLAN Deploy (text) of Ethernet 3 of 3-->
    <p></p>
    <div class="control-group">
        <label class="control-label" for="net_vlan3_3">VLAN Ethernet 3:</label>
        <div class="controls">
            <input id="net_vlan3_3" name="net_vlan3_3" type="number" min="1" placeholder="2000" class="input-mini" >
        </div>
    </div>

</div>


<!-- END OF NETWORK FORM ##################################################### -->
<!-- Finish, goes to validation_lpar -->
<div class="control-group">
  <b><label class="control-label" for="next"></label></b>
  <div class="controls">
    <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
    <button id="next" name="next" class="btn btn-primary"> NEXT </button>
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
