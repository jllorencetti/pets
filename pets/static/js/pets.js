$(document).ready(function () {
    $('input[type="file"]').on('change', function () {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#picture').attr('src', e.target.result);
        };
        reader.readAsDataURL(this.files[0]);

        if (this.files[0].size > 8 * 1024 * 1024) {
            this.setCustomValidity('Imagem excede tamanho máximo de 8MB');
            return;
        }

        this.setCustomValidity('');
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

    var links = $('a').not('.pagination a');
    for (var i = 0; i < links.length; i++) {
        var currentPath = window.location.pathname;
        var link = links[i];
        if (link.pathname === currentPath && link.href.indexOf('#') === -1) {
            $(link.parentNode).addClass('active');
        }
    }
});

(function () {
    if (matchMedia('only screen and (min-width: 768px)').matches) {
        $(document).on('scroll', function () {
            var scrollPos = $(this).scrollTop();

            if (scrollPos > 150) {
                $('.navbar-fixed-top').removeClass('navbar-home');
            } else {
                $('.navbar-fixed-top').addClass('navbar-home');
            }
        });
    }
})();