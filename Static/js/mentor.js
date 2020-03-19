function set(id) {
    $('#class').val(id);
    search();
    return;
}

function search() {
    let token = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/get-teachers',
        data: {
            'term': $('#search').val(),
        },
        dataType: 'json',
        success: function (data) {
            let html = '';
            for (let i = 0; i < data.teachers.length; i++)
                html += '<option value="' + data.teachers[i][1] + '">' + data.teachers[i][0] + ' (' + data.teachers[i][2] + ') ' + '</option>';
            $('#teachers').html(html);
        }
    });
}

$(document).ready(function () {
    $('#Mentor').addClass('active');

    $('#updateMentor').click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-class',
            data: {
                'Mentor': $('#teachers').val(),
                'id': $('#class').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    alert('Change successful');
                }
            }
        });
    });
});
