$(document).ready(function(){
    $.ajax({
        url : '/getPostsByUser',
        type : 'GET',
        success: function(response){
            var div = $('<div>').attr('class', 'list-group').append($('<a>').attr('class', 'list-group-item active').append($('<h4>').attr('class', 'list-group-item-heading'),
                $('<p>').attr('class', 'list-group-item-text')));

            var postsObj = JSON.parse(response);
            var posts = '';

            $.each(postsObj,function(index, value){
                posts = $(div).clone();
                $(posts).find('h4').text(value.Title);
                $(posts).find('p').text(value.Text);
                $('.list-group').append(posts);
            });
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