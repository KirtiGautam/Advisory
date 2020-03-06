$(document).ready(function () {
    $('#settings').addClass('active');

    $('#gucci').click(function () {
        $('#pass').show();
    });

    $('#change').click(function (e) {
        e.preventDefault();
        let token = $('meta[name="csrf-token"]').attr('content');
        if ($('#new').val() == '' ||
            $('#renew').val() == '' ||
            $('#pre').val() == '') {
            alert('Please Fill all values');
            return;
        } else if ($('#new').val().length < 8) {
            alert('Passwords cannot be shorter than 8 characters');
            return;
        } else if ($('#new').val() == $('#pre').val()) {
            alert('New Password cannot be same as current');
            return;
        } else if ($('#new').val() !=
            $('#renew').val()) {
            alert("Passwords don't match");
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/change-password',
            data: {
                'password': $('#new').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.Changed) {
                    alert("Password Changed");
                }
            }
        });
        $('#new').val('');
        $('#renew').val('');
        $('#pre').val('');
    });
});