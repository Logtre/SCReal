$(function() {
    var gnav = $('.left-panel-gnav');
    var viewmain = $('.view-main');
    var gnavbtn = $('.left-panel-gnav-btn');
    $('.left-panel-gnav-btn').on('click', function() {
        $('.left-panel-gnav-btn').toggleClass('is-open');
        $('.left-panel-gnav').toggleClass('on');
        $('.view-main').toggleClass('on');
    });
});
