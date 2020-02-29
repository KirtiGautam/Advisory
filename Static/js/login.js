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