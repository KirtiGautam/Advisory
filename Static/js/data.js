$(document).ready(function () {

    $('#dataupload').addClass('active');

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