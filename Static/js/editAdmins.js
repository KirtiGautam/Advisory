function set(i) {
    $('#dep').val(i);
    search();
    return;
}

function search() {
    let token = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/get-hods',
        data: {
            'dept': $('#dep').val(),
            'term': $('#search').val(),
        },
        dataType: 'json',
        success: function (data) {
            html = '';
            for (let i = 0; i < data.hods.length; i++)
                html += '<option value="' + data.hods[i][0] + '">' + data.hods[i][0] + '</option>';
            $('#hods').html(html);
        }
    });
}

$(document).ready(function () {
    $('#updateHod').click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
        let id = '#' + $('#dep').val();
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-hod',
            data: {
                'dept': $('#dep').val(),
                'name': $('#hods').children("option:selected").val(),
                'prev': $(id).children('td').eq(1).html().trim(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    alert('Hod updated');
                    $(id).children('td').eq(1).html($('#hods').children("option:selected").val());
                }
            }
        });
    });

    $('#ad').click(function () {
        $('#add').show();
    });

});