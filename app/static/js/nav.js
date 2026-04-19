document.addEventListener('DOMContentLoaded', function () {
    var btn  = document.getElementById('atom-mobile-btn');
    var menu = document.getElementById('atom-mobile-menu');
    if (btn && menu) {
        btn.addEventListener('click', function () {
            menu.classList.toggle('open');
            var icon = btn.querySelector('i');
            icon.className = menu.classList.contains('open') ? 'fas fa-times' : 'fas fa-bars';
        });
    }
});