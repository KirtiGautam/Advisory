$('#Mentor').addClass('act');

let token = $('meta[name="csrf-token"]').attr('content');

function set(id) {
    $('#class').val(id);
    search();
    return;
}

function deleteClass(id) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/delete-class',
        data: {
            'delete': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data.success) {
                $('tr#' + id).remove();
                alert("Class deleted")
            }
        }
    });
}

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

    $('#updateMentor').click(function () {
        $('#updateMentor').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-class',
            data: {
                'Mentor': $('#teachers').val(),
                'id': $('#class').val(),
                'department': $('#DOC').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    alert('Change successful');
                }
                $('#updateMentor').html('Update');
            }
        });
    });

    $('#addClass').click(function () {
        $('#addClass').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/create-class',
            data: {
                'section': $('#className').val(),
                'batch': $('#batch').val(),
                'Mentor': $('#mentor').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    if (data.created) {
                        $('#className').val('');
                        $('#batch').val('');
                        $('#mentor').val('');
                        let html = '<tr id="' + data.Class.id + '"><td>' + data.Class.section + ' (' + data.Class.batch + ')</td><td>' + data.Class.Mentor + '</td><td><button class="btn btn-info" data-toggle="modal" id="' + data.Class.id + '" onclick="set(this.id)" data-target="#edit" > Edit</button ></td ><td><button type="button" id="' + data.Class.id + '" onclick="deleteClass(this.id)" class="btn btn-danger">Delete</button></td></tr > ';
                        $('tbody').append(html);
                        alert('Classes updated');
                    } else {
                        alert('Class already exists')
                    }
                    $('#updateHod').html('Add');
                }
            }
        });
    });
});
