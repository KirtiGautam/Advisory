let token = $('meta[name="csrf-token"]').attr('content');

function preview(input, targ) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(targ)
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function () {
    $('#settings').addClass('act');

    $('#UAP').click(function () {
        $('#UAP').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        let formdata = new FormData();
        formdata.append('avatar', $('#UserP').prop('files')[0]);
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/user-pic',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {
                if (data.success) {
                    let model = JSON.parse(data.user);
                    console.log(model)
                    $('#UserPic').attr('src', '/Media/' + model[0].fields.avatar);
                    $('.avatar').attr('src', '/Media/' + model[0].fields.avatar);
                    alert('Success');
                }
                else {
                    alert('Incorrect details');
                }
                $('#UAP').html('Upload Pic');
            }
        });
    });

    $('#gucci').click(function () {
        $('#pass').show();
    });

    $('#change').click(function (e) {
        e.preventDefault();
        let ne = $('#new').val(), rene = $('#renew').val(), pre = $('#pre').val();        
        $('#new').val('');
        $('#renew').val('');
        $('#pre').val('');
        if (ne == '' ||
            rene == '' ||
            pre == '') {
            alert('Please Fill all values');
            return;
        } else if (ne.length < 8) {
            alert('Passwords cannot be shorter than 8 characters');
            return;
        } else if (ne == $('#pre').val()) {
            alert('New Password cannot be same as current');
            return;
        } else if (ne !=
            rene) {
            alert("Passwords don't match");
            return;
        }
        $('#change').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/change-password',
            data: {
                'password': ne,
                'pre': $('#pre').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.Changed) {
                    alert("Password Changed");
                }
                else {
                    alert("Invalid Current Password")
                }
                $('#change').html('Change Password');
            }
        });
    });
});
