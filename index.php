<html>
<title>TBN Plex Web Controller</title>
<style>
body {
background-color: black;
color: white;
text-alight:center;
}
</style>
<center>
<body>
<div style="width:500px;">
<img src="plex.jpg" alt="Plex"style="float:left;width:75px;height:75px;"></img>
<h3>TBN Plex Web Controller</h3></div>
<?php 
$precmd = "python /home/pi/hasystem/system.py ";
$mydb = "/home/pi/hasystem/myplex.db";

#$cmd1 = $precmd."nowplaying";
#$out1 = shell_exec($cmd1);
#echo ("Now playing: ".$out1.".<br>");
?>
<br>
<h4>Quick Command Console</h4>
<FORM action = "index.php" method = "post">
<TABLE>
<TR>
	<TD><button TYPE = "Submit" VALUE = "whatupnext" NAME = "command">What Up Next</button>
	<TD><button TYPE = "Submit" VALUE = "queueshow" NAME = "command">Queue Show</button>
	<TD><button TYPE = "Submit" VALUE = "whereat" NAME = "command">Where At</button>
	<TD><button TYPE = "Submit" VALUE = "skipthat" NAME = "command">Skip That</button>
</TR>
<TR>
	<TD><INPUT TYPE = "Submit" VALUE = "stopplayback" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "pauseplayback" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "skipback" NAME = "command">
	<TD><INPUT TYPE = "Submit" VALUE = "skipahead" NAME = "command">
</TR>
<TR>
        <TD><INPUT TYPE = "Submit" VALUE = "muteaudio" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "unmuteaudio" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "getplaymode" NAME= "command">
	<TD><INPUT TYPE = "Submit" VALUE = "explainblock" NAME = "command">
</TR>
<TR>
        <TD><INPUT TYPE = "Submit" VALUE = "suggestmovie" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "suggesttv" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "whatispending" NAME = "command">
	<TD><INPUT TYPE = "Submit" VALUE = "addsuggestion" NAME = "command">
</TR>
</TABLE>
</FORM>
<h4>Manual Control -------------- Querry Database</h4>
<form action = "index.php" method = "post">
<INPUT TYPE = "Text" VALUE ="" NAME = "mcommand">
<INPUT TYPE = "Submit" name = "commandsubmit" value = "Go"/>
<form action = "index.php" method = "post">
     
<INPUT TYPE = "Text" VALUE ="" NAME = "dbcommand">
<INPUT TYPE = "Submit" name = "submit" value = "Go"/>
<br>
<?php
if ((!isset($_POST['submit'])) and (!isset($_POST['commandsubmit'])) and (!isset($_POST['command'])))
{
echo ("Enter a command to proceed.<br>");
}
else
{
if (isset($_POST['command']))
{
$command = $_POST['command'];
?>
<div style="width:500px;">
<?php
echo ("You entered ".$command.".<br><br>");
$runme = $precmd.$command;
$output = shell_exec($runme);
}

if (isset($_POST['commandsubmit'])) 
{
$command = $_POST["mcommand"];
?>
<div style="width:500px;">
<?php
echo ("You entered ".$command.".<br><br>");
$runme = $precmd.$command;
$output = shell_exec($runme);
}
elseif (isset($_POST['submit']))
{
$db = new SQLite3($mydb);
$command = $_POST['dbcommand'];
if (strpos($command, "moviedetails") !==false){
$cmd = explode("moviedetails ", $command);
$cmd = $cmd[1];
$cmd = str_replace("\"","",$cmd);
$query = 'SELECT * FROM Movies WHERE Movie Like \''.$cmd.'\'';
$results = $db->query($query);
while ($row = $results->fetchArray()){
#var_dump($row);
echo "Movie: ".$row["Movie"]."<br>";
echo "Tagline: ".$row["Tagline"]."<br>";
echo "Genre: ".$row["Genre"]."<br>";
echo "Starring: ".$row["Actors"]."<br>";
echo "Directed by: ".$row["Director"]."<br>";
echo "Rated: ".$row["Rating"]."<br>";
echo "Summary: ".$row["Summary"]."<br>";

}
}
elseif (strpos($command, "showdetails") !==false){
$cmd = explode("showdetails ", $command);
$cmd = $cmd[1];
$cmd = str_replace("\"","",$cmd);
$query = 'SELECT * FROM TVshowlist WHERE TShow Like \''.$cmd.'\'';
$results = $db->query($query);
while ($row = $results->fetchArray()){
#var_dump($row);
echo "Show: ".$row["TShow"]."<br>";
echo "Genre: ".$row["Genre"]."<br>";
echo "Rated: ".$row["Rating"]."<br>";
echo "Summary: ".$row["Summary"]."<br>";
}
}
elseif (strpos($command, "findmovie") !==false){
$cmd = explode("findmovie ", $command);
$cmd = $cmd[1];
$cmd = str_replace("\"","",$cmd);
$query = 'SELECT Movie FROM Movies WHERE Movie Like \'%'.$cmd.'%\'';
$results = $db->query($query);
echo ("Movies found containing \"".$cmd."\"<br><br>");
while ($row = $results->fetchArray()){
#var_dump($row);
$link = str_replace(" ","%20",$row["Movie"]);
echo "Movie: <a href=moviedetails.php?title=".$link.">".$row["Movie"]."</a><br>";
}
}
elseif (strpos($command, "findshow") !==false){
$cmd = explode("findshow ", $command);
$cmd = $cmd[1];
$cmd = str_replace("\"","",$cmd);
$query = 'SELECT TShow FROM TVshowlist WHERE TShow Like \'%'.$cmd.'%\'';
$results = $db->query($query);
echo ("Movies found containing \"".$cmd."\"<br><br>");
while ($row = $results->fetchArray()){
#var_dump($row);
$link = str_replace(" ","%20",$row["TShow"]);
echo "Show: <a href=showdetails.php?title=".$link.">".$row["TShow"]."</a><br>";
}
}
elseif (strpos($command, "listmovies") !==false){
$query = 'SELECT Movie FROM Movies';
$results = $db->query($query);
echo ("Movies found containing \"".$cmd."\"<br><br>");
while ($row = $results->fetchArray()){
#var_dump($row);
$link = str_replace(" ","%20",$row["Movie"]);
echo "Movie: <a href=moviedetails.php?title=".$link.">".$row["Movie"]."</a><br>";
}
}
elseif (strpos($command, "listshows") !==false){
$query = 'SELECT TShow FROM TVshowlist';
$results = $db->query($query);
echo ("Movies found containing \"".$cmd."\"<br><br>");
while ($row = $results->fetchArray()){
#var_dump($row);
$link = str_replace(" ","%20",$row["TShow"]);
echo "Show: <a href=showdetails.php?title=".$link.">".$row["TShow"]."</a><br>";
}
}

$output = "<br>Done<br>";
}
$output = str_replace("\n","<br>",$output);
echo ($output."<br>");
}
?></div>

</body>
