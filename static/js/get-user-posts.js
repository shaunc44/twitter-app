$(document).ready(function() {
    $.ajax({
        url: '/getPostsByUser',
        type: 'GET',
        success: function(response) {
            var div = $('<div>')
                .attr('class', 'list-group').append($('<a>')
                .attr('class', 'list-group-item active').append($('<h4>')
                .attr('class', 'list-group-item-heading'),$('<p>')
                .attr('class', 'list-group-item-text')));
        },
        error: function(error) {
            console.log(error);
        }
    });
});