import requests
from flask import render_template_string, session


BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title }} — {{ username }}'s Atom</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static', filename='css/shared.css') }}">
</head>
<body>

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
    <span class="atom-nav__email">
      <i class="fas fa-user-circle" style="color:var(--teal);margin-right:5px;"></i>{{ current_user_email }}
    </span>
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
  <a href="/{{ username }}/logout" class="atom-nav__mobile-link" style="color:var(--red);">
    <i class="fas fa-sign-out-alt" style="width:16px;"></i> Logout
  </a>
  {% endif %}
</div>

<div class="page-shell">
  <div class="page-header">
    <div class="page-header__title">{{ title }}</div>
    {% if subtitle %}<div class="page-header__sub">{{ subtitle }}</div>{% endif %}
  </div>

  <div class="card">
    <div class="card__body">
      {{ content | safe }}
    </div>
  </div>

  {% if instance_status %}
  <div class="status-bar status-bar--{% if instance_status == 'online' %}online{% else %}offline{% endif %}">
    <span class="status-dot status-dot--{% if instance_status == 'online' %}green{% else %}yellow{% endif %}"></span>
    Instance: {% if instance_status == 'online' %}Online{% else %}Offline (cached data){% endif %}
  </div>
  {% endif %}
</div>

<script src="{{ url_for('static', filename='js/nav.js') }}"></script>
</body>
</html>"""


def render_page(username, title, content, instance_status=None, current_user_email=None):
    return render_template_string(
        BASE_TEMPLATE, 
        username=username,
        title=title,
        content=content,
        instance_status=instance_status,
        current_user_email=current_user_email or get_current_user_email()
    )

def fetch_local_data(instance, endpoint, params=None):
    try:
        url = f"{instance.local_url}/api/{endpoint}"
        print(f"Fetching data from: {url} with params: {params}")  # Debug logging
        response = requests.get(
            url,
            params=params,
            timeout=8  # Increased timeout
        )
        if response.ok:
            data = response.json()
            print(f"Successfully fetched data: {len(str(data))} chars")  # Debug logging
            return data, True
        else:
            print(f"Failed to fetch data: {response.status_code}")  # Debug logging
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {e}")
    return None, False

def check_access(instance, request):
    """Check if current user has access to the instance"""
    
    # Use instance-specific session key
    session_key = f'verified_email_{instance.username}'
    user_email = session.get(session_key)
    
    # If not in session, check query params
    if not user_email:
        user_email = request.args.get('email')
    
    # Get allowed users for this instance
    allowed_users = get_allowed_users(instance)
    
    # If no allowed users configured, require explicit configuration
    # (Don't default to allowing everyone)
    if allowed_users is None:
        print(f"No allowed users data available for {instance.username}")
        return False
    
    # If allowed users is empty list, allow all access
    if len(allowed_users) == 0:
        return True
    
    # If no email provided but access control is enabled
    if not user_email:
        return False
    
    # Check if email is allowed
    is_allowed = user_email in allowed_users
    
    # If email is valid, store it in instance-specific session
    if is_allowed:
        session[session_key] = user_email
    
    return is_allowed

def get_allowed_users(instance):
    """Get allowed users list, preferring fresh data from local instance"""
    try:
        response = requests.get(f"{instance.local_url}/api/allowed_users", timeout=3)
        if response.ok:
            return response.json().get('allowed_users', [])
    except Exception as e:
        print(f"Error fetching allowed users from local instance: {e}")
    
    # Fallback to stored data
    if hasattr(instance, 'allowed_users') and instance.allowed_users is not None:
        return instance.allowed_users
    
    # Return None if no data available (different from empty list)
    return None

def get_current_user_email():
    """Get the currently verified email from session"""
    # You might want to make this instance-specific too
    return session.get('verified_email')

def get_file_icon(filename):
    """Get appropriate Font Awesome icon for file type"""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    
    icons = {
        'pdf': 'fas fa-file-pdf text-red-500',
        'doc': 'fas fa-file-word text-blue-500',
        'docx': 'fas fa-file-word text-blue-500',
        'xls': 'fas fa-file-excel text-green-500',
        'xlsx': 'fas fa-file-excel text-green-500',
        'ppt': 'fas fa-file-powerpoint text-orange-500',
        'pptx': 'fas fa-file-powerpoint text-orange-500',
        'jpg': 'fas fa-file-image text-purple-500',
        'jpeg': 'fas fa-file-image text-purple-500',
        'png': 'fas fa-file-image text-purple-500',
        'gif': 'fas fa-file-image text-purple-500',
        'txt': 'fas fa-file-alt',
        'md': 'fas fa-file-alt',
        'py': 'fab fa-python text-blue-500',
        'js': 'fab fa-js text-yellow-500',
        'html': 'fab fa-html5 text-orange-500',
        'css': 'fab fa-css3 text-blue-500',
        'json': 'fas fa-file-code',
    }
    
    return icons.get(ext, 'fas fa-file')
