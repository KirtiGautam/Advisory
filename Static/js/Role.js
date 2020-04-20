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
                html += '<option value="' + data.teachers[i][1] + '">' + data.teachers[i][0] + ' (' + data.teachers[i][2] + ') ' + '</option>';
            $('.teachers').html(html);
        }
    });
}

function set(permission) {
    $('#perm').val(permission);
    search();
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
                if(data.success){
                    alert('Permission added')
                }
            }
        });
    });
});