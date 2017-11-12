$(function() {
    var gnav = $('.right-panel-gnav');
    var viewmain = $('.view-main');
    var gnavbtn = $('.right-panel-gnav-btn');
    $('.right-panel-gnav-btn').on('click', function() {
        $('.right-panel-gnav-btn').toggleClass('is-open');
        $('.right-panel-gnav').toggleClass('on');
        $('.view-main').toggleClass('on');
    });
});
