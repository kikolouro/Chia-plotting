function register(email, password) {
    $.ajax({

        url: "http://localhost:5000/register",
        type: 'POST',
        dataType: 'JSON',
        data: {
            email: email,
            password: password
        },
        success: function (response) {
            if (response.code == 0) {
                window.location = "index.php?error=" + response.message
            }
            else if (response.code == 1) {
                window.location = "index.php?message=" + response.message
            }
        },
        error: function (response) {
            alert(JSON.stringify(response))
        }
    });


}

function login(email, password){
    $.ajax({

        url: "http://localhost:5000/login",
        type: 'POST',
        dataType: 'JSON',
        data: {
            email: email,
            password: password
        },
        success: function (response) {
            if (response.code == 0) {
                window.location = "index.php?error=" + response.message
            }
            else if (response.code == 1) {
                
                xmlhttp.onreadystatechange = () => {
                    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                        aux = xmlhttp.responseText;
                        if (window.XMLHttpRequest) {
                            xmlhttp = new XMLHttpRequest();
                        } else {
                            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                        }
                        xmlhttp.onreadystatechange = () => {
                            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                                alert(response)
                                window.location.replace("index.php");
                            }
                            else {
                                console.error("erro")
                            }
                        }
                        xmlhttp.open("POST", "api/login.php", true);
                        xmlhttp.setRequestHeader("Content-Type", "application/json")
                        xmlhttp.send(JSON.stringify(response))
                    }
                }
            }
        },
        error: function (response) {
            alert(JSON.stringify(response))
        }
    });
} 