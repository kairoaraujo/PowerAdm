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

<form action="/deploy_do" class="form-horizontal" method="GET">
<fieldset>


<!-- LPAR Configuration -->
<legend>LPAR Deploy</legend>

<p></p>
% if deploy_list == []:
    <p>Not LPAR with NIM Deploy enabled available to execute.</p>
    <P></P>
    <div class="control-group">
        <b><label class="control-label" for="next"></label></b>
        <div class="controls">
            <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
        </div>
    </div>


% else:
    <div class="control-group">
        <b><label class="control-label" for="deploy_file">Select LPAR NIM:</label></b>
        <div class="controls">
            <select id="deploy_file" name="deploy_file" class="input-xlarge">
                %for file in deploy_list:
                    <option>{{file}}</option>
                %end
            </select>
        </div>
    </div>
    <p></p>
    <div class="control-group">
        <b><label class="control-label" for="os_version">Select OS Version</label></b>
        <div class="controls">
            <select id="os_version" name="os_version" class="input-xlarge">
                %for os_version in os_list:
                    <option>{{os_version}}</option>
                %end
            </select>
        </div>
    </div>
    <p></p>
    <div class="control-group">
        <b><label class="control-label" for="nimsrv">Select NIM Serer to be used</label></b>
        <div class="controls">
            <select id="nimsrv" name="nimsrv" class="input-xlarge">
                %for nimsrv in nimsrv_list:
                    <option>{{nimsrv}}</option>
                %end
            </select>
        </div>
    </div>

    <p></p>
    <b><label class="control-label" for="deploy_lpar">Do you want execute deploy?</label></b>
    <div class="controls">
        <b><label class="radio" for="deploy_lpar_yes">
        <input type="radio" name="deploy_lpar" id="exec_lpar_yes" value="y">
        yes
        </label></b>
        <b><label class="radio" for="deploy_lpar_no">
        <input type="radio" name="deploy_lpar" id="exec_lpar_no" value="n" checked="checked">
        no
        </label></b>
    </div>

    <P></P>
    <div class="control-group">
        <b><label class="control-label" for="next"></label></b>
        <div class="controls">
            <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
            <button id="next" name="next" class="btn btn-primary"> CONFIRM </button>
        </div>
    </div>
</fieldset>
%end
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
</CODE>

</DIV>
</BODY>
</HTML>
