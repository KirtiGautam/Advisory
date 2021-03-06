let token = $('meta[name="csrf-token"]').attr('content');

function deleteSubject(id) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/delete-subject',
        data: {
            'id': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data.success) {
                $('tr#' + id).remove();
                alert('Subject removed successfully');
            }
        }
    });
}

$(document).ready(function () {

    $('#subjects').addClass('act');

    $('#addSubjects').click(function () {
        $('#addSubjects').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/add-subject',
            data: {
                'sub_code': $('#sub_code').val(),
                'Name': $('#Name').val(),
                'credits': $('#credits').val(),
                'department': $('#Departments').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    html = '<tr id="' + $('#sub_code').val() + '"><td>' + $('#sub_code').val() + '</td><td>' + $('#Name').val();
                    html += (data.superuser) ? '</td><td>' + data.department + '</td>' : '</td>';
                    html += '<td><button type="submit" class="btn btn-danger" id="' + $('#sub_code').val() + '" onclick="deleteSubject(this.id)">Delete</button></td></tr>';
                    $('tbody').append(html);
                    $('#credits').val('');
                    $('#sub_code').val('');
                    $('#Name').val('');
                    $('#ETR').hide();
                    alert('Subject added successfully');
                } else {
                    alert(data.message);
                }
                $('#addSubjects').html('Add');
            }
        });
    });
});


