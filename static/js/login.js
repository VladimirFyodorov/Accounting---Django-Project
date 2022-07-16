window.addEventListener('DOMContentLoaded', function() {
    'use strict';

    let form_numer = document.getElementById('form_numer'),
        forms = document.querySelectorAll('.form');

    if (form_numer.textContent == 2) {
        forms[0].style.display = 'none';
        forms[1].style.display = 'block';
    }

});