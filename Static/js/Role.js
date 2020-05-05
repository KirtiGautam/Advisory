let token = $('meta[name="csrf-token"]').attr('content');

function search(value = '') {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/get-teachers',
        data: {
            'term': value,
        },
        dataType: 'json',
        success: function (data) {
            let html = '';
            for (let i = 0; i < data.teachers.length; i++)
                html += '<option value="' + data.teachers[i].EID + '">' + data.teachers[i].full_name + ' (' + data.teachers[i].contact + ') ' + '</option>';
            $('.teachers').html(html);
        }
    });
}

function set(permission) {
    $('#perm').val(permission);
    search();
}

function removePerm(permission) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/remove-permission',
        data: {
            'permission': permission,
        },
        dataType: 'json',
        success: function (data) {
            console.log(data)
            if (data.success) {
                if (permission == 'can_upload_students') {
                    $("#CUS").find("td:eq(1)").text('None');
                } else {
                    $("#CAM").find("td:eq(1)").text('None');
                }
                alert('Permission removed')
            }
        }
    });
}


$(document).ready(function () {
    $('#Role').addClass('act');

    $('#updatePerm').click(function () {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-permission',
            data: {
                'permission': $('#perm').val(),
                'teach': $('.teachers').val(),
            },
            dataType: 'json',
            success: function (data) {
                console.log(data)
                if (data.success) {
                    if ($('#perm').val() == 'can_upload_students') {
                        $("#CUS").find("td:eq(1)").text(data.user);
                    } else {
                        $("#CAM").find("td:eq(1)").text(data.user);
                    }
                    alert('Permission added')
                }
            }
        });
    });
});