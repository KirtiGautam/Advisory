$(function () {
    $('#hods').selectpicker();
});
function set(i) {
    let token = $('meta[name="csrf-token"]').attr('content');
    $.ajax({
        type: "POST",
        headers: { "X-CSRFToken": token },
        url: '/get-hods',
        data: {
            'dept': i,
        },
        dataType: 'json',
        success: function (data) {
            console.log(data.hods)
            html = '';
            for (let i = 0; i < data.hods.length; i++) {
                html += '<option value="' + data.hods[i].full_name + '">' + data.hods[i].full_name + '</option>';
            }
            console.log(html)
            $('#hods').html(html).selectpicker('refresh');
            // $('#hods')
            // $('#hods')
            // $('#hods')
            $('#edit').show();
        }
    });

}

$('#ad').click(function () {
    $('#add').show();
});