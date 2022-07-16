window.addEventListener('DOMContentLoaded', function() {
    'use strict';

    let rows = document.getElementsByTagName('tr'),
        menuItems = document.querySelectorAll('.account-menu-items'),
        tables = document.querySelectorAll('.account-table');

    function showTable(n) {
        for (let i = 0; i < tables.length; i++) {
            tables[i].style.display = 'none';
            menuItems[i].style.backgroundColor = '#FFFFFF';
        }

        tables[n].style.display = 'block';
        menuItems[n].style.backgroundColor = '#D7D7D7';
    }


    for (let i = 0; i < menuItems.length; i++) {
        menuItems[i].addEventListener('click', function() {
            showTable(i);
        });
    }

    for (let i = 0; i < rows.length; i++) {

        let amount = +rows[i].getElementsByClassName('amount')[0].textContent,
            btn = rows[i].getElementsByTagName('button')[0];
        
        if (btn) {

            if (amount > 0) {
                btn.textContent = 'Receive';
                btn.style.display = 'block';
            } else if (amount < 0) {
                btn.textContent = 'Pay';
                btn.style.display = 'block';
            } else {
                btn.style.display = 'none';
            }


            btn.addEventListener('mouseover', function() {
                this.style.backgroundColor = 'black';
                this.style.color = 'white';
            });

            btn.addEventListener('mouseout', function() {
                this.style.backgroundColor = 'white';
                this.style.color = 'black';
            });

            btn.addEventListener('click', function() {
                alert(5);
            });
        }
    }

});