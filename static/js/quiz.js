(function() {
    if (typeof questions === 'undefined') return;
    var current = 0;
    var answers = [];
    var total = questions.length;

    function render() {
        if (current >= total) return;
        var q = questions[current];
        var numEl = document.getElementById('currentNum');
        var totalEl = document.getElementById('totalNum');
        var textEl = document.getElementById('questionText');
        var container = document.getElementById('optionsContainer');
        var prevBtn = document.getElementById('prevBtn');
        var nextBtn = document.getElementById('nextBtn');
        var finishBtn = document.getElementById('finishBtn');
        if (!numEl || !textEl || !container) return;
        if (numEl) numEl.textContent = current + 1;
        if (totalEl) totalEl.textContent = total;
        textEl.textContent = q.question || '';
        container.innerHTML = '';
        (q.options || []).forEach(function(opt, i) {
            var label = document.createElement('label');
            var radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'opt';
            radio.value = i;
            if (answers[current] === i) radio.checked = true;
            radio.addEventListener('change', function() { answers[current] = i; });
            label.appendChild(radio);
            label.appendChild(document.createTextNode(opt));
            container.appendChild(label);
        });
        if (prevBtn) prevBtn.style.display = current === 0 ? 'none' : 'inline-block';
        if (nextBtn) nextBtn.style.display = current === total - 1 ? 'none' : 'inline-block';
        if (finishBtn) finishBtn.style.display = current === total - 1 ? 'inline-block' : 'none';
    }

    var prevBtn = document.getElementById('prevBtn');
    var nextBtn = document.getElementById('nextBtn');
    var finishBtn = document.getElementById('finishBtn');
    if (prevBtn) prevBtn.addEventListener('click', function() { if (current > 0) { current--; render(); } });
    if (nextBtn) nextBtn.addEventListener('click', function() { if (current < total - 1) { current++; render(); } });
    if (finishBtn) finishBtn.addEventListener('click', function() {
        var url = typeof submitUrl !== 'undefined' ? submitUrl : (typeof quizUrl !== 'undefined' ? quizUrl : '');
        if (!url) return;
        fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answers: answers }) })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                var go = typeof resultUrl !== 'undefined' ? resultUrl : (typeof topicId !== 'undefined' ? '/topic/' + topicId + '/quiz/result' : '');
                if (go) window.location.href = go;
            });
    });
    render();
})();
