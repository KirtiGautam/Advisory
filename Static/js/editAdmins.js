$('#editAdmin').addClass('act');

let token = $('meta[name="csrf-token"]').attr('content');

function setdep(i) {
    $('#dep').val(i);
    searchHOD();
    return;
}

function deleteDep(id) {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/delete-dep',
        data: {
            'delete': id,
        },
        dataType: 'json',
        success: function (data) {
            if (data.success) {
                $('tr#' + id).remove();
                alert("Department deleted")
            }
        }
    });
}


function searchHOD() {
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
            let html = '';
            for (let i = 0; i < data.teachers.length; i++)
                html += '<option value="' + data.teachers[i][1] + '">' + data.teachers[i][0] + ' (' + data.teachers[i][2] + ') ' + '</option>';
            $('#hods').html(html);
        }
    });
}

$(document).ready(function () {

    $('#updateHod').click(function () {

        let id = '#' + $('#dep').val();
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-hod',
            data: {
                'dept': $('#dep').val(),
                'id': $('#hods').children("option:selected").val(),
                'prev': $(id).children('td').eq(1).html().trim(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    alert('Hod updated');
                    $(id).children('td').eq(1).html(data.hod);
                }
            }
        });
    });

    $('#ad').click(function () {
        $('#add').show();
    });

    $('#addDep').click(function () {

        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-deps',
            data: {
                'dept': $('#depname').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    if (data.created) {
                        $('#depname').val('');
                        let html = " <tr id='" + data.deptid + "'><td>" + data.dept + "</td><td>" + data.deptHOD + "</td><td><button class='btn btn-info' data-toggle='modal' id='" + data.deptid
                            + "' onclick='setdep(this.id)' data-target='#edit'>Edit</button ></td><td><button type='submit' id='" + data.deptid + "' onclick='deleteDep(this.id)' class='btn btn-danger'>Delete</button></td></tr > ";
                        $('tbody').append(html);
                        alert('Departments updated');
                    } else {
                        alert('Department already exists')
                    }
                }
            }
        });
    });

});
