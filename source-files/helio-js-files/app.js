/*! ------------------------------------------------
 * Project Name: Helio - Coming Soon and Landing Page Template
 * Project Description: Helio - bright and clean coming soon and landing page template to kick-start your project
 * Tags: mix_design, coming soon, under construction, template, landing page, portfolio, one page, responsive, html5, css3, creative, clean, agency, personal page
 * Version: 1.0.0
 * Build Date: November 2023
 * Last Update: November 2023
 * This product is available exclusively on Themeforest
 * Author: mix_design
 * Author URI: https://themeforest.net/user/mix_design
 * File name: app.js
 * ------------------------------------------------

 * ------------------------------------------------
 * Table of Contents
 * ------------------------------------------------
 *
 *  1. Color Switch
 *  1. SVG Fallback
 *  2. Chrome Smooth Scroll
 *  3. Images moving ban
 *  4. Detecting Mobile/Desktop
 *  7. Menu & Sections Behavior
 *  8. Popup Open/Close
 *  9. Buttons Hover Effect
 *  10. PhotoSwipe Gallery Images Replace
 *
 * ------------------------------------------------
 * Table of Contents End
 * ------------------------------------------------ */


// Color Switch
const themeBtn = document.querySelector('.color-switcher');

function getCurrentTheme(){
  let theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  localStorage.getItem('helio.theme') ? theme = localStorage.getItem('helio.theme') : null;
  return theme;
}

function loadTheme(theme){
  const root = document.querySelector(':root');
  if(theme === "light"){
    themeBtn.innerHTML = `<em></em><i class="ph ph-moon-stars"></i>`;
  } else {
    themeBtn.innerHTML = `<em></em><i class="ph ph-sun"></i>`;
  }
  root.setAttribute('color-scheme', `${theme}`);
};

themeBtn.addEventListener('click', () => {
  let theme = getCurrentTheme();
  if(theme === 'dark'){
    theme = 'light';
  } else {
    theme = 'dark';
  }
  localStorage.setItem('helio.theme', `${theme}`);
  loadTheme(theme);
});

window.addEventListener('DOMContentLoaded', () => {
  loadTheme(getCurrentTheme());
});

$(function() {

  "use strict";

  // SVG Fallback
  if(!Modernizr.svg) {
    $("img[src*='svg']").attr("src", function() {
      return $(this).attr("src").replace(".svg", ".png");
    });
  };

  // Chrome Smooth Scroll
  try {
    $.browserSelector();
    if($("html").hasClass("chrome")) {
      $.smoothScroll();
    }
  } catch(err) {
  };

  // Images moving ban
  $("img, a").on("dragstart", function(event) { event.preventDefault(); });

  // Detecting Mobile/Desktop
  var isMobile = false;
  if( /Android|webOS|iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    $('html').addClass('touch');
    isMobile = true;
  }
  else {
    $('html').addClass('no-touch');
    isMobile = false;
  }
  //IE, Edge
  var isIE = /MSIE 9/i.test(navigator.userAgent) || /rv:11.0/i.test(navigator.userAgent) || /MSIE 10/i.test(navigator.userAgent) || /Edge\/\d+/.test(navigator.userAgent);
  
  // Menu & Sections Behavior
  var menuTrigger        = $('#menu-trigger'),
      menu               = $('#menu'),
      colorSwitcher      = $('#color-switcher'),
      mainSection        = $('#main'),
      aboutSection       = $('#about'),
      worksSection       = $('#works'),
      contactSection     = $('#contact'),
      aboutTrigger       = $('#about-trigger'),
      aboutTriggerBottom = $('#about-trigger-bottom'),
      worksTrigger       = $('#works-trigger'),
      contactTrigger     = $('#contact-trigger'),
      aboutClose       = $('#about-close'),
      worksClose       = $('#works-close'),
      contactClose     = $('#contact-close');

  // menu open - mobile
  menuTrigger.on('click', function(event) {
    event.preventDefault();
    menu.toggleClass('is-visible');
    menuTrigger.toggleClass('menu-is-visible');
  });

  // about section open
  aboutTrigger.on('click', function(event) {
    event.preventDefault();
    mainSection.addClass('animate-out');
    aboutSection.addClass('animate-in');
    setTimeout(function(){
      colorSwitcher.addClass('inner-is-visible');
    }, 500);
    setTimeout(function(){
      menu.removeClass('is-visible');
      menuTrigger.removeClass('menu-is-visible');
    }, 800);
  });

  // about section open
  aboutTriggerBottom.on('click', function(event) {
    event.preventDefault();
    mainSection.addClass('animate-out');
    aboutSection.addClass('animate-in');
    setTimeout(function(){
      colorSwitcher.addClass('inner-is-visible');
    }, 500);
    setTimeout(function(){
      menu.removeClass('is-visible');
      menuTrigger.removeClass('menu-is-visible');
    }, 800);
  });

  // about section close
  aboutClose.on('click', function(event) {
    event.preventDefault();
    mainSection.removeClass('animate-out');
    aboutSection.removeClass('animate-in');
    setTimeout(function(){
      colorSwitcher.removeClass('inner-is-visible');
    }, 100);
    setTimeout(function(){
      aboutSection.animate({ scrollTop: 0 , });
      $('#about .inner__info').animate({ scrollTop: 0 , });
    }, 600);
  });

  // works section open
  worksTrigger.on('click', function(event) {
    event.preventDefault();
    mainSection.addClass('animate-out');
    worksSection.addClass('animate-in');
    setTimeout(function(){
      colorSwitcher.addClass('inner-is-visible');
    }, 500);
    setTimeout(function(){
      menu.removeClass('is-visible');
      menuTrigger.removeClass('menu-is-visible');
    }, 800);
  });

  // works section close
  worksClose.on('click', function(event) {
    event.preventDefault();
    mainSection.removeClass('animate-out');
    worksSection.removeClass('animate-in');
    setTimeout(function(){
      colorSwitcher.removeClass('inner-is-visible');
    }, 100);
    setTimeout(function(){
      worksSection.animate({ scrollTop: 0 , });
      $('#works .inner__info').animate({ scrollTop: 0 , });
    }, 600);
  });

  // contact section open
  contactTrigger.on('click', function(event) {
    event.preventDefault();
    mainSection.addClass('animate-out');
    contactSection.addClass('animate-in');
    setTimeout(function(){
      colorSwitcher.addClass('inner-is-visible');
    }, 500);
    setTimeout(function(){
      menu.removeClass('is-visible');
      menuTrigger.removeClass('menu-is-visible');
    }, 800);
  });

  // contact section close
  contactClose.on('click', function(event) {
    event.preventDefault();
    mainSection.removeClass('animate-out');
    contactSection.removeClass('animate-in');
    setTimeout(function(){
      colorSwitcher.removeClass('inner-is-visible');
    }, 100);
    setTimeout(function(){
      contactSection.animate({ scrollTop: 0 , });
      $('#contact .inner__info').animate({ scrollTop: 0 , });
    }, 600);
  });

  // Popup Open/Close
  var notify            = $('#notify'),
      notifyTrigger     = $('#notify-trigger'),
      notifyClose       = $('#notify-close');

  // Notify Form Open
  notifyTrigger.on('click', function(event){
    event.preventDefault();
    notify.addClass('animate-in').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function() {
      notifyClose.addClass('is-scaled-up');
    });
  });

  // Notify Form Close
  notifyClose.on('click', function(event){
    event.preventDefault();
    notifyClose.removeClass('is-scaled-up');
    setTimeout(function(){
      notify.addClass('animate-out');
    }, 300);
    setTimeout(function(){
      notify.removeClass('animate-in animate-out');
    }, 1000);
  });

  // Buttons Hover Effect
  $('.hover-anim')
  .on('mouseenter', function(e) {
    var parentOffset = $(this).offset(),
      relX = e.pageX - parentOffset.left,
      relY = e.pageY - parentOffset.top;
    $(this).find('em').css({top:relY, left:relX})
  })
  .on('mouseout', function(e) {
    var parentOffset = $(this).offset(),
      relX = e.pageX - parentOffset.left,
      relY = e.pageY - parentOffset.top;
    $(this).find('em').css({top:relY, left:relX})
  });

  // PhotoSwipe Gallery Images Replace
    $('.my-gallery__link')
    // Background set up
    .each(function(){
    $(this)
    // Add a photo container
    .append('<div class="picture"></div>')
    // Set up a background image for each link based on data-image attribute
    .children('.picture').css({'background-image': 'url('+ $(this).attr('data-image') +')'});
  });

});
