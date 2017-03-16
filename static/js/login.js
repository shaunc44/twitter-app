$(document).ready(function() {
    $('#login-register').click(function(){
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            /* 
            1. should i change/delete the success: and error: messages ?? 
            2. maybe i need to POST ajax request to post new usernames and, 
            3. a GET ajax request to get existing username and related posts
            */
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});