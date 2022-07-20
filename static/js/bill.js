window.addEventListener('DOMContentLoaded', function() {
    'use strict';

    function animateAccountPopupWindow() {
        let headerUserBox = document.querySelector('.header-right-menu-user-box'),
            accountPopupWindow = document.querySelector('.account-popup-window'),
            signout = document.querySelector('.account-popup-window-signountbox');
            
        headerUserBox.addEventListener('click', function() {
            if (accountPopupWindow.style.display == 'none') {
                accountPopupWindow.style.display = 'block';
            } else {
                accountPopupWindow.style.display = 'none';
            }
        });

        signout.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#F8F8F8';
        });

        signout.addEventListener('mouseout', function() {
            this.style.backgroundColor = '#FFFFFF';
        });
    }

    animateAccountPopupWindow();


    function getbillsList() {
        return new Promise(function(resolve, reject) {

            let request = new XMLHttpRequest();

            request.open('GET', 'http://127.0.0.1:8000/bills/api/get_bills');
            request.setRequestHeader('Content-type', 'application/json; charset=utf-8');
            request.send();

            request.onload = function() {
                if(request.readyState === 4) {
                    if(request.status == 200) {
                        resolve(this.response);
                    }
                    else {
                        reject();
                    
                    }
                }
            };
        });
    }

    function fomatDate(date) {
        function getTwoDigitDate(number) {
            return (number < 10) ? 0 + number.toString(): number.toString();
        }
        return `${getTwoDigitDate(date.getDate())}-${getTwoDigitDate(date.getMonth() + 1)}`;
    }

    let billsList = document.querySelector('.bills-list'),
        showMoreBtn = document.querySelector('#show-more'),
        showLessBtn = document.querySelector('#show-less');


    getbillsList()
        .then(response => {
            let billsListData = JSON.parse(response);

            function AddBill(i) {
                let billDiv = document.createElement('div'),
                    bill = document.createElement('h4'),
                    date = new Date(billsListData[i].date),
                    dateFormated = fomatDate(date),
                    billName = document.createTextNode(billsListData[i].name + ' ' + dateFormated);
                
                billDiv.classList.add('bills-list-item');

                bill.appendChild(billName);
                billDiv.appendChild(bill);
                billsList.appendChild(billDiv);
            }

            // showing 5 bills
            for (let i = 0; i < 5; i++) {
                AddBill(i);
            }


            showMoreBtn.addEventListener('click', () => {

                for (let i = 5; i < billsListData.length; i++) {
                    AddBill(i);
                }

                showMoreBtn.style.display = 'none';
                showLessBtn.style.display = 'block';
            });

            showLessBtn.addEventListener('click', () => {
                // removing all elements
                billsList.innerHTML = '';
                // adding 5 elements
                for (let i = 0; i < 5; i++) {
                    AddBill(i);
                }
                showMoreBtn.style.display = 'block';
                showLessBtn.style.display = 'none';
            });
            
        })
        .catch(() => console.log("Что-то пошло не так"));


});