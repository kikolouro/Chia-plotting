function register(email, password) {
    console.log("adad")
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
                window.location = "index.php?message=" + response.message
            } 
        },
        error: function (response) {
            alert(JSON.stringify(response))
        }
    });


}
