$(document).ready(function() {
    /*if( localStorage.getItem('newOptions') === null || localStorage.getItem('newOptions') === true ) {
        myApp.popup('.popup-splash');
        localStorage.setItem('newOptions', true);
    }*/

    /*if($('.chart-content').length > 0) {
        var obj = document.querySelector(".chart-content");
        var ctx = obj.getContext("2d");

        showLineChart(ctx);
    }

    if($('.line-chart-content').length > 0) {
        var obj = document.querySelector(".line-chart-content");
        var ctx = obj.getContext("2d");

        showLineChartPage(ctx);
    }

    if($('.bar-chart-content').length > 0) {
        var obj = document.querySelector(".bar-chart-content");
        var ctx = obj.getContext("2d");

        showBarChartPage(ctx);
    }

    if($('.pie-chart-content').length > 0) {
        var obj = document.querySelector(".pie-chart-content");
        var ctx = obj.getContext("2d");

        showPieChartPage(ctx);
    }

    if($('.doughnut-chart-content').length > 0) {
        var obj = document.querySelector(".doughnut-chart-content");
        var ctx = obj.getContext("2d");

        showDoughnutChartPage(ctx);
    }

    if($('.radar-chart-content').length > 0) {
        var obj = document.querySelector(".radar-chart-content");
        var ctx = obj.getContext("2d");

        showRadarChartPage(ctx);
    }

    if($('.polar-chart-content').length > 0) {
        var obj = document.querySelector(".polar-chart-content");
        var ctx = obj.getContext("2d");

        showPolarChartPage(ctx);
    }

    naxvarBg();*/

    $('.js-toggle-menu').on('click', function() {
        $(this).next().slideToggle(200);
        $(this).find('span').toggleClass('icon-chevron-down').toggleClass('icon-chevron-up');
    });

    /*$('body').on('click', '.js-gallery-col', function() {
        var cols = $(this).data('cols');
        $('.gallery-list').attr({ 'data-cols' : cols });

        $('.js-gallery-col').removeClass('active');
        $(this).addClass('active');
    });*/

    setTimeout(function() {
        //videoInit();
        //teamSlider();
    }, 100);
});

function videoInit() {
    var videoBg = findElement('.play-bg-video');

    if(videoBg.length > 0) {
        videoBg.vide('assets/video/video');
    }
}

function teamSlider() {
    var owl = findElement('.team');

    owl.owlCarousel({
        singleItem : true,
        navigation : false,
        navigationText : [],
        pagination : false,
        uniqueHistory: true
    });
    findElement(".team-nav-right").click(function(){
        owl.trigger('owl.next');
    });
    findElement(".team-nav-left").click(function(){
        owl.trigger('owl.prev');
    });
}

function findElement(selector) {
    var box = null;

    if($('.page-on-center').length > 0) {
        box = $('.view-main').find('.page-on-center ' + selector);

        if(box.length === 0) {
            box = $('.view-main').find('.page-on-center' + selector);
        }

    } else {
        box = $('.view-main').find('.page').find(selector);
    }

    return box;
};

function naxvarBg() {
    var navbar = $('.navbar-anim-on-scroll'),
        box = null,
        cls = 'active';

    if(navbar.length === 0) {
        return false;
    }

    if($('.page-on-center').length > 0) {
        box = navbar.next().find('.page-on-center .page-content');
    } else {
        box = navbar.next().find('.page .page-content');
    }

    if( box.scrollTop() > 10 ) {
        navbar.addClass( cls );
    }else{
        navbar.removeClass( cls );
    }

    box.scroll(function() {
        if( $(this).scrollTop() > 40 ) {
            navbar.addClass( cls );
        }else{
            navbar.removeClass( cls );
        }
    });
}


function showLineChart(obj) {
    var data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
            {
                label               : "My dataset",
                fillColor           : "rgba(54, 133, 176, 0.2)",
                strokeColor         : "rgba(54, 133, 176, 1)",
                pointColor          : "rgba(54, 133, 176, 1)",
                pointStrokeColor    : "rgba(54, 133, 176, 1)",
                pointHighlightFill  : "rgba(255, 255, 255, 1)",
                pointHighlightStroke: "rgba(54, 133, 176, 1)",
                data: [65, 59, 80, 81, 56, 55, 40]
            }
        ]
    };

    var chart = new Chart(obj).Line(data, {
        responsive                  : true,

        pointDotRadius              : 3,
        pointDotStrokeWidth         : 1,
        datasetStrokeWidth          : 2,

        scaleFontSize               : 10,
        tooltipFontSize             : 12,

        scaleLineColor              : "rgba(0, 0, 0, 0.7)",
        scaleFontColor              : "rgba(0, 0, 0, 0.7)",

        scaleBeginAtZero            : true,
        scaleShowGridLines          : true,
        scaleShowHorizontalLines    : true,
        scaleShowVerticalLines      : false
    });

    return chart;
}

function showLineChartPage(obj) {
    var data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
            {
                label               : "My dataset",
                fillColor           : "rgba(54, 133, 176, 0.2)",
                strokeColor         : "rgba(54, 133, 176, 1)",
                pointColor          : "rgba(54, 133, 176, 1)",
                pointStrokeColor    : "rgba(54, 133, 176, 1)",
                pointHighlightFill  : "rgba(0, 0, 0, 1)",
                pointHighlightStroke: "rgba(54, 133, 176, 1)",
                data: [65, 59, 80, 81, 56, 55, 40]
            }, {
                label               : "My dataset 2",
                fillColor           : "rgba(224, 61, 14, 0.2)",
                strokeColor         : "rgba(224, 61, 14, 1)",
                pointColor          : "rgba(224, 61, 14, 1)",
                pointStrokeColor    : "rgba(224, 61, 14, 1)",
                pointHighlightFill  : "rgba(0, 0, 0, 1)",
                pointHighlightStroke: "rgba(224, 61, 14, 1)",
                data: [32, 34, 67, 12, 37, 55, 20]
            }
        ]
    };

    var chart = new Chart(obj).Line(data, {
        responsive                  : true,

        pointDotRadius              : 4,
        pointDotStrokeWidth         : 1,
        datasetStrokeWidth          : 2,

        scaleFontSize               : 10,
        tooltipFontSize             : 12,

        scaleLineColor              : "rgba(0, 0, 0, 0.7)",
        scaleFontColor              : "rgba(0, 0, 0, 0.7)",

        scaleBeginAtZero            : true,
        scaleShowGridLines          : true,
        scaleShowHorizontalLines    : true,
        scaleShowVerticalLines      : false
    });

    return chart;
}

function showBarChartPage(obj) {
    var data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
            {
                label               : "My dataset",
                fillColor           : "rgba(54, 133, 176, 0.2)",
                strokeColor         : "rgba(54, 133, 176, 1)",
                pointColor          : "rgba(54, 133, 176, 1)",
                pointStrokeColor    : "rgba(0, 0, 0, 1)",
                pointHighlightFill  : "rgba(0, 0, 0, 1)",
                pointHighlightStroke: "rgba(54, 133, 176, 1)",
                data: [65, 59, 80, 81, 56, 55, 40]
            }, {
                label               : "My dataset 2",
                fillColor           : "rgba(224, 61, 14, 0.2)",
                strokeColor         : "rgba(224, 61, 14, 1)",
                pointColor          : "rgba(224, 61, 14, 1)",
                pointStrokeColor    : "rgba(0, 0, 0, 1)",
                pointHighlightFill  : "rgba(0, 0, 0, 1)",
                pointHighlightStroke: "rgba(224, 61, 14, 1)",
                data: [32, 34, 67, 12, 37, 55, 20]
            }
        ]
    };

    var chart = new Chart(obj).Bar(data, {
        responsive                  : true,

        pointDotRadius              : 2,
        pointDotStrokeWidth         : 1,
        datasetStrokeWidth          : 1,

        scaleFontSize               : 10,
        tooltipFontSize             : 12,

        scaleLineColor              : "rgba(0, 0, 0, 0.7)",
        scaleFontColor              : "rgba(0, 0, 0, 0.7)",

        scaleBeginAtZero            : true,
        scaleShowGridLines          : true,
        scaleShowHorizontalLines    : true,
        scaleShowVerticalLines      : false
    });

    return chart;
}

function showPieChartPage(obj) {
    var data = [
        {
            value: 300,
            color: "rgba(54, 133, 176, 1)",
            highlight: "rgba(54, 133, 176, 0.5)",
            label: "Text 1"
        },
        {
            value: 50,
            color: "rgba(224, 61, 14, 1)",
            highlight: "rgba(224, 61, 14, 0.5)",
            label: "Text 2"
        },
        {
            value: 100,
            color: "#FDB45C",
            highlight: "#FFC870",
            label: "Text 3"
        }
    ]


    var chart = new Chart(obj).Pie(data, {
        responsive                  : true,
        tooltipFontSize             : 12
    });

    return chart;
}

function showDoughnutChartPage(obj) {
    var data = [
        {
            value: 300,
            color: "rgba(54, 133, 176, 1)",
            highlight: "rgba(54, 133, 176, 0.5)",
            label: "Text 1"
        },
        {
            value: 50,
            color: "rgba(224, 61, 14, 1)",
            highlight: "rgba(224, 61, 14, 0.5)",
            label: "Text 2"
        },
        {
            value: 100,
            color: "#FDB45C",
            highlight: "#FFC870",
            label: "Text 3"
        }
    ]


    var chart = new Chart(obj).Doughnut(data, {
        responsive                  : true,
        tooltipFontSize             : 12
    });

    return chart;
}

function showRadarChartPage(obj) {
    var data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
            {
                label               : "My dataset",
                fillColor           : "rgba(54, 133, 176, 0.2)",
                strokeColor         : "rgba(54, 133, 176, 1)",
                pointColor          : "rgba(54, 133, 176, 1)",
                pointStrokeColor    : "rgba(54, 133, 176, 1)",
                pointHighlightFill  : "rgba(0, 0, 0, 1)",
                pointHighlightStroke: "rgba(54, 133, 176, 1)",
                data: [65, 59, 80, 81, 56, 55, 40]
            }, {
                label               : "My dataset 2",
                fillColor           : "rgba(224, 61, 14, 0.2)",
                strokeColor         : "rgba(224, 61, 14, 1)",
                pointColor          : "rgba(224, 61, 14, 1)",
                pointStrokeColor    : "rgba(224, 61, 14, 1)",
                pointHighlightFill  : "rgba(0, 0, 0, 1)",
                pointHighlightStroke: "rgba(224, 61, 14, 1)",
                data: [32, 34, 67, 12, 37, 55, 20]
            }
        ]
    };

    var chart = new Chart(obj).Radar(data, {
        responsive                  : true,

        pointDotRadius              : 3,
        pointDotStrokeWidth         : 1,
        datasetStrokeWidth          : 2,

        scaleFontSize               : 10,
        tooltipFontSize             : 12,

        scaleLineColor              : "rgba(0, 0, 0, 0.7)",
        scaleFontColor              : "rgba(0, 0, 0, 0.7)",
        pointLabelFontColor         : "rgba(0, 0, 0, 0.7)",

        scaleBeginAtZero            : true,
        scaleShowGridLines          : true,
        scaleShowHorizontalLines    : true,
        scaleShowVerticalLines      : false
    });

    return chart;
}

function showPolarChartPage(obj) {
    var data = [
        {
            value: 300,
            color: "rgba(54, 133, 176, 1)",
            highlight: "rgba(54, 133, 176, 0.5)",
            label: "Text 1"
        },
        {
            value: 50,
            color: "rgba(224, 61, 14, 1)",
            highlight: "rgba(224, 61, 14, 0.5)",
            label: "Text 2"
        },
        {
            value: 100,
            color: "#FDB45C",
            highlight: "#FFC870",
            label: "Text 3"
        }
    ]


    var chart = new Chart(obj).PolarArea(data, {
        responsive                  : true,
        scaleFontSize               : 10,
        tooltipFontSize             : 12
    });

    return chart;
}

function hidePreloader() {
    jQuery('.page-preloader').animate({
        opacity: 0
    }, function() {
        jQuery(this).hide();
    });
}
