$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location.href = $(this).data("href");
    });
});