var max_width = 400;
$().reader(function() {
    $.getScript('http://services.sunlightlabs.com/brandingbar/hat_js/labs/');
    $('.post_content img').load(function(i) {
        var elem = $(this);
        if (elem.width() > max_width) {
            var r = elem.width() / elem.height();
            elem.width(max_width).height(max_width / r);
        }
    });
    $('')
});