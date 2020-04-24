let token = $('meta[name="csrf-token"]').attr('content');

$(document).ready(function () {

    $('#notification').addClass('act');


    $('#mail').click(function () {
        let values = $('#receiver').val();
        console.log(values);
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/notification',
            data: {
                'receiver': values,
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    alert('Mail sent');
                }
                else {
                    alert('Error!');
                }
            }
        });
    });
});