$(document).ready(function() {
    $('#login-register').click(function(){
        $.ajax({
            url: '/logIn',
            data: $('form').serialize(),
            type: 'POST',
            /* should i change/delete the success: and error: messages ?? */
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});