//Navbar

function SlideMenu() {
    if (document.getElementById('menu').style.width == '250px') {
        document.getElementById('menu').style.width = '0';
        document.getElementById('content').style.marginLeft = '0';
    }

    else {
        document.getElementById('menu').style.width = '250px';
        document.getElementById('content').style.marginLeft = '250px';
    }
}

function closeSlideMenu() {
    document.getElementById('menu').style.width = '0';
    document.getElementById('content').style.marginLeft = '0';
}


//Data Upload
$(document).ready(function () {

    $("#upload").click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
        Papa.parse(document.getElementById("data").files[0], {
            header: true,
            complete: function (results) {
                console.log(results.data);
                let inlength = Object.keys(results.data[0]).length;
                for (let i = 0; i < results.data.length; i++) {
                    if (Object.keys(results.data[i]).length != inlength)
                        results.data.splice(i,1);
                }
                console.log(results.data);
                $.ajax({
                    type: "POST",
                    headers: { "X-CSRFToken": token },
                    url: '/uploadt-data',
                    data: {
                        'tdata': JSON.stringify(results.data),
                        'model': $('#uptype').val(),
                    },
                    dataType: 'json',
                    success: function (data) {
                        if (data.success) {
                            alert('File upload success');
                        }
                    }
                });
            }
        });
        // var fileUpload = document.getElementById("data").files[0];
        // var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.csv|.txt)$/;
        // if (regex.test(document.getElementById("data").value.toLowerCase())) {
        //     if (typeof (FileReader) != "undefined") {
        //         var reader = new FileReader();
        //         reader.onload = (function (fileUpload) {
        //             return function (e) {
        //                 let table = [];
        //                 console.log(e.target.result);
        //                 let rows = e.target.result.split("\n");
        //                 let keys = rows[0].split(",");
        //                 for (var i = 1; i < rows.length; i++) {
        //                     var cells = rows[i].split(",");
        //                     if (cells.length > 1) {
        //                         let temp = {};
        //                         for (let j = 0; j < cells.length; j++) {
        //                             console.log([keys[j], cells[j]])
        //                             // if (cells[j] != null)
        //                             //     temp[keys[j].replace('\r', '')] = cells[j].replace('\r', '');
        //                             // else
        //                             //     temp[keys[j].replace('\r', '')] = null; 
        //                         }
        //                         table.push(temp);
        //                     }
        //                 }
        //                 console.log(table);
        //                 // $.ajax({
        //                 //     type: "POST",
        //                 //     headers: { "X-CSRFToken": token },
        //                 //     url: '/uploadt-data',
        //                 //     data: {
        //                 //         'tdata': JSON.stringify(table),
        //                 //         'model': $('#uptype').val(),
        //                 //     },
        //                 //     dataType: 'json',
        //                 //     success: function (data) {
        //                 //         if (data.success) {
        //                 //             alert('File upload success');
        //                 //         }
        //                 //     }
        //                 // });
        //             };
        //         })(fileUpload)
        //         reader.readAsText(fileUpload);
        //     } else {
        //         alert("This browser does not support HTML5.");
        //     }
        // }
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


//Login
function check() {
    $('p').remove();
    if (document.getElementById('username').value == '') {
        $('.userd').append('<p><br />Username required</p>');
        $('#username').focus();
        return false;
    }
    if (document.getElementById('password').value == '') {
        $('.passd').append('<p>Password required</p>');
        $('#password').focus();
        return false;
    }
    if (document.getElementById('password').value.length < 8) {
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

//Role

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
                else {
                    alert("Invalid Current Password")
                }
            }
        });
        $('#new').val('');
        $('#renew').val('');
        $('#pre').val('');
    });
});


//Students

function searchStu(value = '') {
    let token = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/get-students',
        data: {
            'term': value,
        },
        dataType: 'json',
        success: function (data) {
            let students = JSON.parse(data.student);
            let html = '';
            for (let i = 0; i < students.length; i++) {
                let pk = students[i].pk;
                let student = students[i].fields;
                html += '<tr id="' + pk + '" ><td>' + pk + '</td><td>' + student.crn + '</td><td>' + student.full_name + '</td><td>' + student.Father_name + '</td><td>' + student.Mother_name + '</td><td>' + student.Contact + '</td><td>' + student.email + '</td></tr>';
            }
            $('tbody').html(html);
        }
    });
}

$(document).ready(function () {
    $('#downloadStu').click(function () {
        tableToExcel('stusearch', 'Students');
    });

    $('#studDet').click(function () {
        $("#Details").html($("#stuDet").html());
    });

    $('#pareDet').click(function () {
        $("#Details").html($("#parDet").html());
    });

    $('#markDet').click(function () {
        $("#Details").html($("#marDet").html());
    });


    $('table#stusearch').delegate('tr', 'click', function () {
        let urn = this.id;
        let token = $('meta[name="csrf-token"]').attr('content');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/get-student',
            data: {
                'student': urn,
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    let models = JSON.parse(data.student);
                    let student = models[0].fields;
                    let Class = models[1].fields;
                    let Department = models[2].fields;
                    for (let x in student)
                        $('#' + x).html(student[x]);
                    for (let x in Class)
                        $('#' + x).html(Class[x]);
                    for (let x in Department)
                        $('#' + x).html(Department[x]);
                    let da = new Date();
                    let sem = 2 * (4 - (Class['batch'] - da.getUTCFullYear()));
                    if (sem <= 8)
                        sem += da.getUTCMonth() > 5 ? 1 : 0;
                    let marks = JSON.parse(data.marks);
                    let html = '';
                    for (let i = 0; i < marks.length; i++) {
                        let mark = marks[i].fields;
                        html += '<div class="col-lg-6 col-sm-12 col-xs-12 d-flex">' + '<h6 class="mr-3">Semester:</h6>' + '<h6 class="h6">' + mark.sem + '</h6> </div>' + '<div class="col-lg-6 col-sm-12 col-xs-12 d-flex">' + '<h6 class="mr-3">SGPA:</h6>' + '<h6 class="h6">' + mark.sgpa + '</h6> </div>' + '<div class="col-lg-6 col-sm-12 col-xs-12 d-flex">' + '<h6 class="mr-3">Active backlogs:</h6>' + '<h6 class="h6">' + mark.active_backs + '</h6> </div>' + '<div class="col-lg-6 col-sm-12 col-xs-12 d-flex"> <h6 class="mr-3">Passive backlogs:</h6>' + '<h6 class="h6">' + mark.passive_backs + '</h6> </div>' + '<hr>';
                    }
                    $('#fathpic').attr('src', '/Media/' + student.Father_pic);
                    $('#mothpic').attr('src', '/Media/' + student.Mother_pic);
                    $('#stupic').attr('src', '/Media/' + student.photo);
                    $('#marDet').html(html);
                    $('#batch').html(sem);
                    $('#urn').html(urn);
                    $('#studDet').trigger('click');
                    $('#data').modal('show');
                }
                else {
                    alert('Error getting details');
                }
            }
        });
    });
});

function closeStudent() {
    $('#Details').html('');
}

var tableToExcel = (function () {
    var uri = 'data:application/vnd.ms-excel;base64,'
        , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
        , base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))) }
        , format = function (s, c) { return s.replace(/{(\w+)}/g, function (m, p) { return c[p]; }) }
    return function (table, name) {
        if (!table.nodeType) table = document.getElementById(table)
        var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML }
        window.location.href = uri + base64(format(template, ctx))
    }
})()

//uploadImage

$(document).ready(function () {
    $('#imsub').click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/get-student',
            data: {
                'student': $('#imurn').val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    let models = JSON.parse(data.student);
                    if (models[0].fields.dob == $('#imdob').val()) {
                        $('#imver').hide();
                        $('#imForm').show();
                    }
                }
                else {
                    alert('Incorrect details');
                }
            }
        });
    });

    $('#SSP').click(function () {
        let token = $('meta[name="csrf-token"]').attr('content');
        let formdata = new FormData();
        formdata.append('urn', $('#imurn').val());
        formdata.append('Father_pic', $('#FatherPic').prop('files')[0]);
        formdata.append('Mother_pic', $('#MotherPic').prop('files')[0]);
        formdata.append('photo', $('#studentPic').prop('files')[0]);
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/update-student',
            processData: false,
            contentType: false,
            data: formdata,
            success: function (data) {
                if (data.success) {
                    let model = JSON.parse(data.student);
                    console.log(model[0].fields.photo);
                    $('#fathPic').attr('src', '/Media/' + model[0].fields.Father_pic);
                    $('#mothPic').attr('src', '/Media/' + model[0].fields.Mother_pic);
                    $('#stuPic').attr('src', '/Media/' + model[0].fields.photo);
                    alert('Success');
                }
                else {
                    alert('Incorrect details');
                }
            }
        });
    });
});

function preview(input, targ) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(targ)
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$('#addStu').click(function () {
    $('#newStu').show();
});
