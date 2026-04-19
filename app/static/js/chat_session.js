var msgs = document.getElementById('cs-messages');
var form = document.getElementById('cs-form');
var input = document.getElementById('cs-input');

function scrollBottom() { msgs.scrollTop = msgs.scrollHeight; }

function escHtml(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderMessages(list) {
    msgs.innerHTML = '';
    list.forEach(function (m) {
        var d = document.createElement('div');
        d.className = 'cs-msg cs-msg--' + m.role;
        d.innerHTML = '<div class="cs-bubble"><div class="cs-bubble__text">' + escHtml(m.content) +
            '</div><div class="cs-bubble__time">' + (m.timestamp ? m.timestamp.slice(0, 16) : '') + '</div></div>';
        msgs.appendChild(d);
    });
    scrollBottom();
}

function refresh() {
    fetch('/' + ATOM_USERNAME + '/chat/' + ATOM_SESSION_ID + '/messages', { headers: { 'Accept': 'application/json' } })
        .then(function (r) { if (r.ok) return r.json(); })
        .then(function (data) { if (data && data.messages) renderMessages(data.messages); })
        .catch(function () {});
}

form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = input.value.trim();
    if (!msg) return;
    input.value = '';
    var d = document.createElement('div');
    d.className = 'cs-msg cs-msg--user';
    d.innerHTML = '<div class="cs-bubble"><div class="cs-bubble__text">' + escHtml(msg) +
        '</div><div class="cs-bubble__time">' + new Date().toISOString().slice(0, 16) + '</div></div>';
    msgs.appendChild(d);
    scrollBottom();
    fetch('/' + ATOM_USERNAME + '/chat/' + ATOM_SESSION_ID + '/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    }).then(function (r) {
        if (!r.ok) { refresh(); }
        else { setTimeout(refresh, 1500); }
    });
});

fetch('/' + ATOM_USERNAME + '/chat/' + ATOM_SESSION_ID + '/messages', { method: 'HEAD' })
    .then(function (r) {
        if (r.ok) { setInterval(refresh, 3000); refresh(); }
        else { setInterval(function () { location.reload(); }, 4000); }
    })
    .catch(function () { setInterval(function () { location.reload(); }, 4000); });

scrollBottom();