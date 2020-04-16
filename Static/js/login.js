function check() {
    $('.login-btn').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
    if ($('#username').val() == '') {
        alert('Username cannot be empty');
        $("#username").focus();
        return false;
    } else if ($('#password').val() == '') {
        alert('Password cannot be empty');
        $("#password").focus();
        return false
    }
    return true;
}
