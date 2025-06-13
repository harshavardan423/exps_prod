import requests
from flask import render_template_string, session
from app.templates import BASE_TEMPLATE

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
