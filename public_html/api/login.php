<?php
session_start();

$myfile = fopen("/tokens/" . $_POST['email'] . ".txt", "r") or die(json_encode('{
    "code": "0",
    "message": "Error opening file" 
}'));
$token =  fread($myfile, filesize("/tokens/" . $_POST['email'] . ".txt"));
if($_POST['token'] == $token){
    $_SESSION['email'] = $_POST['email'];
    echo $_POST['email'];
}
else {
    echo "nope";
}


