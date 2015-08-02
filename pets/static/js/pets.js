$(document).ready(function () {
    $('#profile_picture').on('change', function () {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#picture').attr('src', e.target.result);
        };
        reader.readAsDataURL(this.files[0]);
    });

    $('#new-city').on('click', function (e) {
        e.preventDefault();
        $('.new-city').show(250);
    });

    $(function () {
        $(".found-or-adopted > h2 br")
            .before("<span class='spacer'>")
            .after("<span class='spacer'>");
    });

    var links = document.getElementsByTagName('a');
    for (var i = 0; i < links.length; i++) {
        var currentPath = window.location.pathname;
        var link = links[i];
        if (link.pathname == currentPath && link.href.indexOf('#') == -1) {
            $(link.parentNode).addClass('active');
        }
    }
});