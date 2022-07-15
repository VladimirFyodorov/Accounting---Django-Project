window.addEventListener('DOMContentLoaded', function() {
    'use strict';

    let menu = document.querySelector('.info-header'),
        tabs = document.querySelectorAll('.info-header-tab'),
        tabsContent = document.querySelectorAll('.info-tabcontent');

    
    function hideTabContent(a) {
        for (let i = a; i < tabsContent.length; i++) {
            tabsContent[i].classList.remove('show');
            tabsContent[i].classList.add('hide');
        }
    }

    function showTabContent(a) {
        if (tabsContent[a].classList.contains('hide')) {
            tabsContent[a].classList.remove('hide');
            tabsContent[a].classList.add('show');
        }
    }

    // on first load - hide all tabs content except first one
    hideTabContent(1);

    // inicializing tabs
    menu.addEventListener('click', function(event) {
        let target = event.target;
        
        if (target && target.classList.contains('info-header-tab')) {
            for (let i = 0; i < tabs.length; i++) {
                if (target == tabs[i]) {
                    hideTabContent(0);
                    showTabContent(i);
                }
            }
        }
    });


});