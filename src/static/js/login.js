
$(document).ready( () => {
    $("#signup").on("click", signup)
    $("#login").on("click", login)
});


function signup () {
    let form = $("#login-form");
    form.attr("action", "/signup");
    form.submit();
}


function login () {
    let form = $("#login-form");
    form.attr("action", "/login");
    form.submit();
}