
function gaoActiveLink(item) {
    $(item).each(function() {
        if ($($(this))[0].href == String(window.location)) {
            $(this).parent().addClass('active');
            var $pa = $(this).parent().parent().parent();
            if ($pa.hasClass('treeview')) {
                $pa.addClass('active');
            }
            $(this).click(function() {
                return false;
            });
        } else {
            $(this).parent().removeClass('active');
        }
    });
}
