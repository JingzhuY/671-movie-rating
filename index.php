<?php

session_start();
unset($_SESSION['name']);


$_SESSSION['data'] = array();

$salt = 'XyZzy12*_';
$stored_hash = '64f4fba5160dd3a5be63f3ec3911359f';	// pw is si6712015

// error checking: to check whether user & pass are typed in 
if( isset($_POST['who']) && isset($_POST['pass'])){
	// if user or pass info is missing, error msg 
	if( strlen($_POST['who']) < 1 || strlen($_POST['pass']) < 1) {
		//$failure = "User ID and password are required";	 
		//Instead, redirect to the current page 
		header("Location: index.php");
		$_SESSION['error'] = "User ID and password are required";
		exit();
	}
	// if user and pass are not blank, check for the password by comparing to the stored hash. 
	elseif ((int)$_POST['who'] < 1 && (int)$_POST['who'] > 6041) {
		header("Location: index.php");
		$_SESSION['error'] = "User ID doesn't exist. Please check again.";
		exit();
	}
	else {
		$check = hash('md5', $salt.$_POST['pass']);
		if( $check == $stored_hash) {
			$_SESSION['name'] = $_POST['who'];
			// Redirect the browser to autos.php
			header("Location: data.php");
			exit();
		}	
		// when the md5 hash is not matching the stored hash, error msg
		else{
			//$failure = "Incorrect password";
			//redirect again
			$_SESSION['error'] = "Incorrect password";
			header("Location: index.php");
			exit();
		}
	}
}

?>

<!DOCTYPE html>
<html>
<head>
	<title>Movie Recommender</title>
</head>
<body style = "font-family: sans-serif;">

	<h1>Please Log In </h1>
	<?php
		if( isset($_SESSION['error'])) {
			echo '<p style = "color: red;">'.htmlentities($_SESSION['error'])."</p>";
			unset($_SESSION['error']);
		}
	?>
	<form method = "POST" action = "index.php">
		<label for = "nam">User ID</label>
		<input type = "text" name = "who" id = "nam"> <br>
		<label for = "id_1723">Password</label>
		<input type = "text" name = "pass" id = "id_1723"> <br>
		<input type = "submit" value = "Log In">
	</form> 
	<p>
		For a password hint, view source and find a password hint in the HTML comments.
		<!-- Hint: The password is the course number + year. -->
	</p>
	<!-- <p>
	Attempt to <a href = "data.php">Edit Address Book</a> without logging in. 
	</p>  -->
</body>
</html>
