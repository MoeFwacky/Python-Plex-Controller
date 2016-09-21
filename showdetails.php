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
$cmd = str_replace("%20"," ",$cmd);
$db = new SQLite3($mydb);
$query = 'SELECT * FROM TVshowlist WHERE TShow Like \''.$cmd.'\'';
$results = $db->query($query);
while ($row = $results->fetchArray()){
#var_dump($row);
echo "Show: ".$row["TShow"]."<br>";
echo "Genre: ".$row["Genre"]."<br>";
echo "Rated: ".$row["Rating"]."<br>";
echo "Summary: ".$row["Summary"]."<br>";
}
?>
<br><br>
<h4>Quick Commands</h4>
<FORM action = "showdetails.php?title=<?php echo $cmd;?>" method = "post">
<TABLE>
<TR>
	<TD><button TYPE = "Submit" VALUE = "setupnext" NAME = "command">Set Up Next</button>
	<TD><button TYPE = "Submit" VALUE = "queueadd" NAME = "command">Add to Queue</button>
	<TD><button TYPE = "Submit" VALUE = "nextep" NAME = "command">Next Episode</button>
        <TD><button TYPE = "Submit" VALUE = "playme" NAME = "command">Play Now</button>
</TR>
</TABLE>
<?php
if (isset($_POST['command']))
{
$command = $_POST['command'];
?>
<div style="width:500px;">
<?php
echo ("You entered ".$command." ".$cmd."<br><br>");
$runme = $precmd.$command." \"".$cmd."\"";
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
