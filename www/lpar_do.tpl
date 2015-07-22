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
<legend>RESULT</legend>
<p></p>
%if exec_lpar == 'yes':
    <p>File path: {{pahome}}/poweradm/changes/{{change_file}}</p>

    <b><p>The LPAR was created.</p></b>
    <p>Creation LOG:</p>
    % if mklog != 'none':
        % for log_line in mklog.splitlines():
            <div>{{log_line}}</div>
        %end
    %end

%else:
    <b><p>LPAR Creation <font color="#C80000">CANCELLED</font>.</p></b>

%end

</fieldset>
<!-- LPAR Configuration -->
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>

</DIV>
</HTML>
