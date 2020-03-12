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
            let html = '';
            for (let i = 0; i < data.teachers.length; i++)
                html += '<option value="' + data.teachers[i][1] + '">' + data.teachers[i][0] + ' (' + data.teachers[i][2] + ') ' + '</option>';
            $('#hods').html(html);
        }
    });
}

$(document).ready(function () {

    $('#editAdmin').addClass('active');

    $('#updateHod').click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
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
        let token = $('meta[name="csrf-token"]').attr('content');
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
                            + "' onclick='set(this.id)' data-target='#edit'>Edit</button ></td></tr >";
                        $('tbody').append(html);
                        alert('Departments updated');
                    }else{
                        alert('Department already exists')
                    }
                }
            }
        });
    });

});