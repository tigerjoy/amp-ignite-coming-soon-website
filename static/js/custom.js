// ------------------------------------------------
// Project Name: Helio - Coming Soon and Landing Page Template
// Project Description: Helio - bright and clean coming soon and landing page template to kick-start your project
// Tags: mix_design, coming soon, under construction, template, landing page, portfolio, one page, responsive, html5, css3, creative, clean, agency, personal page
// Version: 1.0.0
// Build Date: November 2023
// Last Update: November 2023
// This product is available exclusively on Themeforest
// Author: mix_design
// Author URI: https://themeforest.net/user/mix_design
// File name: custom.js
// ------------------------------------------------

// ------------------------------------------------
// Table of Contents
// ------------------------------------------------
//
//  1. Loader & Loading Animation
//  2. Typed.js Plugin Settings
//  3. Swiper Slider
//  4. Magnific Popup Video
//  5. KBW-Countdown
//  6. Vegas Kenburns
//  7. Accordion
//  8. Skillbars
//  9. Mailchimp Notify Form
//  10. Contact Form
//  11. ParticlesJS Backgrounds
//
// ------------------------------------------------
// Table of Contents End
// ------------------------------------------------

$(window).on("load", function () {

  "use strict";

  // --------------------------------------------- //
  // Loader & Loading Animation Start
  // --------------------------------------------- //
  $(".loader__logo").addClass('scaleOut');

  setTimeout(function () {
    $(".loader").addClass('loaded');
    $("#main").addClass('animate-in');
    $("body").addClass('loaded');
  }, 300);
  // --------------------------------------------- //
  // Loader & Loading Animation End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // Typed.js Plugin Settings Start
  // --------------------------------------------- //
  var animatedHeadline = $(".animated-headline");
  if (animatedHeadline.length) {
    var typed = new Typed('#typed', {
      stringsElement: '#typed-strings',
      loop: true,
      typeSpeed: 60,
      backSpeed: 30,
      backDelay: 2500
    });
  }
  // --------------------------------------------- //
  // Typed.js Plugin Settings End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // Set User's timezone Start
  // --------------------------------------------- //
  var timezone = jstz.determine();
  var timezoneName = timezone.name();
  var offsetMinutes = timezone.needle ? timezone.needle.split(",") : [0];
  offsetMinutes = Number(offsetMinutes[0]);
  var offsetHours = Math.floor(offsetMinutes / 60);
  var offsetMinutesPart = offsetMinutes % 60;

  var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
  csrftoken = csrftoken ? csrftoken : "";
  var formattedOffset = `(GMT${offsetHours >= 0 ? '+' : ''}${String(offsetHours).padStart(2, "0")}:${String(offsetMinutesPart).padStart(2, "0")})`;
  console.log(timezoneName + ' ' + formattedOffset);

  $.ajax({
    type: 'POST',
    url: window.endpoints && window.endpoints["setTimezone"] ? window.endpoints["setTimezone"] : "/404",
    headers: {
      'X-CSRFToken': csrftoken
    },
    data: {
      'timezone': timezoneName,
      'formattedOffset': formattedOffset
    },
    success: function (response) {
      console.log('Timezone set successfully');
    },
    error: function (xhr, status, error) {
      console.error('Error setting timezone:', error);
    }
  });
  // --------------------------------------------- //
  // Set User's timezone End
  // --------------------------------------------- //
});

$(function () {

  "use strict";

  // --------------------------------------------- //
  // Swiper Slider Start
  // --------------------------------------------- //
  var swiper = new Swiper('.swiper', {
    // Optional parameters
    grabCursor: true,
    effect: "creative",
    creativeEffect: {
      prev: {
        //shadow: true,
        translate: ["-20%", 0, -1],
      },
      next: {
        translate: ["100%", 0, 0],
      },
    },
    parallax: true,
    speed: 1300,
    loop: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },

    // If we need pagination
    pagination: {
      el: ".swiper-pagination",
      type: "fraction",
    },

    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },

  });
  // --------------------------------------------- //
  // Swiper Slider End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // Magnific Popup Video Start
  // --------------------------------------------- //
  $('#showreel-trigger').magnificPopup({
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false,
    callbacks: {
      beforeOpen: function () { $('body').addClass('overflow-hidden'); },
      close: function () { $('body').removeClass('overflow-hidden'); }
    }
  });

  $('#inner-video-trigger').magnificPopup({
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false,
    callbacks: {
      beforeOpen: function () { $('body').addClass('overflow-hidden'); },
      close: function () { $('body').removeClass('overflow-hidden'); }
    }
  });
  // --------------------------------------------- //
  // Magnific Popup Video End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // KBW-Countdown Start
  // --------------------------------------------- //
  $('#countdown').countdown({ until: $.countdown.UTCDate(+10, 2024, 2, 2), format: 'D' });
  // --------------------------------------------- //
  // KBW-Countdown End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // Vegas Kenburns Start
  // --------------------------------------------- //
  var bgndKenburns = $('#bgndKenburns');
  if (bgndKenburns.length) {
    bgndKenburns.vegas({
      timer: false,
      delay: 8000,
      transition: 'fade2',
      transitionDuration: 2000,
      slides: [
        { src: "https://dummyimage.com/1440x1620/4d4d4d/636363" },
        { src: "https://dummyimage.com/1440x1620/4d4d4d/636363" },
        { src: "https://dummyimage.com/1440x1620/4d4d4d/636363" }
      ],
      animation: ['kenburnsUp', 'kenburnsDown', 'kenburnsLeft', 'kenburnsRight']
    });
  }
  // --------------------------------------------- //
  // Vegas Kenburns End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // Accordion Start
  // --------------------------------------------- //
  $(".accordion__title").on("click", function (e) {

    e.preventDefault();
    var $this = $(this);

    if (!$this.hasClass("accordion-active")) {
      $(".accordion__content").slideUp(400);
      $(".accordion__title").removeClass("accordion-active");
      $('.accordion__arrow').removeClass('accordion-rotate');
    }

    $this.toggleClass("accordion-active");
    $this.next().slideToggle();
    $('.accordion__arrow', this).toggleClass('accordion-rotate');
  });
  // --------------------------------------------- //
  // Accordion End
  // --------------------------------------------- //


  // --------------------------------------------- //
  // Skillbars Settings Start
  // --------------------------------------------- //
  $('.skillbar').skillBars({
    from: 0,
    speed: 4000,
    interval: 100,
  });
  // --------------------------------------------- //
  // Skillbars Settings End
  // --------------------------------------------- //

  // --------------------------------------------- //
  // Mailchimp Notify Form Start
  // --------------------------------------------- //
  // $('.notify-form').ajaxChimp({
  //   callback: mailchimpCallback,
  //   url: 'https://besaba.us10.list-manage.com/subscribe/post?u=e8d650c0df90e716c22ae4778&amp;id=54a7906900'
  // });

  // function mailchimpCallback(resp) {
  //   if (resp.result === 'success') {
  //     $('.notify').find('.form').addClass('is-hidden');
  //     $('.notify').find('.subscription-ok').addClass('is-visible');
  //     setTimeout(function () {
  //       // Done Functions
  //       $('.notify').find('.subscription-ok').removeClass('is-visible');
  //       $('.notify').find('.form').delay(300).removeClass('is-hidden');
  //       $('.notify-form').trigger("reset");
  //     }, 5000);
  //   } else if (resp.result === 'error') {
  //     $('.notify').find('.form').addClass('is-hidden');
  //     $('.notify').find('.subscription-error').addClass('is-visible');
  //     setTimeout(function () {
  //       // Done Functions
  //       $('.notify').find('.subscription-error').removeClass('is-visible');
  //       $('.notify').find('.form').delay(300).removeClass('is-hidden');
  //       $('.notify-form').trigger("reset");
  //     }, 5000);
  //   }
  // };
  // --------------------------------------------- //
  // Mailchimp Notify Form End
  // --------------------------------------------- //

  function debounce(func, delay = 300) {
    let timeoutId;
    return function () {
      const context = this;
      const args = arguments;
      clearTimeout(timeoutId);
      timeoutId = setTimeout(function () {
        func.apply(context, args);
      }, delay);
    };
  }

  // --------------------------------------------- //
  // Notify Form Start
  // --------------------------------------------- //
  $("#notify-form").submit(function () { //Change
    debounce(function () {
      console.log("Started submitting notfication form...");
      var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
      var th = $("#notify-form");
      console.log("Form data serialized: ", th.serialize());
      // Add the loader overlay on the form to prevent any further
      // clicks until the request completes
      th.find("#notify-loading-overlay").removeClass("d-none").addClass("visible");
      // Change the text of the Submit button
      th.find("#notify-submit-btn .btn-caption").text("Sending...");
      $.ajax({
        type: "POST",
        url: window.endpoints && window.endpoints["submitNotificationDetails"] ? window.endpoints["submitNotificationDetails"] : "/404",
        headers: {
          'X-CSRFToken': csrftoken
        },
        data: th.serialize(),
        success: function () {
          console.log("Successfully submitted form!")
          // On successful form submission, 
          var th = $("#notify-form");

          th.queue(function (next) {

            // Step 1
            $(this).delay(1000).queue(function (next) {
              // (a): Change button text to Sent and icon to Check
              $(this).find("#notify-submit-btn .btn-caption").text("Sent!");
              $(this).find("#notify-submit-btn i").removeClass("ph-paper-plane").addClass("ph-check-fat");

              // (b) Hide the spinner
              $(this).find("#notify-spinner").addClass("hidden");

              next();
            });

            // Step 2: Wait for the hide animation to complete, then
            $(this).delay(600).queue(function (next) {
              // (a) Set display to none
              $(this).find("#notify-spinner").addClass("d-none");
              // (b) Show the tick sign
              $(this).find("#notify-tick").removeClass("d-none").addClass("visible");

              next();
            });

            // Step 3:
            $(this).delay(1000).queue(function (next) {
              // (a): Show the success message
              // Hide the form
              $(this).addClass("is-hidden");

              // Show the success reply
              $('.notify').find('.subscription-ok').addClass("is-visible");

              next();
            });

            $(this).delay(1000).queue(function (next) {
              // (b) Reset
              // Reset all the loader, spinner, tick to their original classes

              // Reset loading-overlay
              $(this).find("#notify-loading-overlay").removeClass("visible").addClass("d-none");

              // Reset submit button
              $(this).find("#notify-submit-btn .btn-caption").text("Submit");
              $(this).find("#notify-submit-btn i").removeClass("ph-check-fat").addClass("ph-paper-plane");

              // Reset spinner
              $(this).find("#notify-spinner").removeClass("hidden d-none");

              // Reset tick
              $(this).find("#notify-tick").removeClass("visible").addClass("d-none");

              next();
            });

            // Step 4:
            $(this).delay(5000).queue(function (next) {
              // Done Functions
              var th = $("#notify-form");
              $('.notify').find('.subscription-ok').removeClass('is-visible');
              th.delay(300).removeClass('is-hidden');
              th.trigger("reset");
              $("#notify-close").click();
              next();
            });


            next();
          });
        },
        error: function () {
          // Error handling
          console.log('Error submitting form');

          var th = $("#contact-form");

          th.queue(function (next) {
            // Step 1
            $(this).delay(1000).queue(function (next) {
              // (a): Change button text to Sent and icon to Check
              $(this).find("#notify-submit-btn .btn-caption").text("Error!");
              $(this).find("#notify-submit-btn i").removeClass("ph-paper-plane").addClass("ph-x");

              // (b) Hide the spinner
              $(this).find("#notify-spinner").addClass("hidden");

              next();
            });

            // Step 2: Wait for the hide animation to complete, then
            $(this).delay(600).queue(function (next) {
              // (a) Set display to none
              $(this).find("#notify-spinner").addClass("d-none");
              // (b) Show the tick sign
              $(this).find("#notify-cross").removeClass("d-none").addClass("visible");

              next();
            });

            // Step 3:
            $(this).delay(1000).queue(function (next) {
              // (a): Show the success message
              // Hide the form
              $(this).addClass("is-hidden");

              // Show the success reply
              $('.notify').find('.subscription-error').addClass('is-visible');

              next();
            });

            // Step 4:
            $(this).delay(1000).queue(function (next) {
              // (b) Reset
              // Reset all the loader, spinner, tick to their original classes

              // Reset loading-overlay
              $(this).find("#notify-loading-overlay").removeClass("visible").addClass("d-none");

              // Reset submit button
              $(this).find("#notify-submit-btn .btn-caption").text("Submit");
              $(this).find("#notify-submit-btn i").removeClass("ph-check-fat").addClass("ph-paper-plane");

              // Reset spinner
              $(this).find("#notify-spinner").removeClass("hidden d-none");

              // Reset tick
              $(this).find("#notify-cross").removeClass("visible").addClass("d-none");

              next();
            });

            next();
          });
        }
      });
    })();
    // --------------------------------------------- //
    // Notify Form End
    // --------------------------------------------- //

    // --------------------------------------------- //
    // Contact Form Start
    // --------------------------------------------- //

    $("#contact-form").submit(function () { //Change
      debounce(function () {
        console.log("Started submitting form...");
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        var th = $("#contact-form");
        console.log("Form data serialized: ", th.serialize());
        // Add the loader overlay on the form to prevent any further
        // clicks until the request completes
        th.find("#loading-overlay").removeClass("d-none").addClass("visible");
        // Change the text of the Submit button
        th.find("#submit-button .btn-caption").text("Sending...");
        $.ajax({
          type: "POST",
          url: window.endpoints && window.endpoints["submitContactDetails"] ? window.endpoints["submitContactDetails"] : "/404",
          headers: {
            'X-CSRFToken': csrftoken
          },
          data: th.serialize(),
          success: function () {
            console.log("Successfully submitted form!")
            // On successful form submission, 
            var th = $("#contact-form");

            th.queue(function (next) {

              // Step 1
              $(this).delay(1000).queue(function (next) {
                // (a): Change button text to Sent and icon to Check
                $(this).find("#submit-button .btn-caption").text("Sent!");
                $(this).find("#submit-button i").removeClass("ph-paper-plane").addClass("ph-check-fat");

                // (b) Hide the spinner
                $(this).find("#spinner").addClass("hidden");

                next();
              });

              // Step 2: Wait for the hide animation to complete, then
              $(this).delay(600).queue(function (next) {
                // (a) Set display to none
                $(this).find("#spinner").addClass("d-none");
                // (b) Show the tick sign
                $(this).find("#tick").removeClass("d-none").addClass("visible");

                next();
              });

              // Step 3:
              $(this).delay(1000).queue(function (next) {
                // (a): Show the success message
                // Hide the form
                $(this).addClass("is-hidden");

                // Show the success reply
                $("#success-reply").addClass("is-visible z-3");

                next();
              });

              $(this).delay(1000).queue(function (next) {
                // (b) Reset
                // Reset all the loader, spinner, tick to their original classes

                // Reset loading-overlay
                $(this).find("#loading-overlay").removeClass("visible").addClass("d-none");

                // Reset submit button
                $(this).find("#submit-button .btn-caption").text("Submit");
                $(this).find("#submit-button i").removeClass("ph-check-fat").addClass("ph-paper-plane");

                // Reset spinner
                $(this).find("#spinner").removeClass("hidden d-none");

                // Reset tick
                $(this).find("#tick").removeClass("visible").addClass("d-none");

                next();
              });

              // Step 4:
              $(this).delay(5000).queue(function (next) {
                // Done Functions
                var th = $("#contact-form");
                $("#success-reply").removeClass('is-visible z-3');
                th.delay(300).removeClass('is-hidden');
                th.trigger("reset");
                next();
              });


              next();
            });
          },
          error: function () {
            // Error handling
            console.log('Error submitting form');

            var th = $("#contact-form");

            th.queue(function (next) {
              // Step 1
              $(this).delay(1000).queue(function (next) {
                // (a): Change button text to Sent and icon to Check
                $(this).find("#submit-button .btn-caption").text("Error!");
                $(this).find("#submit-button i").removeClass("ph-paper-plane").addClass("ph-x");

                // (b) Hide the spinner
                $(this).find("#spinner").addClass("hidden");

                next();
              });

              // Step 2: Wait for the hide animation to complete, then
              $(this).delay(600).queue(function (next) {
                // (a) Set display to none
                $(this).find("#spinner").addClass("d-none");
                // (b) Show the tick sign
                $(this).find("#cross").removeClass("d-none").addClass("visible");

                next();
              });

              // Step 3:
              $(this).delay(1000).queue(function (next) {
                // (a): Show the success message
                // Hide the form
                $(this).addClass("is-hidden");

                // Show the success reply
                $("#failure-reply").addClass("is-visible z-3");

                next();
              });

              // Step 4:
              $(this).delay(1000).queue(function (next) {
                // (b) Reset
                // Reset all the loader, spinner, tick to their original classes

                // Reset loading-overlay
                $(this).find("#loading-overlay").removeClass("visible").addClass("d-none");

                // Reset submit button
                $(this).find("#submit-button .btn-caption").text("Submit");
                $(this).find("#submit-button i").removeClass("ph-check-fat").addClass("ph-paper-plane");

                // Reset spinner
                $(this).find("#spinner").removeClass("hidden d-none");

                // Reset tick
                $(this).find("#cross").removeClass("visible").addClass("d-none");

                next();
              });

              next();
            });
          }
        });
      })();
      // $.ajax({
      //   type: "POST",
      //   url: "mail.php", //Change
      //   data: th.serialize()
      // }).done(function () {
      //   $('.contact').find('.form').addClass('is-hidden');
      //   $('.contact').find('.reply-group').addClass('is-visible');
      //   setTimeout(function () {
      //     // Done Functions
      //     $('.contact').find('.reply-group').removeClass('is-visible');
      //     $('.contact').find('.form').delay(300).removeClass('is-hidden');
      //     th.trigger("reset");
      //   }, 5000);
      // });
      return false;
    });
    // --------------------------------------------- //
    // Contact Form End
    // --------------------------------------------- //

    // --------------------------------------------- //
    // ParticlesJS Backgrounds Start
    // --------------------------------------------- //
    // Triangles BG - particlesJS
    var bgndTriangles = $('#triangles-js');
    if (bgndTriangles.length) {
      particlesJS('triangles-js', {
        "particles": {
          "number": {
            "value": 33,
            "density": {
              "enable": true,
              "value_area": 1420.4657549380909
            }
          },
          "color": {
            "value": "#ffffff"
          },
          "shape": {
            "type": "triangle",
            "stroke": {
              "width": 0,
              "color": "#000000"
            },
            "polygon": {
              "nb_sides": 5
            },
            "image": {
              "src": "img/github.svg",
              "width": 100,
              "height": 100
            }
          },
          "opacity": {
            "value": 0.06313181133058181,
            "random": false,
            "anim": {
              "enable": false,
              "speed": 1,
              "opacity_min": 0.1,
              "sync": false
            }
          },
          "size": {
            "value": 11.83721462448409,
            "random": true,
            "anim": {
              "enable": false,
              "speed": 40,
              "size_min": 0.1,
              "sync": false
            }
          },
          "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.4,
            "width": 1
          },
          "move": {
            "enable": true,
            "speed": 4,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": false,
            "attract": {
              "enable": false,
              "rotateX": 600,
              "rotateY": 1200
            }
          }
        },
        "interactivity": {
          "detect_on": "canvas",
          "events": {
            "onhover": {
              "enable": true,
              "mode": "repulse"
            },
            "onclick": {
              "enable": true,
              "mode": "push"
            },
            "resize": true
          },
          "modes": {
            "grab": {
              "distance": 400,
              "line_linked": {
                "opacity": 1
              }
            },
            "bubble": {
              "distance": 400,
              "size": 40,
              "duration": 2,
              "opacity": 8,
              "speed": 3
            },
            "repulse": {
              "distance": 200,
              "duration": 0.4
            },
            "push": {
              "particles_nb": 4
            },
            "remove": {
              "particles_nb": 2
            }
          }
        },
        "retina_detect": true
      });
    };

    // Particles BG - particlesJS
    var bgndParticles = $('#particles-js');
    if (bgndParticles.length) {
      particlesJS('particles-js', {
        "particles": {
          "number": {
            "value": 60,
            "density": {
              "enable": true,
              "value_area": 800
            }
          },
          "color": {
            "value": "#ffffff"
          },
          "shape": {
            "type": "circle",
            "stroke": {
              "width": 0,
              "color": "#000000"
            },
            "polygon": {
              "nb_sides": 5
            },
            "image": {
              "src": "img/github.svg",
              "width": 100,
              "height": 100
            }
          },
          "opacity": {
            "value": 0.5,
            "random": false,
            "anim": {
              "enable": false,
              "speed": 1,
              "opacity_min": 0.1,
              "sync": false
            }
          },
          "size": {
            "value": 3,
            "random": true,
            "anim": {
              "enable": false,
              "speed": 40,
              "size_min": 0.1,
              "sync": false
            }
          },
          "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.4,
            "width": 1
          },
          "move": {
            "enable": true,
            "speed": 4,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": false,
            "attract": {
              "enable": false,
              "rotateX": 600,
              "rotateY": 1200
            }
          }
        },
        "interactivity": {
          "detect_on": "canvas",
          "events": {
            "onhover": {
              "enable": true,
              "mode": "repulse"
            },
            "onclick": {
              "enable": true,
              "mode": "push"
            },
            "resize": true
          },
          "modes": {
            "grab": {
              "distance": 400,
              "line_linked": {
                "opacity": 1
              }
            },
            "bubble": {
              "distance": 400,
              "size": 40,
              "duration": 2,
              "opacity": 8,
              "speed": 3
            },
            "repulse": {
              "distance": 200,
              "duration": 0.4
            },
            "push": {
              "particles_nb": 4
            },
            "remove": {
              "particles_nb": 2
            }
          }
        },
        "retina_detect": true
      });
    };
    // --------------------------------------------- //
    // ParticlesJS Backgrounds End
    // --------------------------------------------- //

  });
