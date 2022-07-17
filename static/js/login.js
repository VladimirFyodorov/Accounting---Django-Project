window.addEventListener('DOMContentLoaded', function() {
    'use strict';

    let form_numer = document.getElementById('form_numer'),
        forms = document.querySelectorAll('.form'),
        see_password_icon = document.querySelector('#see-password-icon'),
        input_password = document.querySelector('#password');

    if (form_numer.textContent == 2) {
        forms[0].style.display = 'none';
        forms[1].style.display = 'block';
    }

    see_password_icon.addEventListener('click', function() {
        if (input_password.type == 'password') {
            input_password.type = 'text';
            see_password_icon.classList.toggle('bi-eye');
        } else {
            input_password.type = 'password';
            see_password_icon.classList.toggle('bi-eye');
        }
    });

});