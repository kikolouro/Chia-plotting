function login(user, password) {
    $.ajax({

        url: "http://localhost:5000/register",
        type: 'POST',
        dataType: 'JSON',
        data: {
            user: user,
            password: password
        },
        success: function (response) {

                alert(response)


        }
    });


}
