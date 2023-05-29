'use strict';

 // Open offsite navigation.
 $('#nav-expander').on('click', function(e) {
    e.preventDefault();
    $('nav').toggleClass('nav-expanded');
});

// Close offsite navigation.
 $('.menu .close').on('click', function(e) {
    e.preventDefault();
    $('nav').toggleClass('nav-expanded');
});

// Close offsite navigation after user click on an link in navigation.
$('.menu  a').on('click', function(e) {
    $('nav').removeClass('nav-expanded');
});


//Calculate full with of jumbotron.
 function homeFullScreen() {
    var homeSection = $('.home');
    var windowHeight = $(window).outerHeight();

    if (homeSection.hasClass('home-fullscreen')) {

        $('.home-fullscreen').css('height', windowHeight);
    }
}

// Initialization
$(window).load(function () {
    homeFullScreen();
    // smoothScroll.init();
});


//What happens on window resize
$(window).resize(function () {
    homeFullScreen();
});


