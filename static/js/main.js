(function() {
    // Enrollment confirm modal (course detail page)
    var enrollBtn = document.getElementById('enrollBtn');
    var modal = document.getElementById('enrollModal');
    if (enrollBtn && modal) {
        var cancelBtn = document.getElementById('enrollCancel');
        var yesBtn = document.getElementById('enrollYes');
        enrollBtn.addEventListener('click', function() { modal.classList.add('active'); });
        if (cancelBtn) cancelBtn.addEventListener('click', function() { modal.classList.remove('active'); });
        if (yesBtn) yesBtn.addEventListener('click', function() {
            var courseId = enrollBtn.getAttribute('data-course-id');
            fetch('/enroll/' + courseId, { method: 'POST', headers: { 'Content-Type': 'application/json' } })
                .then(function(r) { return r.json(); })
                .then(function(data) {
                    modal.classList.remove('active');
                    if (data.ok) window.location.href = '/my-course/' + courseId;
                });
        });
    }
})();

(function() {
    // Theme toggle (light / dark)
    function applyTheme(theme) {
        var body = document.body;
        if (theme === 'dark') {
            body.classList.add('theme-dark');
        } else {
            body.classList.remove('theme-dark');
        }
    }

    var stored = localStorage.getItem('ts_theme') || 'light';
    applyTheme(stored);

    var toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.checked = (stored === 'dark');
        toggle.addEventListener('change', function() {
            var theme = toggle.checked ? 'dark' : 'light';
            localStorage.setItem('ts_theme', theme);
            applyTheme(theme);
        });
    }
})();
