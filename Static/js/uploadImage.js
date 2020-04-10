let token = $('meta[name="csrf-token"]').attr('content');

$(document).ready(function () {
    $('#imsub').click(function () {

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