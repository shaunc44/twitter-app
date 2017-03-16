$(document).ready(function(){
    $('#fileupload').fileupload({
        url: 'upload',
        dataType: 'json',
        add: function (e, data) {
            data.submit();
        },
        success:function(response,status) {
        console.log(response.filename);
        var filePath = 'static/Uploads/' + response.filename;
        $('#imgUpload').attr('src',filePath);
        $('#filePath').val(filePath);
            console.log('success');
        },
        error:function(error){
            console.log(error);
        }
    });
})





// $(document).ready(function() {
//     $('#btnSignUp').click(function(){
//         $.ajax({
//             url: '/signUp',
//             data: $('form').serialize(),
//             type: 'POST',
//             success: function(response) {
//                 console.log(response);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
//     });
// });

