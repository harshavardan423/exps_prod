import requests
from flask import render_template_string, session
from app.templates import BASE_TEMPLATE

def render_page(username, title, content, instance_status=None):
    return render_template_string(
        BASE_TEMPLATE, 
        username=username,
        title=title,
        content=content,
        instance_status=instance_status
    )

def fetch_local_data(instance, endpoint, params=None):
    try:
        url = f"{instance.local_url}/api/{endpoint}"
        response = requests.get(
            url,
            params=params,
            timeout=5
        )
        if response.ok:
            return response.json(), True
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {e}")
    return None, False

def check_access(instance, request):
    """Check if current user has access to the instance"""
    
    # First check if email is already in session
    user_email = session.get('verified_email')
    
    # If not in session, check query params
    if not user_email:
        user_email = request.args.get('email')
        
        # If email provided in query, store it in session for future requests
        if user_email:
            session['verified_email'] = user_email
    
    # If still no email, check if access control is even enabled
    if not user_email:
        # Try to fetch allowed_users to see if access control is enabled
        try:
            response = requests.get(f"{instance.local_url}/api/allowed_users", timeout=3)
            if response.ok:
                allowed_users = response.json().get('allowed_users', [])
                # If no allowed users set, allow access without email
                if not allowed_users:
                    return True
        except Exception as e:
            print(f"Error checking access from local instance: {e}")
        
        # Check stored allowed_users as fallback
        if hasattr(instance, 'allowed_users') and instance.allowed_users:
            if not instance.allowed_users:  # Empty list
                return True
        else:
            # No allowed_users data available, allow access
            return True
        
        # Access control is enabled but no email provided
        return False
    
    # We have an email, now check if it's allowed
    # First, try to fetch allowed_users from local instance (for most up-to-date data)
    try:
        response = requests.get(f"{instance.local_url}/api/allowed_users", timeout=3)
        if response.ok:
            allowed_users = response.json().get('allowed_users', [])
            # If no allowed users set, allow all access
            if not allowed_users:
                return True
            # Check if user email is in allowed users
            return user_email in allowed_users
    except Exception as e:
        print(f"Error checking access from local instance: {e}")
    
    # If we couldn't fetch from local instance, use stored allowed_users
    if hasattr(instance, 'allowed_users') and instance.allowed_users:
        # If no allowed users set, allow all access
        if not instance.allowed_users:
            return True
        # Check if user email is in allowed users
        return user_email in instance.allowed_users
    
    # If we have no allowed users data, default to allowing access
    return True

def get_current_user_email():
    """Get the currently verified email from session"""
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
