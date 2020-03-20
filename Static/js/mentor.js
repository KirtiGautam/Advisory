function set(id) {
    $('#class').val(id);
    search();
    return;
}

function deleteClass(id) {
    let token = $('meta[name="csrf-token"]').attr('content');
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
    let token = $('meta[name="csrf-token"]').attr('content');
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

    $('#addClass').click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
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
                        let html = '<tr id="' + data.Class.id + '"><td>' + data.Class.section + ' (' + data.Class.batch + ')</td><td>' + data.Class.Mentor + '</td><td><button class="btn btn-info" data-toggle="modal" id="' + data.Class.id + '" onclick="set(this.id)" data - target="#edit" > Edit</button ></td ><td><button type="button" id="' + data.Class.id + '" onclick="deleteClass(this.id)" class="btn btn-danger">Delete</button></td></tr > ';
                        $('tbody').append(html);
                        alert('Classes updated');
                    } else {
                        alert('Class already exists')
                    }
                }
            }
        });
    });
});
