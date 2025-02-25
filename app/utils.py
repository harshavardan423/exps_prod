import requests
from flask import render_template_string
from app.templates import BASE_TEMPLATE
import datetime

def render_page(username, title, content, instance_status=None):
    return render_template_string(
        BASE_TEMPLATE, 
        username=username,
        title=title,
        content=content,
        instance_status=instance_status
    )


def fetch_local_data(instance, data_type, params=None):
    """
    Fetch data from instance cache or return cached data
    
    Args:
        instance: ExposedInstance object
        data_type: Type of data to fetch ('home_data', 'files_data', 'behaviors_data')
        params: Optional parameters for the request
    
    Returns:
        tuple: (data, is_fresh)
    """
    now = datetime.utcnow()
    
    # Get the cached data based on data_type
    cached_data = None
    if data_type == 'home_data':
        cached_data = instance.home_data
    elif data_type == 'files_data':
        cached_data = instance.files_data
    elif data_type == 'behaviors_data':
        cached_data = instance.behaviors_data

    # Check if we have a recent heartbeat (within last 2 minutes)
    is_fresh = False
    if instance.last_heartbeat:
        time_since_heartbeat = (now - instance.last_heartbeat).total_seconds()
        is_fresh = time_since_heartbeat < 120  # 2 minutes

    # If we have cached data, return it
    if cached_data is not None:
        return cached_data, is_fresh

    # If no cached data, return empty structure
    empty_data = {
        'home_data': {},
        'files_data': {'structure': {'folders': [], 'files': []}},
        'behaviors_data': {'behaviors': [], 'sequences': []}
    }
    
    return empty_data.get(data_type, {}), is_fresh



def check_access(instance, request):
    """Check if current user has access to the instance"""
    # Get email from query params
    user_email = request.args.get('email')
    
    # Try to fetch allowed_users from local instance
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
        print(f"Error checking access: {e}")
    
    # If we can't get the allowed users list, default to allowing access
    # You might want to change this based on your security requirements
    return True

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

def get_dummy_files(path=''):
    """Generate dummy file structure based on path"""
    # Mock file system structure
    root = {
        'documents': {
            'type': 'folder',
            'children': {
                'reports': {
                    'type': 'folder',
                    'children': {
                        'q1_report.pdf': {'type': 'file', 'size': '2.3 MB', 'modified': '2025-02-01'},
                        'q2_report.pdf': {'type': 'file', 'size': '3.1 MB', 'modified': '2025-02-15'},
                    }
                },
                'project_proposal.docx': {'type': 'file', 'size': '546 KB', 'modified': '2025-01-20'},
                'budget.xlsx': {'type': 'file', 'size': '1.2 MB', 'modified': '2025-02-10'},
            }
        },
        'images': {
            'type': 'folder',
            'children': {
                'profile.jpg': {'type': 'file', 'size': '1.5 MB', 'modified': '2025-01-15'},
                'background.png': {'type': 'file', 'size': '2.8 MB', 'modified': '2025-01-22'},
            }
        },
        'code': {
            'type': 'folder',
            'children': {
                'projects': {
                    'type': 'folder',
                    'children': {
                        'atom': {
                            'type': 'folder',
                            'children': {
                                'main.py': {'type': 'file', 'size': '4.2 KB', 'modified': '2025-02-18'},
                                'utils.py': {'type': 'file', 'size': '2.7 KB', 'modified': '2025-02-18'},
                                'config.json': {'type': 'file', 'size': '1.3 KB', 'modified': '2025-02-17'},
                            }
                        }
                    }
                },
                'snippets': {
                    'type': 'folder',
                    'children': {
                        'script.js': {'type': 'file', 'size': '1.8 KB', 'modified': '2025-02-05'},
                        'style.css': {'type': 'file', 'size': '3.4 KB', 'modified': '2025-02-08'},
                    }
                }
            }
        },
        'notes.txt': {'type': 'file', 'size': '12 KB', 'modified': '2025-02-20'},
        'README.md': {'type': 'file', 'size': '5 KB', 'modified': '2025-01-10'},
    }
    
    # Default return value if path is not found
    result = {'folders': [], 'files': []}
    
    # Navigate to the requested path
    if not path:
        current = root
    else:
        parts = path.strip('/').split('/')
        current = root
        try:
            for part in parts:
                if part in current and current[part]['type'] == 'folder':
                    current = current[part]['children']
                else:
                    # Path not found, return empty structure
                    return result
        except (KeyError, TypeError):
            # Handle any navigation errors
            return result
    
    # Convert the current directory structure to the response format
    folders = []
    files = []
    
    for name, item in current.items():
        if item['type'] == 'folder':
            folders.append({
                'name': name,
                'modified': '2025-02-20'  # Default date for folders
            })
        else:
            files.append({
                'name': name,
                'size': item['size'],
                'modified': item['modified'],
                'icon': get_file_icon(name)
            })
    
    result = {
        'folders': sorted(folders, key=lambda x: x['name']),
        'files': sorted(files, key=lambda x: x['name'])
    }
    
    return result
