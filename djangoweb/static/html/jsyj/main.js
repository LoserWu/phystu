$(document).ready(function () {
 
  /* ========================================================================
     On click menu item animate to the section
   ========================================================================== */
  $(".mobilenav li, .back-to-top").on('click', function() {
    var target = $(this).data('rel');
    var $target = $(target);
    $('html, body').stop().animate({
        'scrollTop': $target.offset().top
    }, 900, 'swing');
  });
  
    $('#contact-form').submit(function () {
        var Name = $("#name").val();
        var email = $("#email").val();
        var phone = $("#phone").val();
        var studentid = $("#studentid").val();
        var url ="http://127.0.0.1:8000/mail/?sub=1"+"&name="+Name+"&phone="+phone+"&email="+email+"&studentid="+studentid;
		window.open(encodeURI(url));

    });
});