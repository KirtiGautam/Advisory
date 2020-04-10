let token = $('meta[name="csrf-token"]').attr('content');

$('#dataupload').addClass('act');

$(document).ready(function () {

    $("#upload").click(function () {

        Papa.parse(document.getElementById("data").files[0], {
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
