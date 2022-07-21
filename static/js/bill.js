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

    function getUsersList() {
        return new Promise(function(resolve, reject) {

            let request = new XMLHttpRequest();

            request.open('GET', 'http://127.0.0.1:8000/bills/api/get_all_users');
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
        usersList = document.querySelector('.bills-list-users-list'),
        usersListHead = document.querySelector('#bills-are-payed-by'),
        usersListArrow = document.querySelector('.arrow');

    getUsersList()
        .then(response => {
            let usersListData = JSON.parse(response);

            function addUser(i) {
                let userDiv = document.createElement('div'),
                    user = document.createElement('h5'),
                    userName = document.createTextNode(usersListData[i]["first_name"]);
                
                userDiv.classList.add('bills-list-users-list-item');
                user.appendChild(userName);
                userDiv.appendChild(user);
                usersList.appendChild(userDiv);
            }

            for (let i = 0; i < usersListData.length; i++) {
                addUser(i);
            }

            getbillsList()
                .then(response => {
                    let billsListData = JSON.parse(response);

                    function showBillsForLender(billsData) {
                        // declare functions
                        function AddBill(billData) {
                            let billDiv = document.createElement('div'),
                                bill = document.createElement('h4'),
                                date = new Date(billData.date),
                                dateFormated = fomatDate(date),
                                billName = document.createTextNode(billData.name + ' ' + dateFormated);
                            
                            billDiv.classList.add('bills-list-item');
    
                            bill.appendChild(billName);
                            billDiv.appendChild(bill);
                            billDiv.addEventListener('mouseover', () => {showBill(billData);});
                            billDiv.addEventListener('mouseout', () => {hideBill();});
                            billsList.appendChild(billDiv);
                        }
    
                        function removeinnerHTML(element) {
                            element.innerHTML = '';
                        }

                        function removeEventListeners(element) {
                            element.replaceWith(element.cloneNode(true));
                        }

                        function showBill(billData) {
                            let billHeader = document.querySelector('.bill-header'),
                                billPaymentBoxItem = document.querySelector('.bill-payment-box-item'),
                                billPaymentBox = document.querySelector('.bill-payment-box'),
                                billDate = fomatDate(new Date(billData.date)),
                                billName = `${billData.name} ${billDate} ${billData.lender.first_name}`;
                            
                            billHeader.textContent = billName;
                            
                            // cleaning
                            removeinnerHTML(billPaymentBox);

                            // adding
                            for (let i = 0; i < billData.items.length; i++) {
                                let item = billData.items[i],
                                    billPaymentBoxItemClone = billPaymentBoxItem.cloneNode(true),
                                    children = billPaymentBoxItemClone.children;
                                
                                billPaymentBoxItemClone.style.display = 'flex';

                                children[0].textContent = item.name;
                                children[1].textContent = item.cost_per_exemplar;
                                children[2].textContent = 'x' + item.amount;

                                billPaymentBox.appendChild(billPaymentBoxItemClone);
                            }
                        }

                        function hideBill() {
                            let billHeader = document.querySelector('.bill-header'),
                                billPaymentBoxItem = document.querySelector('.bill-payment-box-item'),
                                billPaymentBox = document.querySelector('.bill-payment-box');
                            
                            billHeader.textContent = '';
                            
                            // cleaning
                            removeinnerHTML(billPaymentBox);

                            // saving one hidden item
                            billPaymentBoxItem.style.display = 'none';
                            billPaymentBox.appendChild(billPaymentBoxItem);
                        }

                        let showMoreBtn = document.querySelector('#show-more'),
                            showLessBtn = document.querySelector('#show-less');
                        ////// script //////

                        // cleaning up
                        removeinnerHTML(billsList);
                        removeEventListeners(showMoreBtn);
                        removeEventListeners(showLessBtn);

                        // re-assigning
                        showMoreBtn = document.querySelector('#show-more');
                        showLessBtn = document.querySelector('#show-less');

                        // closing menu
                        usersList.style.display = 'none';
                        usersListArrow.classList.remove('up');
                        usersListArrow.classList.add('down');

                        // show bills
                        if (billsData.length < 5) {
                            // showing all bills
                            for (let i = 0; i < billsData.length; i++) {
                                AddBill(billsData[i]);
                            }
                            // there is no need for this button
                            showMoreBtn.style.display = 'none';
                            showLessBtn.style.display = 'none';
                        } else {
                            showMoreBtn.style.display = 'block';
                            showLessBtn.style.display = 'none';
                            // showing 5 bills
                            for (let i = 0; i < 5; i++) {
                                AddBill(billsData[i]);
                            }

                            showMoreBtn.addEventListener('click', () => {

                                for (let i = 5; i < billsData.length; i++) {
                                    AddBill(billsData[i]);
                                }

                                showMoreBtn.style.display = 'none';
                                showLessBtn.style.display = 'block';
                            });

                            showLessBtn.addEventListener('click', () => {
                                removeinnerHTML(billsList);

                                for (let i = 0; i < 5; i++) {
                                    AddBill(billsData[i]);
                                }
                                showMoreBtn.style.display = 'block';
                                showLessBtn.style.display = 'none';
                            });
                        }
                    }

                    // starting position is filter ALL
                    showBillsForLender(billsListData);


                    usersListArrow.addEventListener('click', (event) => {
                        let target = event.target;
                        if (target.classList.contains('down')) {
                            usersList.style.display = 'block';
                            //billsList.style.marginTop = `${-usersList.clientHeight}px`;
                            target.classList.remove('down');
                            target.classList.add('up');
                        } else {
                            usersList.style.display = 'none';
                            //billsList.style.marginTop = '0px';
                            target.classList.remove('up');
                            target.classList.add('down');
                        }
                    });

                    /////// adding Filter /////
                    let usersListItems = document.querySelectorAll('.bills-list-users-list-item,.bills-list-users-list-item-current'),
                        checkmarkDiv = document.querySelector('.checkmark');
                    
                    // adding eventListener on ALL filter
                    usersListItems[0].addEventListener('click', () => {

                        // changing bills list
                        showBillsForLender(billsListData);

                        // changing users list
                        usersListHead.textContent = `Bills are payed by`;

                        usersListItems.forEach((element)=>{
                            if (element.classList.contains('bills-list-users-list-item-current')) {
                                element.classList.remove('bills-list-users-list-item-current');
                                element.classList.add('bills-list-users-list-item');
                            }
                        });
                        usersListItems[0].classList.remove('bills-list-users-list-item');
                        usersListItems[0].classList.add('bills-list-users-list-item-current');
                        if (checkmarkDiv.parentNode) {
                            checkmarkDiv.parentNode.removeChild(checkmarkDiv);
                            usersListItems[0].prepend(checkmarkDiv);
                        }
                    });

                    // adding eventListener on Users (except ALL)
                    for (let i = 1; i < usersListItems.length; i++) {
                        usersListItems[i].addEventListener('click', () => {

                            let billsListDataByLender = [],
                                userId = usersListData[i - 1].id,
                                userFirstName = usersListData[i - 1].first_name;

                            // making bills list
                            for (let j = 0; j < billsListData.length; j++) {
                                // cheking if bill's lender is consistent with filter
                                if (billsListData[j]["lender"].id == userId) {
                                    billsListDataByLender.push(billsListData[j]);  
                                }
                            }

                            // changing bills list
                            showBillsForLender(billsListDataByLender);

                            // changing users list
                            usersListHead.textContent = `Bills are payed by ${userFirstName}`;

                            usersListItems.forEach((element)=>{
                                if (element.classList.contains('bills-list-users-list-item-current')) {
                                    element.classList.remove('bills-list-users-list-item-current');
                                    element.classList.add('bills-list-users-list-item');
                                }
                            });
                            
                            usersListItems[i].classList.remove('bills-list-users-list-item');
                            usersListItems[i].classList.add('bills-list-users-list-item-current');
                            if (checkmarkDiv.parentNode) {
                                checkmarkDiv.parentNode.removeChild(checkmarkDiv);
                                usersListItems[i].prepend(checkmarkDiv);
                            }
                        });
                    }
                })
                .catch(() => console.log("Что-то пошло не так"));
        })
        .catch(() => console.log("Что-то пошло не так"));
});