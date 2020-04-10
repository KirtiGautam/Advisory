let token = $('meta[name="csrf-token"]').attr('content');

$('#Role').addClass('act');

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


$(document).ready(function () {
    $('.edit').click(function () {
        search();
    });
});