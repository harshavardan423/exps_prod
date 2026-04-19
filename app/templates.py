# Contains all your HTML templates (BASE_TEMPLATE, INDEX_TEMPLATE, FILE_EXPLORER_TEMPLATE, BEHAVIORS_TEMPLATE, ALLOWED_USERS_TEMPLATE, EMAIL_VERIFICATION_TEMPLATE)
# HTML Templates

# ─────────────────────────────────────────────────────────────
#  Shared CSS injected into every page
# ─────────────────────────────────────────────────────────────
_SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:          #07070a;
    --bg2:         #0e0e14;
    --bg3:         #16161e;
    --surface:     rgba(22,22,30,0.85);
    --surface2:    rgba(28,28,38,0.9);
    --border:      rgba(255,255,255,0.07);
    --border-h:    rgba(45,212,168,0.3);
    --teal:        #2dd4a8;
    --teal-dim:    #1a7a62;
    --teal-glow:   rgba(45,212,168,0.12);
    --text:        #ededf0;
    --text-dim:    #9898a8;
    --text-muted:  #56566a;
    --red:         #f87171;
    --yellow:      #fbbf24;
    --blue:        #60a5fa;
    --radius:      18px;
    --radius-sm:   12px;
    --radius-xs:   8px;
    --font:        'Syne', sans-serif;
    --mono:        'JetBrains Mono', monospace;
    --nav-h:       60px;
    --shadow:      0 8px 32px rgba(0,0,0,0.5);
    --shadow-teal: 0 0 28px rgba(45,212,168,0.1);
}

html { scroll-behavior: smooth; }
body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--teal-dim); border-radius: 8px; }

/* ── Nav ── */
.atom-nav {
    position: sticky; top: 0; z-index: 100;
    height: var(--nav-h);
    background: rgba(7,7,10,0.92);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center;
    padding: 0 clamp(14px,4vw,36px);
}
.atom-nav__brand {
    display: flex; align-items: center; gap: 10px;
    text-decoration: none; flex-shrink: 0;
}
.atom-nav__logo { width: 34px; height: 34px; border-radius: 10px; }
.atom-nav__title { font-size: 16px; font-weight: 700; color: var(--text); letter-spacing: -0.02em; }
.atom-nav__links { display: flex; align-items: center; gap: 2px; margin-left: 28px; }
.atom-nav__link {
    display: flex; align-items: center; gap: 6px;
    padding: 5px 13px; border-radius: 30px;
    font-size: 13px; font-weight: 500; color: var(--text-dim);
    text-decoration: none; transition: all 0.18s;
    border: 1px solid transparent;
}
.atom-nav__link:hover { color: var(--teal); background: var(--teal-glow); border-color: var(--border-h); }
.atom-nav__spacer { flex: 1; }
.atom-nav__user { display: flex; align-items: center; gap: 10px; }
.atom-nav__email {
    font-size: 12px; color: var(--text-dim);
    font-family: var(--mono);
    max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.atom-nav__logout {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 5px 12px; border-radius: 20px; font-size: 12px;
    font-family: var(--mono); font-weight: 500;
    background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.25);
    color: var(--red); text-decoration: none; transition: all 0.18s; cursor: pointer;
}
.atom-nav__logout:hover { background: rgba(248,113,113,0.2); }
.atom-nav__mobile-btn {
    display: none; background: none; border: none;
    color: var(--text-dim); font-size: 20px; cursor: pointer; padding: 4px;
}
.atom-nav__mobile-menu {
    display: none; position: fixed;
    top: var(--nav-h); left: 0; right: 0;
    background: rgba(7,7,10,0.97); backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--border);
    padding: 12px; z-index: 99;
    flex-direction: column; gap: 3px;
}
.atom-nav__mobile-menu.open { display: flex; }
.atom-nav__mobile-link {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px; border-radius: var(--radius-xs);
    color: var(--text-dim); text-decoration: none;
    font-size: 14px; font-weight: 500; transition: all 0.15s;
}
.atom-nav__mobile-link:hover { color: var(--teal); background: var(--teal-glow); }

@media (max-width: 768px) {
    .atom-nav__links { display: none; }
    .atom-nav__email { display: none; }
    .atom-nav__mobile-btn { display: block; }
}

/* ── Page shell ── */
.page-shell { max-width: 1160px; margin: 0 auto; padding: clamp(20px,4vw,44px) clamp(14px,4vw,36px); }

/* ── Page header ── */
.page-header { margin-bottom: 28px; }
.page-header__eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 3px 12px; background: var(--teal-glow);
    border: 1px solid var(--border-h); border-radius: 20px;
    font-size: 10px; font-family: var(--mono); color: var(--teal);
    margin-bottom: 10px; letter-spacing: 0.06em; text-transform: uppercase;
}
.page-header__title { font-size: clamp(22px,4vw,32px); font-weight: 800; letter-spacing: -0.03em; color: var(--text); line-height: 1.1; }
.page-header__sub { margin-top: 6px; font-size: 14px; color: var(--text-dim); }

/* ── Card ── */
.card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); backdrop-filter: blur(12px);
    box-shadow: var(--shadow); overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.card--hover:hover { border-color: var(--border-h); box-shadow: var(--shadow), var(--shadow-teal); }
.card__header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 22px; background: rgba(0,0,0,0.2);
    border-bottom: 1px solid var(--border);
}
.card__header-title { font-size: 13px; font-weight: 600; color: var(--text); display: flex; align-items: center; gap: 8px; }
.card__body { padding: 22px; }

/* ── Pill ── */
.pill {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-family: var(--mono); font-weight: 500;
    border: 1px solid transparent;
}
.pill--teal   { background: rgba(45,212,168,0.1);  border-color: rgba(45,212,168,0.25);  color: var(--teal); }
.pill--blue   { background: rgba(96,165,250,0.1);  border-color: rgba(96,165,250,0.25);  color: var(--blue); }
.pill--yellow { background: rgba(251,191,36,0.1);   border-color: rgba(251,191,36,0.25);   color: var(--yellow); }
.pill--red    { background: rgba(248,113,113,0.1);  border-color: rgba(248,113,113,0.25);  color: var(--red); }
.pill--gray   { background: rgba(255,255,255,0.05); border-color: var(--border);           color: var(--text-dim); }

/* ── Buttons ── */
.btn {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 18px; border-radius: 30px;
    font-size: 13px; font-weight: 600; font-family: var(--font);
    border: 1px solid transparent; cursor: pointer;
    transition: all 0.18s; text-decoration: none; line-height: 1;
}
.btn--primary { background: var(--teal-dim); border-color: rgba(45,212,168,0.3); color: var(--text); }
.btn--primary:hover { background: #1f8c6e; }
.btn--ghost { background: rgba(255,255,255,0.04); border-color: var(--border); color: var(--text-dim); }
.btn--ghost:hover { background: rgba(255,255,255,0.08); color: var(--text); border-color: rgba(255,255,255,0.14); }

/* ── Status dot ── */
.status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.status-dot--green  { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
.status-dot--yellow { background: var(--yellow); box-shadow: 0 0 6px var(--yellow); }

/* ── Form ── */
.form-input {
    width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--border);
    border-radius: var(--radius-xs); padding: 10px 14px; color: var(--text);
    font-size: 14px; font-family: var(--font); transition: border-color 0.18s; outline: none;
}
.form-input:focus { border-color: var(--border-h); }
.form-input::placeholder { color: var(--text-muted); }

/* ── Modal ── */
.modal-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.72); backdrop-filter: blur(6px);
    z-index: 200; align-items: center; justify-content: center; padding: 16px;
}
.modal-overlay.open { display: flex; }
.modal {
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: var(--radius); width: 100%; max-width: 500px;
    box-shadow: var(--shadow); overflow: hidden;
}
.modal__header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 22px; background: rgba(0,0,0,0.2); border-bottom: 1px solid var(--border);
}
.modal__title { font-size: 14px; font-weight: 700; color: var(--text); }
.modal__close { background: none; border: none; color: var(--text-muted); font-size: 17px; cursor: pointer; transition: color 0.15s; padding: 2px; }
.modal__close:hover { color: var(--text); }
.modal__body { padding: 22px; display: flex; flex-direction: column; gap: 14px; }
.modal__footer { display: flex; justify-content: flex-end; gap: 10px; padding: 14px 22px; border-top: 1px solid var(--border); }

/* ── Status bar ── */
.status-bar {
    margin-top: 18px; padding: 11px 16px; border-radius: var(--radius-sm);
    display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 500; border: 1px solid transparent;
}
.status-bar--online  { background: rgba(34,197,94,0.08);  border-color: rgba(34,197,94,0.2);  color: #4ade80; }
.status-bar--offline { background: rgba(251,191,36,0.08); border-color: rgba(251,191,36,0.2); color: var(--yellow); }

/* ── Empty state ── */
.empty-state { text-align: center; padding: 56px 24px; color: var(--text-muted); }
.empty-state__icon { font-size: 44px; margin-bottom: 14px; opacity: 0.35; }
.empty-state__title { font-size: 17px; font-weight: 700; color: var(--text-dim); margin-bottom: 6px; }
.empty-state__text { font-size: 13px; }
"""

_SHARED_JS = """
<script>
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
</script>
"""

_NAV_INSTANCE = """
<nav class="atom-nav">
    <a href="/{{ username }}/home" class="atom-nav__brand">
        <img src="{{ url_for('static', filename='images/atom2.gif') }}" alt="Atom" class="atom-nav__logo">
        <span class="atom-nav__title">{{ username }}'s Atom</span>
    </a>
    <div class="atom-nav__links">
        <a href="/{{ username }}/home"      class="atom-nav__link"><i class="fas fa-home"></i> Home</a>
        <a href="/{{ username }}/files"     class="atom-nav__link"><i class="fas fa-folder"></i> Files</a>
        <a href="/{{ username }}/behaviors" class="atom-nav__link"><i class="fas fa-cogs"></i> Behaviors</a>
        <a href="/{{ username }}/chat"      class="atom-nav__link"><i class="fas fa-comments"></i> Chat</a>
    </div>
    <div class="atom-nav__spacer"></div>
    <div class="atom-nav__user">
        {% if current_user_email %}
        <span class="atom-nav__email"><i class="fas fa-user-circle" style="color:var(--teal);margin-right:5px;"></i>{{ current_user_email }}</span>
        <a href="/{{ username }}/logout" class="atom-nav__logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
        {% endif %}
        <button class="atom-nav__mobile-btn" id="atom-mobile-btn"><i class="fas fa-bars"></i></button>
    </div>
</nav>
<div class="atom-nav__mobile-menu" id="atom-mobile-menu">
    <a href="/{{ username }}/home"      class="atom-nav__mobile-link"><i class="fas fa-home"     style="width:16px;"></i> Home</a>
    <a href="/{{ username }}/files"     class="atom-nav__mobile-link"><i class="fas fa-folder"   style="width:16px;"></i> Files</a>
    <a href="/{{ username }}/behaviors" class="atom-nav__mobile-link"><i class="fas fa-cogs"     style="width:16px;"></i> Behaviors</a>
    <a href="/{{ username }}/chat"      class="atom-nav__mobile-link"><i class="fas fa-comments" style="width:16px;"></i> Chat</a>
    {% if current_user_email %}
    <div style="margin-top:8px;padding:10px 14px;border-top:1px solid var(--border);font-size:12px;color:var(--text-muted);">
        <i class="fas fa-user-circle" style="color:var(--teal);margin-right:6px;"></i>{{ current_user_email }}
    </div>
    <a href="/{{ username }}/logout" class="atom-nav__mobile-link" style="color:var(--red);"><i class="fas fa-sign-out-alt" style="width:16px;"></i> Logout</a>
    {% endif %}
</div>
"""

BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title }} — {{ username }}'s Atom</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>""" + _SHARED_CSS + """</style>
</head>
<body>
""" + _NAV_INSTANCE + """
<div class="page-shell">
    <div class="page-header">
        <div class="page-header__title">{{ title }}</div>
        {% if subtitle %}<div class="page-header__sub">{{ subtitle }}</div>{% endif %}
    </div>
    <div class="card"><div class="card__body">{{ content | safe }}</div></div>
    {% if instance_status %}
    <div class="status-bar status-bar--{% if instance_status == 'online' %}online{% else %}offline{% endif %}">
        <span class="status-dot status-dot--{% if instance_status == 'online' %}green{% else %}yellow{% endif %}"></span>
        Instance: {% if instance_status == 'online' %}Online{% else %}Offline (cached data){% endif %}
    </div>
    {% endif %}
</div>
""" + _SHARED_JS + """
</body>
</html>"""


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Atom Exposure Server</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>
""" + _SHARED_CSS + """
.hero {
    padding: clamp(48px,8vw,96px) clamp(14px,4vw,36px) clamp(28px,5vw,56px);
    text-align: center; position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 55% at 50% 0%, rgba(45,212,168,0.09) 0%, transparent 70%);
    pointer-events: none;
}
.hero__eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 14px; background: var(--teal-glow); border: 1px solid var(--border-h);
    border-radius: 20px; font-size: 11px; font-family: var(--mono); color: var(--teal);
    margin-bottom: 18px; letter-spacing: 0.05em;
}
.hero__title { font-size: clamp(30px,6vw,52px); font-weight: 800; letter-spacing: -0.04em; color: var(--text); line-height: 1.06; margin-bottom: 10px; }
.hero__sub { font-size: 15px; color: var(--text-dim); max-width: 400px; margin: 0 auto; }
.instances-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 14px; padding: 0 clamp(14px,4vw,36px) clamp(28px,4vw,56px);
    max-width: 1160px; margin: 0 auto;
}
.instance-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
    padding: 22px; transition: all 0.22s; text-decoration: none; display: block;
    position: relative; overflow: hidden;
}
.instance-card::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, var(--teal-glow) 0%, transparent 60%);
    opacity: 0; transition: opacity 0.22s; pointer-events: none;
}
.instance-card:hover { border-color: var(--border-h); transform: translateY(-3px); box-shadow: var(--shadow), var(--shadow-teal); }
.instance-card:hover::after { opacity: 1; }
.instance-card__icon {
    width: 42px; height: 42px; background: rgba(45,212,168,0.1); border: 1px solid rgba(45,212,168,0.2);
    border-radius: 12px; display: flex; align-items: center; justify-content: center;
    font-size: 19px; color: var(--teal); margin-bottom: 14px;
}
.instance-card__name { font-size: 17px; font-weight: 700; color: var(--text); margin-bottom: 3px; letter-spacing: -0.02em; }
.instance-card__label { font-size: 11px; color: var(--text-muted); font-family: var(--mono); margin-bottom: 18px; }
.instance-card__cta { display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 600; color: var(--teal); }
</style>
</head>
<body>
<nav class="atom-nav">
    <a href="/" class="atom-nav__brand">
        <img src="{{ url_for('static', filename='images/atom2.gif') }}" alt="Atom" class="atom-nav__logo">
        <span class="atom-nav__title">Atom Server</span>
    </a>
    <div class="atom-nav__spacer"></div>
    <span class="pill pill--gray"><i class="fas fa-server"></i> Exposure Server</span>
</nav>
<div class="hero">
    <div class="hero__eyebrow"><i class="fas fa-circle" style="font-size:8px;"></i> Live</div>
    <h1 class="hero__title">Atom Exposure<br>Server</h1>
    <p class="hero__sub">Active Atom instances running on this node</p>
</div>
{% if instances %}
<div class="instances-grid">
    {% for instance in instances %}
    <a href="/{{ instance.username }}/home" class="instance-card">
        <div class="instance-card__icon"><i class="fas fa-atom"></i></div>
        <div class="instance-card__name">{{ instance.username }}</div>
        <div class="instance-card__label">atom://instance</div>
        <div class="instance-card__cta">View Instance <i class="fas fa-arrow-right"></i></div>
    </a>
    {% endfor %}
</div>
{% else %}
<div style="max-width:420px;margin:0 auto;padding:0 16px 56px;">
    <div class="card"><div class="card__body">
        <div class="empty-state">
            <div class="empty-state__icon"><i class="fas fa-atom"></i></div>
            <div class="empty-state__title">No Active Instances</div>
            <div class="empty-state__text">No Atom instances are currently registered on this server.</div>
        </div>
    </div></div>
</div>
{% endif %}
</body>
</html>"""


ALLOWED_USERS_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Allowed Users — Atom Server</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>""" + _SHARED_CSS + """</style>
</head>
<body>
<nav class="atom-nav">
    <a href="/" class="atom-nav__brand">
        <img src="{{ url_for('static', filename='images/atom2.gif') }}" alt="Atom" class="atom-nav__logo">
        <span class="atom-nav__title">Atom Server</span>
    </a>
    <div class="atom-nav__spacer"></div>
    <span class="pill pill--teal"><i class="fas fa-users"></i> Access Control</span>
</nav>
<div class="page-shell" style="max-width:820px;">
    <div class="page-header">
        <div class="page-header__eyebrow"><i class="fas fa-shield-halved"></i> Access Control</div>
        <div class="page-header__title">Allowed Users</div>
        <div class="page-header__sub">Manage user access to Atom instances</div>
    </div>
    <div class="card"><div class="card__body">{{ content | safe }}</div></div>
</div>
</body>
</html>"""


EMAIL_VERIFICATION_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Email Verification — Atom Server</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<style>
""" + _SHARED_CSS + """
.verify-wrap {
    min-height: 100vh; display: flex; align-items: center;
    justify-content: center; padding: 24px;
    background: radial-gradient(ellipse 80% 55% at 50% 0%, rgba(45,212,168,0.06) 0%, transparent 60%);
}
.verify-box { width: 100%; max-width: 440px; }
.verify-icon {
    width: 54px; height: 54px; background: rgba(45,212,168,0.1);
    border: 1px solid rgba(45,212,168,0.2); border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; color: var(--teal); margin: 0 auto 20px;
}
.verify-title { text-align: center; font-size: 24px; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 5px; }
.verify-sub { text-align: center; font-size: 13px; color: var(--text-dim); margin-bottom: 24px; }
</style>
</head>
<body>
<nav class="atom-nav">
    <a href="/" class="atom-nav__brand">
        <img src="{{ url_for('static', filename='images/atom2.gif') }}" alt="Atom" class="atom-nav__logo">
        <span class="atom-nav__title">Atom Server</span>
    </a>
    <div class="atom-nav__spacer"></div>
    <span class="pill pill--teal"><i class="fas fa-envelope"></i> Verification</span>
</nav>
<div class="verify-wrap">
    <div class="verify-box">
        <div class="verify-icon"><i class="fas fa-envelope-open-text"></i></div>
        <div class="verify-title">Email Verification</div>
        <div class="verify-sub">Verify your email to access Atom instances</div>
        <div class="card"><div class="card__body">{{ content | safe }}</div></div>
    </div>
</div>
</body>
</html>"""

BEHAVIORS_TEMPLATE = """
<style>
/* ---- List style for behaviors and sequences ---- */
.beh-list, .seq-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.seq-item, .beh-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    transition: border-color 0.2s, background 0.2s;
}
.seq-item:hover, .beh-item:hover {
    border-color: var(--border-h);
    background: rgba(255,255,255,0.03);
}
.beh-icon, .seq-icon {
    width: 32px;
    height: 32px;
    background: rgba(45,212,168,0.07);
    border: 1px solid rgba(45,212,168,0.14);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--teal);
    font-size: 14px;
    flex-shrink: 0;
}
.beh-info, .seq-info {
    flex: 1;
    min-width: 0;
}
.beh-name, .seq-name {
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 2px;
}
.beh-trigger, .seq-meta {
    font-size: 10px;
    font-family: var(--mono);
    color: var(--text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.beh-actions, .seq-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}
/* Toggle switch (same as in create_connection.html) */
.toggle-label {
    cursor: pointer;
    flex-shrink: 0;
}
.toggle-input {
    display: none;
}
.toggle-track {
    display: block;
    width: 36px;
    height: 20px;
    background: rgba(255,255,255,0.08);
    border: 1px solid var(--border-med);
    border-radius: 10px;
    position: relative;
    transition: background 0.2s, border-color 0.2s;
}
.toggle-track::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 14px;
    height: 14px;
    background: var(--text-sec);
    border-radius: 50%;
    transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1), background 0.2s;
}
.toggle-input:checked + .toggle-track {
    background: rgba(45,212,168,0.18);
    border-color: rgba(45,212,168,0.4);
}
.toggle-input:checked + .toggle-track::after {
    transform: translateX(16px);
    background: var(--accent-bright);
}
/* Play button */
.play-btn {
    width: 30px;
    height: 30px;
    background: var(--accent);
    border: 1px solid rgba(45,212,168,0.18);
    color: var(--text-pri);
    cursor: pointer;
    border-radius: 50%;
    font-size: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.15s, transform 0.1s;
    flex-shrink: 0;
}
.play-btn:hover:not(:disabled) {
    background: var(--accent-mid);
    transform: scale(1.08);
}
.play-btn:disabled {
    cursor: default;
}
.play-btn.playing {
    background: rgba(45,212,168,0.12);
    border-color: rgba(45,212,168,0.3);
    color: var(--accent-bright);
}
.play-btn.done {
    background: rgba(80,220,130,0.12);
    border-color: rgba(80,220,130,0.35);
    color: var(--online);
}
.section-title-sm {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-sec);
    margin-bottom: 12px;
    padding: 0 4px;
}
</style>

<div>
    {% if behaviors_data.behaviors and behaviors_data.behaviors|length > 0 %}
    <div class="section-title-sm"><i class="fas fa-brain" style="margin-right:6px;"></i> Behaviors</div>
    <div class="beh-list">
        {% for beh in behaviors_data.behaviors %}
        <div class="beh-item">
            <div class="beh-icon"><i class="fas fa-bolt"></i></div>
            <div class="beh-info">
                <div class="beh-name">{{ beh.name }}</div>
                <div class="beh-trigger">{{ beh.trigger }}</div>
            </div>
            <div class="beh-actions">
                <label class="toggle-label">
                    <input type="checkbox" class="toggle-input beh-toggle" data-behavior="{{ beh.name }}" {% if beh.active %}checked{% endif %}>
                    <span class="toggle-track"></span>
                </label>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if behaviors_data.sequences and behaviors_data.sequences|length > 0 %}
    <div class="section-title-sm" style="margin-top:24px;"><i class="fas fa-play-circle" style="margin-right:6px;"></i> Sequences</div>
    <div class="seq-list">
        {% for seq in behaviors_data.sequences %}
        <div class="seq-item">
            <div class="seq-icon"><i class="fas fa-play"></i></div>
            <div class="seq-info">
                <div class="seq-name">{{ seq.name }}</div>
                <div class="seq-meta">{{ seq.steps }} steps · {{ seq.desc }}</div>
            </div>
            <div class="seq-actions">
                <button class="play-btn seq-run" data-sequence="{{ seq.name }}"><i class="fas fa-play"></i></button>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if (not behaviors_data.behaviors or behaviors_data.behaviors|length == 0) and (not behaviors_data.sequences or behaviors_data.sequences|length == 0) %}
    <div class="empty-state">
        <div class="empty-state__icon"><i class="fas fa-cogs"></i></div>
        <div class="empty-state__title">No Behaviors or Sequences</div>
        <div class="empty-state__text">This instance has no configured behaviors or sequences.</div>
    </div>
    {% endif %}
</div>

<script>
(function() {
    var username = '{{ username }}';

    // Behavior toggle
    document.querySelectorAll('.beh-toggle').forEach(function(toggle) {
        toggle.addEventListener('change', function(e) {
            e.stopPropagation();
            var behName = this.dataset.behavior;
            var isActive = this.checked;
            var url = isActive ? '/activate_behavior' : '/deactivate_behavior';
            fetch('/' + username + url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: behName })
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!data.success) {
                    alert(data.error || 'Failed to ' + (isActive ? 'activate' : 'deactivate') + ' behavior');
                    toggle.checked = !isActive;
                }
            })
            .catch(function(err) {
                alert('Error: ' + err.message);
                toggle.checked = !isActive;
            });
        });
    });

    // Run sequence
    document.querySelectorAll('.seq-run').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            var seqName = this.dataset.sequence;
            var originalHtml = this.innerHTML;
            this.disabled = true;
            this.classList.add('playing');
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            fetch('/' + username + '/run_sequence', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: seqName })
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.error) throw new Error(data.error);
                btn.classList.remove('playing');
                btn.classList.add('done');
                btn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(function() {
                    btn.classList.remove('done');
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                }, 1500);
            })
            .catch(function(err) {
                btn.classList.remove('playing');
                btn.innerHTML = '<i class="fas fa-times"></i>';
                alert('Error: ' + err.message);
                setTimeout(function() {
                    btn.innerHTML = originalHtml;
                    btn.disabled = false;
                }, 1500);
            });
        });
    });
})();
</script>
"""

FILE_EXPLORER_TEMPLATE = """
<style>
.fe-toolbar { display: flex; align-items: center; justify-content: space-between; padding: 0 0 18px; gap: 12px; flex-wrap: wrap; }
.fe-breadcrumb {
    display: flex; align-items: center; gap: 4px; font-size: 12px; font-family: var(--mono);
    background: rgba(0,0,0,0.2); border: 1px solid var(--border); border-radius: 30px;
    padding: 6px 14px; flex-wrap: wrap; flex: 1; min-width: 0;
}
.fe-breadcrumb a { color: var(--teal); text-decoration: none; }
.fe-breadcrumb a:hover { text-decoration: underline; }
.fe-breadcrumb .sep { color: var(--text-muted); }
.fe-actions { display: flex; gap: 8px; flex-shrink: 0; }

.fe-table { width: 100%; border-collapse: collapse; }
.fe-table th {
    text-align: left; font-size: 10px; font-family: var(--mono); color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.07em;
    padding: 9px 16px; background: rgba(0,0,0,0.15); border-bottom: 1px solid var(--border);
}
.fe-table td { border-bottom: 1px solid rgba(255,255,255,0.04); vertical-align: middle; }
.fe-table tr:last-child td { border-bottom: none; }
.fe-table tr:hover td { background: rgba(255,255,255,0.02); }

.fe-row {
    display: flex; align-items: center; gap: 10px; padding: 10px 16px;
    text-decoration: none; color: var(--text); font-size: 13px; transition: color 0.15s;
    cursor: pointer; border: none; background: none; width: 100%; text-align: left; font-family: var(--font);
}
.fe-row:hover { color: var(--teal); }
.fe-row__icon { font-size: 14px; flex-shrink: 0; width: 18px; text-align: center; }
.fe-row__name { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fe-row__meta { font-size: 11px; font-family: var(--mono); color: var(--text-muted); flex-shrink: 0; }
.fe-sec-head {
    font-size: 9px; font-family: var(--mono); color: var(--text-muted); text-transform: uppercase;
    letter-spacing: 0.08em; padding: 7px 16px 4px;
    background: rgba(0,0,0,0.1); border-bottom: 1px solid rgba(255,255,255,0.04);
}

/* File viewer */
.fv-overlay {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.78); backdrop-filter: blur(8px);
    z-index: 300; align-items: flex-start; justify-content: center;
    padding: 20px 12px; overflow-y: auto;
}
.fv-overlay.open { display: flex; }
.fv-modal {
    background: var(--bg3); border: 1px solid var(--border); border-radius: var(--radius);
    width: 100%; max-width: 800px; box-shadow: var(--shadow); overflow: hidden; margin: auto;
}
.fv-modal__head {
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    padding: 13px 18px; background: rgba(0,0,0,0.25); border-bottom: 1px solid var(--border); flex-wrap: wrap;
}
.fv-modal__name { font-size: 13px; font-weight: 700; color: var(--text); word-break: break-all; flex: 1; }
.fv-modal__actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.fv-modal__body { padding: 18px; max-height: 68vh; overflow: auto; }
.fv-modal__body pre {
    background: rgba(0,0,0,0.3); border: 1px solid var(--border); border-radius: var(--radius-sm);
    padding: 14px; font-family: var(--mono); font-size: 12px; color: var(--text);
    overflow: auto; white-space: pre-wrap; word-break: break-word;
}
.fv-tabs { display: flex; gap: 4px; margin-bottom: 12px; }
.fv-tab {
    padding: 5px 13px; border-radius: 20px; font-size: 12px; font-weight: 600;
    border: 1px solid var(--border); background: none; color: var(--text-dim);
    cursor: pointer; transition: all 0.15s; font-family: var(--font);
}
.fv-tab.active { background: var(--teal-glow); border-color: var(--border-h); color: var(--teal); }
</style>

<div>
    <div class="fe-toolbar">
        <div class="fe-breadcrumb">
            <i class="fas fa-folder-open" style="color:var(--teal);"></i>
            <a href="/{{ username }}/files">root</a>
            {% if current_path %}
                {% set path_parts = current_path.split('/') %}
                {% set ns = namespace(acc='') %}
                {% for part in path_parts %}
                    {% if part %}
                        {% if ns.acc %}{% set ns.acc = ns.acc + '/' + part %}{% else %}{% set ns.acc = part %}{% endif %}
                        <span class="sep">/</span>
                        <a href="/{{ username }}/files?path={{ ns.acc | urlencode }}">{{ part }}</a>
                    {% endif %}
                {% endfor %}
            {% endif %}
        </div>
        <div class="fe-actions">
            <button class="btn btn--ghost" onclick="showUploadModal()"><i class="fas fa-upload"></i> Upload</button>
            <button class="btn btn--ghost" onclick="showNewFolderModal()"><i class="fas fa-folder-plus"></i> Folder</button>
        </div>
    </div>

    <div class="card" style="overflow:hidden;">
        <table class="fe-table">
            <thead>
                <tr>
                    <th style="width:54%;">Name</th>
                    <th style="width:16%;text-align:center;">Size</th>
                    <th style="width:30%;text-align:right;padding-right:18px;">Modified</th>
                </tr>
            </thead>
            <tbody>
                {% if current_path %}
                <tr>
                    <td><a href="/{{ username }}/files{% if parent_path %}?path={{ parent_path|urlencode }}{% endif %}" class="fe-row">
                        <span class="fe-row__icon"><i class="fas fa-arrow-up" style="color:var(--text-muted);"></i></span>
                        <span class="fe-row__name">..</span>
                    </a></td>
                    <td></td><td></td>
                </tr>
                {% endif %}

                {% if file_data.folders %}
                <tr><td colspan="3"><div class="fe-sec-head">Folders</div></td></tr>
                {% for item in file_data.folders %}
                    {% if current_path %}{% set fp = current_path + '/' + item.name %}{% else %}{% set fp = item.name %}{% endif %}
                <tr>
                    <td><a href="/{{ username }}/files?path={{ fp|urlencode }}" class="fe-row">
                        <span class="fe-row__icon"><i class="fas fa-folder" style="color:#fbbf24;"></i></span>
                        <span class="fe-row__name">{{ item.name }}</span>
                    </a></td>
                    <td style="padding:0 16px;text-align:center;"><span class="pill pill--gray">dir</span></td>
                    <td style="padding-right:18px;text-align:right;"><span class="fe-row__meta">{{ item.modified }}</span></td>
                </tr>
                {% endfor %}
                {% endif %}

                {% if file_data.files %}
                <tr><td colspan="3"><div class="fe-sec-head">Files</div></td></tr>
                {% for item in file_data.files %}
                    {% if current_path %}{% set fp = current_path + '/' + item.name %}{% else %}{% set fp = item.name %}{% endif %}
                <tr>
                    <td><button class="fe-row" onclick="viewFile('{{ fp|e }}')">
                        <span class="fe-row__icon"><i class="{{ item.icon }}" style="color:var(--text-dim);"></i></span>
                        <span class="fe-row__name">{{ item.name }}</span>
                    </button></td>
                    <td style="padding:0 16px;text-align:center;"><span class="fe-row__meta">{{ item.size }}</span></td>
                    <td style="padding-right:18px;text-align:right;"><span class="fe-row__meta">{{ item.modified }}</span></td>
                </tr>
                {% endfor %}
                {% endif %}

                {% if not file_data.folders and not file_data.files %}
                <tr><td colspan="3">
                    <div class="empty-state">
                        <div class="empty-state__icon"><i class="fas fa-folder-open"></i></div>
                        <div class="empty-state__title">Empty Directory</div>
                        <div class="empty-state__text">Upload files or create folders to get started.</div>
                    </div>
                </td></tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>

<!-- File viewer -->
<div id="fv-overlay" class="fv-overlay" onclick="if(event.target===this)closeFileViewer()">
    <div class="fv-modal">
        <div class="fv-modal__head">
            <span id="fv-name" class="fv-modal__name"></span>
            <div class="fv-modal__actions">
                <a id="fv-download" href="#" class="btn btn--ghost" style="font-size:12px;padding:6px 14px;"><i class="fas fa-download"></i> Download</a>
                <button class="btn btn--ghost" style="padding:6px 10px;" onclick="closeFileViewer()"><i class="fas fa-times"></i></button>
            </div>
        </div>
        <div class="fv-modal__body"><div id="fv-content"></div></div>
    </div>
</div>

<!-- Upload modal -->
<div id="uploadModal" class="modal-overlay" onclick="if(event.target===this)closeUploadModal()">
    <div class="modal">
        <div class="modal__header">
            <span class="modal__title"><i class="fas fa-upload" style="color:var(--teal);margin-right:8px;"></i>Upload Files</span>
            <button class="modal__close" onclick="closeUploadModal()"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal__body">
            <div>
                <label style="font-size:11px;color:var(--text-dim);font-family:var(--mono);display:block;margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">Select Files</label>
                <input type="file" id="fileInput" multiple style="width:100%;background:rgba(0,0,0,0.3);border:1px solid var(--border);border-radius:var(--radius-xs);padding:9px 12px;color:var(--text);font-size:13px;font-family:var(--font);">
            </div>
            <div style="font-size:11px;color:var(--text-muted);font-family:var(--mono);background:rgba(0,0,0,0.2);padding:8px 12px;border-radius:var(--radius-xs);border:1px solid var(--border);">
                <i class="fas fa-folder" style="color:var(--yellow);margin-right:6px;"></i>/{{ current_path if current_path else 'root' }}
            </div>
            <div id="uploadStatus" style="font-size:13px;min-height:20px;"></div>
        </div>
        <div class="modal__footer">
            <button class="btn btn--ghost" onclick="closeUploadModal()">Cancel</button>
            <button class="btn btn--primary" onclick="uploadFiles()"><i class="fas fa-upload"></i> Upload</button>
        </div>
    </div>
</div>

<!-- New Folder modal -->
<div id="newFolderModal" class="modal-overlay" onclick="if(event.target===this)closeNewFolderModal()">
    <div class="modal">
        <div class="modal__header">
            <span class="modal__title"><i class="fas fa-folder-plus" style="color:var(--yellow);margin-right:8px;"></i>New Folder</span>
            <button class="modal__close" onclick="closeNewFolderModal()"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal__body">
            <div>
                <label style="font-size:11px;color:var(--text-dim);font-family:var(--mono);display:block;margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">Folder Name</label>
                <input type="text" id="folderNameInput" class="form-input" placeholder="my-folder" autocomplete="off">
            </div>
            <div style="font-size:11px;color:var(--text-muted);font-family:var(--mono);background:rgba(0,0,0,0.2);padding:8px 12px;border-radius:var(--radius-xs);border:1px solid var(--border);">
                <i class="fas fa-folder" style="color:var(--yellow);margin-right:6px;"></i>/{{ current_path if current_path else 'root' }}
            </div>
        </div>
        <div class="modal__footer">
            <button class="btn btn--ghost" onclick="closeNewFolderModal()">Cancel</button>
            <button class="btn btn--primary" onclick="createFolder()"><i class="fas fa-folder-plus"></i> Create</button>
        </div>
    </div>
</div>

<script>
var currentPath = '{{ current_path|e }}';
var username    = '{{ username|e }}';

function viewFile(filePath) {
    fetch('/' + username + '/file-content/' + encodeURIComponent(filePath))
        .then(function(r) { if (!r.ok) throw new Error('Not available'); return r.json(); })
        .then(function(data) { displayFileContent(data, filePath); })
        .catch(function(err) {
            document.getElementById('fv-name').textContent = filePath.split('/').pop();
            document.getElementById('fv-content').innerHTML =
                '<div style="text-align:center;color:var(--red);padding:32px;"><i class="fas fa-exclamation-triangle" style="font-size:28px;margin-bottom:10px;display:block;"></i>Failed: ' + err.message + '</div>';
            document.getElementById('fv-overlay').classList.add('open');
        });
}

function displayFileContent(data, filePath) {
    document.getElementById('fv-name').textContent = data.filename;
    var contentDiv = document.getElementById('fv-content');

    var dl = document.getElementById('fv-download');
    var newDl = dl.cloneNode(true);
    dl.parentNode.replaceChild(newDl, dl);
    document.getElementById('fv-download').addEventListener('click', function(e) {
        e.preventDefault();
        try {
            var bin;
            var isText = data.mime_type && (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || data.mime_type === 'application/javascript');
            if (isText) { try { bin = atob(data.content); } catch(x) { bin = String.fromCharCode.apply(null, new TextEncoder().encode(data.content)); } }
            else { bin = atob(data.content); }
            var bytes = new Uint8Array(bin.length);
            for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            var blob = new Blob([bytes], { type: data.mime_type || 'application/octet-stream' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a'); a.href = url; a.download = data.filename;
            document.body.appendChild(a); a.click();
            setTimeout(function() { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
        } catch(err) { alert('Download failed: ' + err.message); }
    });

    if (data.filename.endsWith('.html') || data.mime_type === 'text/html') {
        contentDiv.innerHTML = '<div class="fv-tabs"><button class="fv-tab active" id="tab-raw" onclick="switchTab(\'raw\')">Raw</button><button class="fv-tab" id="tab-render" onclick="openRendered()">Rendered <i class="fas fa-external-link-alt" style="font-size:10px;"></i></button></div><div id="fv-raw"><pre>' + escHtml(data.content) + '</pre></div>';
        window._currentHtml = data.content;
    } else if (data.mime_type && data.mime_type.startsWith('image/')) {
        contentDiv.innerHTML = '<div style="text-align:center;"><img src="data:' + data.mime_type + ';base64,' + data.content + '" style="max-width:100%;max-height:60vh;border-radius:var(--radius-sm);"></div>';
    } else if (data.mime_type && (data.mime_type.startsWith('text/') || data.mime_type === 'application/json' || data.mime_type === 'application/javascript')) {
        contentDiv.innerHTML = '<pre>' + escHtml(data.content) + '</pre>';
    } else {
        contentDiv.innerHTML = '<div style="text-align:center;padding:28px;color:var(--text-dim);"><i class="fas fa-file" style="font-size:36px;margin-bottom:10px;display:block;opacity:.35;"></i><div style="font-family:var(--mono);font-size:11px;">' + data.mime_type + '</div><div style="margin-top:8px;font-size:13px;">Use the download button to save this file.</div></div>';
    }
    document.getElementById('fv-overlay').classList.add('open');
}

function switchTab(t) {
    var raw = document.getElementById('fv-raw');
    if (raw) raw.style.display = t === 'raw' ? '' : 'none';
    var tabRaw = document.getElementById('tab-raw');
    if (tabRaw) tabRaw.classList.toggle('active', t === 'raw');
}
function openRendered() {
    if (window._currentHtml) { var w = window.open('','_blank'); w.document.write(window._currentHtml); w.document.close(); }
}
function closeFileViewer() {
    document.getElementById('fv-overlay').classList.remove('open');
    document.getElementById('fv-content').innerHTML = '';
}
function escHtml(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function showUploadModal()  { document.getElementById('uploadModal').classList.add('open'); document.getElementById('uploadStatus').innerHTML = ''; }
function closeUploadModal() { document.getElementById('uploadModal').classList.remove('open'); document.getElementById('fileInput').value = ''; }

function uploadFiles() {
    var files = document.getElementById('fileInput').files;
    if (!files.length) { document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--red)">Select at least one file</span>'; return; }
    var fd = new FormData();
    for (var i = 0; i < files.length; i++) fd.append('file', files[i]);
    fd.append('path', currentPath);
    document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--teal)"><i class="fas fa-spinner fa-spin"></i> Uploading…</span>';
    fetch('/' + username + '/api/upload', { method: 'POST', body: fd })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') {
                document.getElementById('uploadStatus').innerHTML = '<span style="color:#4ade80"><i class="fas fa-check"></i> Done!</span>';
                setTimeout(function() { location.reload(); }, 1100);
            } else {
                document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--red)">Error: ' + (data.error||'Unknown') + '</span>';
            }
        })
        .catch(function(err) { document.getElementById('uploadStatus').innerHTML = '<span style="color:var(--red)">' + err.message + '</span>'; });
}

function showNewFolderModal()  { document.getElementById('newFolderModal').classList.add('open'); document.getElementById('folderNameInput').value = ''; }
function closeNewFolderModal() { document.getElementById('newFolderModal').classList.remove('open'); }

function createFolder() {
    var name = document.getElementById('folderNameInput').value.trim();
    if (!name) { alert('Please enter a folder name'); return; }
    var fd = new FormData();
    fd.append('path', currentPath);
    fd.append('folder', JSON.stringify({ name: name }));
    fetch('/' + username + '/api/upload', { method: 'POST', body: fd })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.status === 'success') { closeNewFolderModal(); location.reload(); }
            else { alert('Failed: ' + (data.error||'Unknown error')); }
        })
        .catch(function(err) { alert('Error: ' + err.message); });
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') { closeFileViewer(); closeUploadModal(); closeNewFolderModal(); }
});
</script>
"""


CHAT_LIST_TEMPLATE = """
<style>
.cl-list { display: flex; flex-direction: column; gap: 10px; }
.cl-card {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 18px; background: var(--surface2); border: 1px solid var(--border);
    border-radius: var(--radius); text-decoration: none; transition: all 0.2s;
}
.cl-card:hover { border-color: var(--border-h); transform: translateX(3px); box-shadow: var(--shadow-teal); }
.cl-name { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 4px; }
.cl-meta { display: flex; gap: 8px; font-size: 11px; font-family: var(--mono); color: var(--text-muted); flex-wrap: wrap; }
.cl-count { background: rgba(45,212,168,0.1); border: 1px solid rgba(45,212,168,0.2); padding: 2px 8px; border-radius: 12px; color: var(--teal); }
.cl-arrow { color: var(--text-muted); font-size: 11px; flex-shrink: 0; }
</style>
<div class="cl-list">
    {% if sessions %}
        {% for sess in sessions %}
        <a href="/{{ username }}/chat/{{ sess.id }}" class="cl-card">
            <div>
                <div class="cl-name">{{ sess.name }}</div>
                <div class="cl-meta">
                    <span class="cl-count">{{ sess.message_count }} msgs</span>
                    <span>{{ sess.last_active[:16] }}</span>
                </div>
            </div>
            <i class="fas fa-chevron-right cl-arrow"></i>
        </a>
        {% endfor %}
    {% else %}
    <div class="empty-state">
        <div class="empty-state__icon"><i class="fas fa-comment-slash"></i></div>
        <div class="empty-state__title">No Chat Sessions</div>
        <div class="empty-state__text">Start a conversation in Atom to see sessions here.</div>
    </div>
    {% endif %}
</div>
"""


CHAT_SESSION_TEMPLATE = """
<style>
.cs-wrap {
    display: flex; flex-direction: column;
    height: calc(100vh - var(--nav-h) - 100px);
    min-height: 480px; max-height: 780px;
}
.cs-header {
    display: flex; align-items: center; gap: 12px;
    padding-bottom: 14px; border-bottom: 1px solid var(--border); flex-wrap: wrap;
}
.cs-back {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 13px; background: rgba(255,255,255,0.04); border: 1px solid var(--border);
    border-radius: 30px; font-size: 12px; font-weight: 500; color: var(--text-dim);
    text-decoration: none; transition: all 0.18s; flex-shrink: 0;
}
.cs-back:hover { border-color: var(--border-h); color: var(--teal); }
.cs-title { font-size: 15px; font-weight: 700; color: var(--text); letter-spacing: -0.02em; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.cs-messages {
    flex: 1; overflow-y: auto; padding: 18px 0; display: flex; flex-direction: column; gap: 12px;
}
.cs-messages::-webkit-scrollbar { width: 4px; }
.cs-messages::-webkit-scrollbar-thumb { background: var(--teal-dim); border-radius: 4px; }

.cs-msg { display: flex; }
.cs-msg--user      { justify-content: flex-end; }
.cs-msg--assistant { justify-content: flex-start; }

.cs-bubble {
    max-width: min(76%, 580px); padding: 10px 15px; border-radius: 18px;
    border: 1px solid var(--border); font-size: 14px; line-height: 1.5;
}
.cs-msg--user .cs-bubble { background: #0d3d35; border-color: rgba(45,212,168,0.2); border-bottom-right-radius: 5px; }
.cs-msg--assistant .cs-bubble { background: rgba(28,28,38,0.9); border-bottom-left-radius: 5px; }
.cs-bubble__text { color: var(--text); word-wrap: break-word; }
.cs-bubble__time { font-size: 10px; font-family: var(--mono); color: var(--text-muted); margin-top: 5px; text-align: right; }

.cs-input-area { padding: 14px 0 0; border-top: 1px solid var(--border); }
.cs-input-row {
    display: flex; gap: 10px; align-items: center;
    background: rgba(0,0,0,0.3); border: 1px solid var(--border);
    border-radius: 44px; padding: 4px 4px 4px 16px; transition: border-color 0.18s;
}
.cs-input-row:focus-within { border-color: var(--border-h); }
.cs-input {
    flex: 1; background: transparent; border: none; color: var(--text);
    font-size: 14px; font-family: var(--font); outline: none; padding: 9px 0;
}
.cs-input::placeholder { color: var(--text-muted); font-size: 13px; }
.cs-send {
    background: var(--teal-dim); border: 1px solid rgba(45,212,168,0.25); border-radius: 36px;
    padding: 8px 16px; font-size: 13px; font-weight: 700; color: var(--text);
    cursor: pointer; transition: all 0.15s; font-family: var(--font);
    display: flex; align-items: center; gap: 6px; flex-shrink: 0;
}
.cs-send:hover { background: #1f8c6e; }
.cs-send:active { transform: scale(0.97); }
</style>

<div class="cs-wrap">
    <div class="cs-header">
        <a href="/{{ username }}/chat" class="cs-back"><i class="fas fa-arrow-left"></i> Back</a>
        <div class="cs-title">{{ session.name }}</div>
    </div>

    <div id="cs-messages" class="cs-messages">
        {% for msg in session.messages %}
        <div class="cs-msg cs-msg--{{ msg.role }}">
            <div class="cs-bubble">
                <div class="cs-bubble__text">{{ msg.content }}</div>
                <div class="cs-bubble__time">{{ msg.timestamp[:16] if msg.timestamp else '' }}</div>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="cs-input-area">
        <form id="cs-form">
            <div class="cs-input-row">
                <input type="text" id="cs-input" class="cs-input" placeholder="Type a message…" autocomplete="off">
                <button type="submit" class="cs-send"><i class="fas fa-paper-plane"></i> Send</button>
            </div>
        </form>
    </div>
</div>

<script>
var sessionId = "{{ session_id }}";
var username  = "{{ username }}";
var msgs      = document.getElementById('cs-messages');
var form      = document.getElementById('cs-form');
var input     = document.getElementById('cs-input');

function scrollBottom() { msgs.scrollTop = msgs.scrollHeight; }

function escHtml(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function renderMessages(list) {
    msgs.innerHTML = '';
    list.forEach(function(m) {
        var d = document.createElement('div');
        d.className = 'cs-msg cs-msg--' + m.role;
        d.innerHTML = '<div class="cs-bubble"><div class="cs-bubble__text">' + escHtml(m.content) +
            '</div><div class="cs-bubble__time">' + (m.timestamp ? m.timestamp.slice(0,16) : '') + '</div></div>';
        msgs.appendChild(d);
    });
    scrollBottom();
}

function refresh() {
    fetch('/' + username + '/chat/' + sessionId + '/messages', { headers: { 'Accept': 'application/json' }})
        .then(function(r) { if (r.ok) return r.json(); })
        .then(function(data) { if (data && data.messages) renderMessages(data.messages); })
        .catch(function() {});
}

form.addEventListener('submit', function(e) {
    e.preventDefault();
    var msg = input.value.trim();
    if (!msg) return;
    input.value = '';
    var d = document.createElement('div');
    d.className = 'cs-msg cs-msg--user';
    d.innerHTML = '<div class="cs-bubble"><div class="cs-bubble__text">' + escHtml(msg) +
        '</div><div class="cs-bubble__time">' + new Date().toISOString().slice(0,16) + '</div></div>';
    msgs.appendChild(d);
    scrollBottom();
    fetch('/' + username + '/chat/' + sessionId + '/send', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    }).then(function(r) {
        if (!r.ok) { refresh(); }
        else { setTimeout(refresh, 1500); }
    });
});

fetch('/' + username + '/chat/' + sessionId + '/messages', { method: 'HEAD' })
    .then(function(r) {
        if (r.ok) { setInterval(refresh, 3000); refresh(); }
        else { setInterval(function() { location.reload(); }, 4000); }
    })
    .catch(function() { setInterval(function() { location.reload(); }, 4000); });

scrollBottom();
</script>
"""