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
<?php
$precmd = "python /home/pi/hasystem/system.py ";
$mydb = "/home/pi/hasystem/myplex.db";
$cmd = $_GET["title"];
$db = new SQLite3($mydb);
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
?>
<br><br>
<h4>Quick Commands</h4>
<FORM action = "moviedetails.php?title=<?php echo $cmd;?>" method = "post">
<TABLE>
<TR>
        <TD><INPUT TYPE = "Submit" VALUE = "setupnext" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "queueshow" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "whereat" NAME = "command">
        <TD><INPUT TYPE = "Submit" VALUE = "skipthat" NAME = "command">
</TR>
</TABLE>
<?php
if (isset($_POST['command']))
{
$command = $_POST['command'];
?>
<div style="width:500px;">
<?php
echo ("You entered ".$command.".<br><br>");
$runme = $precmd.$command." ".$cmd;
$output = shell_exec($runme);
echo $output;
?>
<meta http-equiv="location" content="http://index.php/" />
<?php
}
?>
<br><a href="index.php">Go Home</a><br>
</div>
</body>
