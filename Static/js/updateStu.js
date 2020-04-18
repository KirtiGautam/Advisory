let token = $('meta[name="csrf-token"]').attr('content');

function valStu(data) {
    for (let x in data) {
        if (data[x] == '') {
            alert('Please enter all details');
            return false;
        }
    }
    if (data['Contact'].length != 10 ||
        data['Father_contact'].length != 10 ||
        data['Mother_contact'].length != 10) {
        alert('Contact number must be equal to 10 digits');
        return false;
    }
    if (data['urn'].length != 7 || data['crn'].length != 7) {
        alert('Roll number must be equal to 7 digits');
        return false;
    }
    return true;
}

function getPin(pincode, COP) {
    if (pincode.length == 6) {
        $.ajax({
            type: "POST",
            headers: { "X-CSRFToken": token },
            url: '/get-pin',
            data: {
                'id': pincode,
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    document.getElementsByName(COP + 'City')[0].value = data.City;
                    document.getElementsByName(COP + 'State')[0].value = data.State;
                    document.getElementsByName(COP + 'District')[0].value = data.District;
                }
            }
        });
    }
}