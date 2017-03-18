$(document).ready(function(){

    // MUSTACHE.JS
    Mustache.tags = [ '<%', '%>' ];

    $.ajax({
        url : '/getPostsByUser',
        method : 'GET',
        dataType: 'json',
        success: function(data){
            // MUSTACHE.JS
            // Username display
            var usernameTemplate = $("#username-header-scrpt").html();
            var usernameRender = Mustache.render(usernameTemplate, data);
            $("#username-header-html").html(usernameRender);
            // Tweets diplay
            var tweetsTemplate = $("#tweetList").html();
            var tweetsRender = Mustache.render(tweetsTemplate, data);
            $(".list-group").html(tweetsRender);

        },
        error: function(error){
            console.log(error);
        }
    });

});
