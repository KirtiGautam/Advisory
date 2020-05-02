let token = $('meta[name="csrf-token"]').attr('content');


function uploadData(model, dataId, btnID) {
    Papa.parse(document.getElementById(dataId).files[0], {
        header: true,
        complete: function (results) {
            console.log(results.data);
            let inlength = Object.keys(results.data[0]).length;
            for (let i = 0; i < results.data.length; i++) {
                if (Object.keys(results.data[i]).length != inlength)
                    results.data.splice(i, 1);
            }
            console.log(results.data);
            $.ajax({
                type: "POST",
                headers: { "X-CSRFToken": token },
                url: '/upload-data',
                data: {
                    'tdata': JSON.stringify(results.data),
                    'model': model,
                },
                dataType: 'json',
                success: function (data) {
                    if (data.success) {
                        alert('File upload success');
                        $("#" + dataId).replaceWith($("#" + dataId).val('').clone(true));
                        $('#' + btnID).html('Upload Data');
                    }
                }
            });
        }
    });
}

function check(id) {
    var fileInput = document.getElementById(id);
    var filePath = fileInput.value;
    var allowedExtensions = /(\.csv)$/i;

    if ($('#' + id).get(0).files.length == 0) {
        alert('Please select a file to upload');
        return false;
    } else if (!allowedExtensions.exec(filePath)) {
        alert('Please upload csv file only.');
        fileInput.value = '';
        return false;
    }
    return true;
}

$(document).ready(function () {
    $('#dataupload').addClass('act');

    $("#DB").click(function () {
        if (check('DD')) {
            $("#DB").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            uploadData('department', 'DD', 'DB');
        }
    });

    $("#TB").click(function () {
        if (check('TD')) {
            $("#TB").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            uploadData('teachers', 'TD', 'TB');
        }
    });

    $("#SB").click(function () {
        if (check('SD')) {
            $("#SB").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            uploadData('students', 'SD', 'SB');
        }
    });

    $("#MB").click(function () {
        if (check('MD')) {
            $("#MB").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            uploadData('marks', 'MD', 'MB');
        }
    });
});

//Might use later don't delete

    // $("#upload").click(function () {

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
    // });
