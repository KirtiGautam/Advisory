$('student').addClass('act');

let token = $('meta[name="csrf-token"]').attr('content');

function searchStu(value = '') {
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/get-students',
        data: {
            'term': value,
            'class': $('#ABatch').val(),
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
    searchStu();

    $('#ABatch').change(function () {
        console.log('Inside change function');
        $('#SSB').keyup();
    });

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

    $('#AS').click(function () {
        data = {
            'urn': document.getElementsByName('urn')[0].value,
            'crn': document.getElementsByName('crn')[0].value,
            'full_name': document.getElementsByName('name')[0].value,
            'dob': document.getElementsByName('dob')[0].value,
            'gender': document.getElementsByName('gender')[0].value,
            'living': document.getElementsByName('living')[0].value,
            'blood_group': document.getElementsByName('blood')[0].value,
            'category': document.getElementsByName('category')[0].value,
            'Contact': document.getElementsByName('contact')[0].value,
            'email': document.getElementsByName('email')[0].value,
            'height': document.getElementsByName('height')[0].value,
            'weight': document.getElementsByName('weight')[0].value,
            'Father_name': document.getElementsByName('father_name')[0].value,
            'Mother_name': document.getElementsByName('mother_name')[0].value,
            'Father_contact': document.getElementsByName('father_contact')[0].value,
            'Mother_contact': document.getElementsByName('mother_contact')[0].value,
            'Address': document.getElementsByName('address')[0].value,
            'Pincode': document.getElementsByName('pincode')[0].value,
            'City': document.getElementsByName('city')[0].value,
            'State': document.getElementsByName('state')[0].value,
            'District': document.getElementsByName('district')[0].value,
        };
        console.log(data);
        if (valStu(data)) {
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": token },
                url: '/create-student',
                data: {
                    'student': JSON.stringify(data)
                },
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        alert('Success');
                        searchStu();
                    }
                    else {
                        alert('Incorrect details');
                    }
                }
            });
        }
    });


    $('table#stusearch').delegate('tr', 'click', function () {
        let urn = this.id;

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
                    let da = new Date();
                    let sem = 2 * (4 - (models[1].fields['batch'] - da.getUTCFullYear()));
                    if (sem <= 8)
                        sem += da.getUTCMonth() > 5 ? 1 : 0;
                    setStuDetails(models[0].pk, models[0].fields, models[1].fields, models[2].fields, sem);
                    setStuMarks(models[0].fields['diploma_marks'], data.marks, sem);
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

function setStuMarks(diploma, marks, sem) {
    let SGPA = 0;
    let Credits = 0;
    let Active_backs = 0;
    let Passive_backs = 0;
    let html = '';
    html += '<table class="table table-hover table-bordered">';
    html += '<thead class="thead-dark"><tr><th>Subject Code</th><th>Subject Name</th><th>Grade</th><th>Examination Date</th><th>Credits</tr></thead>';
    html += '<tbody>'
    for (let i = (diploma == 0) ? 1 : 3; i < sem; i++) {
        for (let i = 1; i < sem; i++) {
            let credits = 0;
            let sgpa = 0;
            let active_backs = 0;
            let passive_backs = 0;
            html += '<tr class="table-dark"><td colspan=5>Semester' + i + '</td></tr>';
            for (let x in marks) {
                if (marks[x].semester == i) {
                    if (marks[x].Sgpa != 0) {
                        html += '<tr><td>' + marks[x].subject + '</td><td>' + marks[x].subject__Name + '</td><td>' + marks[x].Sgpa + ' </td><td>' + marks[x].exam_date + '</td><td>' + marks[x].subject__credits + '</td></tr>';
                        sgpa += (marks[x].Sgpa * marks[x].subject__credits);
                        credits += marks[x].subject__credits;
                        if (marks[x].passive_back)
                            passive_backs += 1;
                    } else {
                        html += '<tr><td>' + marks[x].subject + '</td><td>' + marks[x].subject__Name + '</td><td>' + marks[x].exam_date + ' </td></tr>';
                        active_backs += 1;
                    }
                    const index = marks.indexOf(x);
                    if (index > -1) {
                        marks.splice(index, 1);
                    }
                }
            }
            html += '<h6>Semester SGPA = ';
            html += active_backs != 0 ? 'Fail' : (sgpa / credits);
            html += '   Semester Credits earned = ' + credits + '  Passive backs = ' + passive_backs + '  Active backs = ' + active_backs + '</h6></div>';
            SGPA += sgpa;
            Credits += credits;
            Active_backs += active_backs;
            Passive_backs += passive_backs;
        }
        html += '<div style="display: block; block; width: 100%;"><h3>Aggregate SGPA : ';
        html += Active_backs != 0 ? 'Fail' : (SGPA / Credits);
        html += '<br>Aggregate Credits earned = ' + Credits + '<br>Active Backlogs = ' + Active_backs + '<br>Passive Backlogs = ' + Passive_backs + '</h3></div>';
        $('#marDet').html(html);
    }
}

function setStuDetails(urn, student, Class, Department, sem) {
    for (let x in student)
        $('#' + x + ', .' + x).html(student[x]);
    for (let x in Class)
        $('#' + x).html(Class[x]);
    for (let x in Department)
        $('#' + x).html(Department[x]);
    $('#urn').html(urn);
    $('.urn').val(urn);
    $('#batch').html(sem);
    if (student.Father_pic != '') {
        $('#fathpic').attr('src', '/Media/' + student.Father_pic);
        $('#mothpic').attr('src', '/Media/' + student.Mother_pic);
        $('#stupic').attr('src', '/Media/' + student.photo);
    } else {
        $('#fathpic').attr('src', '');
        $('#mothpic').attr('src', '');
        $('#stupic').attr('src', '');
    }
}



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

$('#addStu').click(function () {
    $('#newStu').show();
});