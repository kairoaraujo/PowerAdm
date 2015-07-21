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

%if deploy_lpar == 'y':
    <fieldset>
    <legend>RESULT</legend>
    <p></p>
    <p>Server file: {{deploy_file}}</p>

    <b><p>The LPAR Deployed.</p></b>
    <p>Creation LOG:</p>
    % for log_line in mklog.splitlines():
        <div>{{log_line}}</div>
    %end

    <b><p>Please finish the OS installation.</p></b>
    <div>1. Access the HMC Server</div>
    <div>2. Open the terminal console</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;mkvterm -m {{lparframe}} -p {{lparprefix}}-{{lparname}}</div>
    <div>&nbsp;&nbsp;&nbsp;&nbsp;TIP: Maybe you need press '1 Enter'
    </fieldset>
    <p><p>
    <fieldset>
    <legend>Deploy informations</legend>
    <div><b>LPAR Name: </b>{{lparprefix}}-{{lparname}}</div>
    <div><b>OS Version: </b>{{os_version}}</div>
    <div><b>NIM Server: </b>{{nimsrv}}</div>
    <div><b>NIM IP: </b>{{nim_ipdeploy}}</div>
    </fieldset>



%else:
<fieldset>
<legend>RESULT</legend>


    <b><p>LPAR deploy <font color="#C80000">CANCELLED</font>.</p></b>

</fieldset>

%end

<!-- LPAR Configuration -->
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
</CODE>

</DIV>
</BODY>
</HTML>
