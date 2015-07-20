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
<form action="/lpar_config_sys_net" class="form-horizontal" method="GET">
<fieldset>


<!-- LPAR Configuration -->
<legend>LPAR Configuration</legend>
<p></p>
<!-- Change or Ticket number-->
<div class="control-group">
  <b><label class="control-label" for="change">Change or Ticket number:</label></b>
  <div class="controls">
    <input id="change" name="change" type="text" placeholder="TICKET0000" pattern="[a-zA-Z0-9]+" class="input-large" required="">
    <p class="help-block">Help: Insert change or ticket number.</p>
  </div>
</div>

<!-- LPAR Prefix -->
<div class="control-group">
  <b><label class="control-label" for="prefix">LPAR Prefix:</label></b>
  <div class="controls">
    <input id="prefix" name="prefix" type="text" placeholder="PREFIX" pattern="[a-zA-Z0-9]+" class="input-xlarge" required="">
    <p class="help-block">Help: Prefix is to identify the group of LPAR also DEV-MYLPAR. DEV is the prefix.</p>
  </div>
</div>

<!-- LPAR Name -->
<div class="control-group">
  <b><label class="control-label" for="lparname">LPAR Name:</label></b>
  <div class="controls">
    <input id="lparname" name="lparname" type="text" pattern="[a-zA-Z0-9]+" placeholder="myaixlpar" class="input-xlarge" required="">
    <p class="help-block">Help: The name of LPAR.</p>
  </div>
</div>

<!-- LPAR Entitled CPU desired -->
<div class="control-group">
  <b><label class="control-label" for="lparentcpu">LPAR Entitled CPU desired:</label></b>
  <div class="controls">
    <input id="lparentcpu" onkeyup="getCPU()" name="lparentcpu" type="number" mim="0.1" step="any" placeholder="0.4" class="input-mini" required="">
    <p class="help-block">Help: Entitled CPU. Example: 0.4 or 1.3</p>
  </div>
</div>

<!-- LPAR Virtual CPU desired -->
<div class="control-group">
  <b><label class="control-label" for="lparvcpu">LPAR Virtual CPU desired:</label></b>
  <div class="controls">
    <input id="lparvcpu" onkeyup="getCPU()" name="lparvcpu" type="number" min="1" placeholder="3" class="input-mini" required="">
    <p class="help-block">Help: Virtual CPU. Example: 3</p>
    <p><span id="cpu"></span></p>
  </div>

<!-- Verify if entitled is 10% of virtual cpu -->
<script type="text/javascript">
function getCPU() {
    var vcpu = document.getElementById("lparvcpu").value;
    var entcpu = document.getElementById("lparentcpu").value;
    var result = (entcpu*100)/vcpu
    if (result >= 10) {
        var msg = "";
        document.getElementById("next").disabled = false; 
    } else {
        var msg = "ERROR: It's necessary that CPU Entitled is at least 10% of the Virtual";
        document.getElementById("next").disabled = true;
    };
    document.getElementById("cpu").innerHTML = msg;
}
</script>
</div>

<!-- LPAR Memory desired -->
<div class="control-group">
  <b><label class="control-label" for="lparmem">LPAR Memory desired:</label></b>
  <div class="controls">
    <input id="lparmem" name="lparmem" type="number" min="1" placeholder="10" class="input-mini" required="">
    <p class="help-block">Help: Memory Size (without GB)</p>
  </div>
</div>


<!-- Finish, goes to lpar_config_deploy -->
<div class="control-group">
  <b><label class="control-label" for="next"></label></b>
  <div class="controls">
    <INPUT Type="button" VALUE="BACK" onClick="history.go(-1);return true;">
    <button id="next" name="next" class="btn btn-primary">NEXT</button>
  </div>
</div>

</fieldset>
</form>
<P></P>
<P><A HREF="/">Back to home</A></P>
<P></P>
</CODE>

</DIV>
</BODY>
</HTML>
