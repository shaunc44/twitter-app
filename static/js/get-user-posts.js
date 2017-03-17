$(document).ready(function(){

    Mustache.tags = [ '<%', '%>' ];

    $.ajax({
        url : '/getPostsByUser',
        method : 'GET',
        dataType: 'json',
        success: function(data){
            // MUSTACHE.JS
            var template = $("#tweetList").html();
            // console.log("Template: ", template);
            var render = Mustache.render(template, data);
            // console.log("Render: ", render);
            $(".list-group").html(render);
        },
        error: function(error){
            console.log(error);
        }
    });
});


// $(document).ready(function() {
//     $.ajax({
//         // calls getPostByUser method in app.py
//         url: '/getPostsByUser',
//         type: 'GET',
//         success: function(response) {
//             var div = $('<div>')
//                 .attr('class', 'list-group').append($('<a>')
//                 .attr('class', 'list-group-item active').append($('<h4>')
//                 .attr('class', 'list-group-item-heading'),$('<p>')
//                 .attr('class', 'list-group-item-text')));
//         },
//         error: function(error) {
//             console.log(error);
//         }
//     });
// });