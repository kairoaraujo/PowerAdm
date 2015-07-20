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

<form action="/lpar_do" class="form-horizontal" method="GET">
<fieldset>


<!-- LPAR Configuration -->
<legend>LPAR Creation</legend>

<p></p>
% if change_files == 'none':
    <p>No changes/tickets available to execute.</p>

% else:
    <div class="control-group">
        <b><label class="control-label" for="change_file">Select change/ticket to execute:</label></b>
        <div class="controls">
            <select id="change_file" name="change_file" class="input-xlarge">
                %for file in change_files:
                    <option>{{file}}</option>
                %end
            </select>
        </div>
    </div>
    <p></p>
    <b><label class="control-label" for="exec_lpar">Do you want execute this change/ticket?</label></b>
    <div class="controls">
        <b><label class="radio" for="exec_lpar_yes">
        <input type="radio" name="exec_lpar" id="exec_lpar_yes" value="yes">
        yes
        </label></b>
        <b><label class="radio" for="exec_lpar_no">
        <input type="radio" name="exec_lpar" id="exec_lpar_no" value="no" checked="checked">
        no
        </label></b>
    </div>
%end

<P></P>
<div class="control-group">
  <b><label class="control-label" for="next"></label></b>
  <div class="controls">
    <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
    <button id="next" name="next" class="btn btn-primary"> CONFIRM </button>
  </div>
</div>
</fieldset>
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
</CODE>

</DIV>
</BODY>
</HTML>
