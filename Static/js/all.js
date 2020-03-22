//Data Upload
$(document).ready(function () {

    $("#upload").click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
        var fileUpload = document.getElementById("data").files[0];
        var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
        if (regex.test(document.getElementById("data").value.toLowerCase())) {
            if (typeof (FileReader) != "undefined") {
                var reader = new FileReader();
                reader.onload = (function (fileUpload) {
                    return function (e) {
                        let table = [];
                        let rows = e.target.result.split("\n");
                        for (var i = 1; i < rows.length; i++) {
                            var cells = rows[i].split(",");
                            if (cells.length > 1) {
                                table.push({
                                    'full_name': cells[0],
                                    'gender': cells[1],
                                    'email': cells[2],
                                    'contact': cells[3],
                                    'department': cells[4].replace('\r', ''),
                                });
                            }
                        }
                        $.ajax({
                            type: "POST",
                            headers: { "X-CSRFToken": token },
                            url: '/uploadt-data',
                            data: {
                                'tdata': JSON.stringify(table),
                            },
                            dataType: 'json',
                            success: function (data) {
                                if (data.success) {
                                    alert('File upload success');
                                }
                            }
                        });
                    };
                })(fileUpload)
                reader.readAsText(fileUpload);
            } else {
                alert("This browser does not support HTML5.");
            }
        }
    });

});

//Edit Admins
function setdep(i) {
    $('#dep').val(i);
    searchHOD();
    return;
}

function deleteDep(id) {
    let token = $('meta[name="csrf-token"]').attr('content');
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
                            + "' onclick='setdep(this.id)' data-target='#edit'>Edit</button ></td><td><button type='submit' id='"+ data.deptid +"' onclick='deleteDep(this.id)' class='btn btn-danger'>Delete</button></td></tr > ";
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


//Login
function check(){
    $('p').remove();
    if(document.getElementById('username').value==''){
        $('.userd').append('<p><br />Username required</p>');
        $('#username').focus();
        return false;
    }
    if(document.getElementById('password').value==''){
        $('.passd').append('<p>Password required</p>');
        $('#password').focus();
        return false;
    }
    if(document.getElementById('password').value.length<8){
        $('.passd').append('<p>Password cannot be less than 8 characters<p>');
        $('#password').focus();
        return false;
    }
    return true;
}

//Mentor
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
                        let html = '<tr id="' + data.Class.id + '"><td>' + data.Class.section + ' (' + data.Class.batch + ')</td><td>' + data.Class.Mentor + '</td><td><button class="btn btn-info" data-toggle="modal" id="' + data.Class.id + '" onclick="set(this.id)" data-target="#edit" > Edit</button ></td ><td><button type="button" id="' + data.Class.id + '" onclick="deleteClass(this.id)" class="btn btn-danger">Delete</button></td></tr > ';
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



//Navbar
(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

//Role
// function search() {
//     let token = $('meta[name="csrf-token"]').attr('content');
//     $.ajax({
//         type: "POST",
//         headers: { "X-CSRFToken": token },
//         url: '/get-teachers',
//         data: {
//             'term': $('#search').val(),
//         },
//         dataType: 'json',
//         success: function (data) {
//             let html = '';
//             for (let i = 0; i < data.teachers.length; i++)
//                 html += '<option value="' + data.teachers[i][1] + '">' + data.teachers[i][0] + ' (' + data.teachers[i][2] + ') ' + '</option>';
//             $('#teachers').html(html);
//         }
//     });
// }

$(document).ready(function () {
    $('.edit').click(function () {
        search();
    });
});


//Settings
$(document).ready(function () {

    $('#gucci').click(function () {
        $('#pass').show();
    });

    $('#change').click(function (e) {
        e.preventDefault();
        let token = $('meta[name="csrf-token"]').attr('content');
        if ($('#new').val() == '' ||
            $('#renew').val() == '' ||
            $('#pre').val() == '') {
            alert('Please Fill all values');
            return;
        } else if ($('#new').val().length < 8) {
            alert('Passwords cannot be shorter than 8 characters');
            return;
        } else if ($('#new').val() == $('#pre').val()) {
            alert('New Password cannot be same as current');
            return;
        } else if ($('#new').val() !=
            $('#renew').val()) {
            alert("Passwords don't match");
            return;
        }
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/change-password',
            data: {
                'password': $('#new').val(),
                'pre': $('#pre').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.Changed) {
                    alert("Password Changed");
                }
                else{
                    alert("Invalid Current Password")
                }
            }
        });
        $('#new').val('');
        $('#renew').val('');
        $('#pre').val('');
    });
});