$(document).ready(function() {
    $('#login-register').click(function(){
        $.ajax({
            url: '/showHomePage',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});