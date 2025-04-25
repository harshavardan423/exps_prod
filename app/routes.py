from flask import jsonify, request, render_template_string
from app import app, db
from app.models import ExposedInstance
from app.utils import render_page, fetch_local_data, check_access,get_file_icon
import uuid
from datetime import datetime
from app.templates import INDEX_TEMPLATE, BASE_TEMPLATE,FILE_EXPLORER_TEMPLATE
from app.use_atom_auth import require_atom_user
import requests

# Routes
@app.route('/')
@require_atom_user
def index():
    try:
        instances = ExposedInstance.query.all()
        active_instances = [
            instance for instance in instances
            if (datetime.utcnow() - instance.last_heartbeat).total_seconds() <= 300
        ]
        
        return render_template_string(
            INDEX_TEMPLATE,
            instances=active_instances
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/<username>/home')
@require_atom_user
def user_home(username):
    instance = ExposedInstance.query.filter_by(username=username).first()
    if not instance:
        return jsonify({'error': 'User not found'}), 404

    if not check_access(instance, request):
        return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Access Required</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100">
                <div class="container mx-auto px-4 py-8">
                    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                        <h1 class="text-2xl font-bold mb-4">Access Required</h1>
                        <p class="mb-4">Please enter your email to access this instance:</p>
                        <form method="GET" class="space-y-4">
                            <input type="email" name="email" placeholder="Enter your email" 
                                    class="w-full px-3 py-2 border rounded" required>
                            <button type="submit" 
                                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                                Submit
                            </button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
        """)

    data, is_fresh = fetch_local_data(instance, 'home_data')
    if data:
        instance.home_data = data
        instance.last_data_sync = datetime.utcnow()
        db.session.commit()
    elif instance.home_data:
        data = instance.home_data
    else:
        data = {"message": "No data available"}

    # Create the connections section
    connections_section = '<div class="text-gray-500 italic">No connections configured</div>'
    if data.get('connections_data'):
        connections_section = '<div class="grid grid-cols-2 gap-3">'
        for k in data['connections_data'].keys():
            connections_section += f'<div class="bg-gray-50 p-3 rounded">{k}</div>'
        connections_section += '</div>'

    # Create the apps section
    apps_section = '<div class="text-gray-500 italic">No apps installed</div>'
    if data.get('apps'):
        apps_section = '<div class="grid grid-cols-2 gap-3">'
        for k in data['apps'].keys():
            apps_section += f'<div class="bg-gray-50 p-3 rounded">{k}</div>'
        apps_section += '</div>'

    # Create the sequences section
    sequences_section = '<div class="text-gray-500 italic">No sequences defined</div>'
    if data.get('sequences'):
        sequences_section = ''
        for seq_name, seq_data in data['sequences'].items():
            sequences_section += f'''
                <div class="mb-4 last:mb-0">
                    <div class="font-medium text-lg mb-2">{seq_name}</div>
                    <div class="bg-gray-50 p-4 rounded">
                        <div class="space-y-2">
            '''
            for action in seq_data:
                icon = 'code' if action['type'] == 'actions' else 'cog'
                sequences_section += f'''
                    <div class="flex items-center space-x-2">
                        <span class="text-blue-500">
                            <i class="fas fa-{icon}"></i>
                        </span>
                        <span class="font-medium">{action['name']}</span>
                    </div>
                '''
            sequences_section += '''
                        </div>
                    </div>
                </div>
            '''

    content = f'''
        <div class="space-y-6">
            <div class="flex items-center space-x-4">
                <div class="text-2xl font-bold text-gray-700">{data.get('name', username)}'s Dashboard</div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-4 text-gray-700">
                        <i class="fas fa-plug mr-2"></i>Connections
                    </h2>
                    {connections_section}
                </div>

                <div class="bg-white p-6 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-4 text-gray-700">
                        <i class="fas fa-cube mr-2"></i>Apps
                    </h2>
                    {apps_section}
                </div>
            </div>

            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4 text-gray-700">
                    <i class="fas fa-code-branch mr-2"></i>Sequences
                </h2>
                {sequences_section}
            </div>
        </div>
    '''
    
    return render_page(username, "Home", content, 
                      instance_status='online' if is_fresh else 'offline')


@app.route('/<username>/files')
@require_atom_user
def user_files(username):
    instance = ExposedInstance.query.filter_by(username=username).first()
    if not instance:
        return jsonify({'error': 'User not found'}), 404
    
    if not check_access(instance, request):
        return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Access Required</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-100">
                <div class="container mx-auto px-4 py-8">
                    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                        <h1 class="text-2xl font-bold mb-4">Access Required</h1>
                        <p class="mb-4">Please enter your email to access this instance:</p>
                        <form method="GET" class="space-y-4">
                            <input type="email" name="email" placeholder="Enter your email" 
                                   class="w-full px-3 py-2 border rounded" required>
                            <button type="submit" 
                                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                                Submit
                            </button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
        """)
        
    path = request.args.get('path', '')
    path = path.strip('/')  # Strip slashes but normalize how paths are constructed

    # Calculate parent path and prepare breadcrumb path parts
    path_parts = []
    if path:
        parts = path.split('/')
        parent_path = '/'.join(parts[:-1])
        
        # Build path parts for breadcrumb navigation
        current = ""
        for i, part in enumerate(parts):
            if not part:  # Skip empty parts
                continue
            current = (current + "/" + part) if current else part
            path_parts.append({"name": part, "path": current})
    else:
        parent_path = ""
    
    # Try to get real file data from local instance or cached data
    data, is_fresh = fetch_local_data(instance, 'files_data', {'path': path})
    
    if data:
        # Update cached data for this path
        if not instance.files_data:
            instance.files_data = {}
        
        instance.files_data = data
        instance.last_data_sync = datetime.utcnow()
        db.session.commit()
        file_data = data.get('structure', {'folders': [], 'files': []})
    elif instance.files_data:
        # Use cached data if available
        file_data = instance.files_data.get('structure', {'folders': [], 'files': []})
    else:
        # Fall back to dummy data if nothing is available
        file_data = get_dummy_files(path)
    
    # Add icons to file data
    for file in file_data.get('files', []):
        if 'icon' not in file:
            file['icon'] = get_file_icon(file['name'])
    
    # Render the file explorer template
    content = render_template_string(
        FILE_EXPLORER_TEMPLATE,
        username=username,
        file_data=file_data,
        current_path=path,
        current_path_prefix=path + '/' if path else '',
        parent_path=parent_path
    )
    
    return render_page(username, "Files", content, 
                      instance_status='online' if is_fresh else 'offline')
    



@app.route('/<username>/file-content/<path:file_path>')
@require_atom_user
def get_file_content(username, file_path):
    # Find the user's instance
    instance = ExposedInstance.query.filter_by(username=username).first()
    if not instance:
        return jsonify({'error': 'User not found'}), 404
        
    try:
        # Fetch file content directly from the local instance
        file_content, is_fresh = fetch_local_data(instance, f"files/{file_path}")
        
        if is_fresh and file_content:
            return jsonify(file_content)
            
        # Check if we have file content in files_data
        if instance.files_data and 'file_contents' in instance.files_data:
            file_contents = instance.files_data['file_contents']
            if file_path in file_contents:
                return jsonify(file_contents[file_path])
                
        return jsonify({'error': 'File content not available'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Add a login callback route
@app.route('/auth/callback')
def auth_callback():
    # Get token from query parameter
    token = request.args.get('token')
    if not token:
        return "No token provided", 400
        
    # Verify token
    try:
        response = requests.post(
            f"{AUTH_SERVER_URL}/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            # Store token in session
            session['token'] = token
            return redirect('/')  # Redirect to home page
        else:
            return "Invalid token", 401
            
    except requests.RequestException:
        return "Auth server error", 500
    
@app.route('/<username>/behaviors')
def user_behaviors(username):
    instance = ExposedInstance.query.filter_by(username=username).first()
    if not instance:
        return jsonify({'error': 'User not found'}), 404

    data, is_fresh = fetch_local_data(instance, 'behaviors_data')
    if data:
        instance.behaviors_data = data
        instance.last_data_sync = datetime.utcnow()
        db.session.commit()
    elif instance.behaviors_data:
        data = instance.behaviors_data
    else:
        data = {"message": "No behaviors data available"}

    content = f"""
        <div class="space-y-4">
            <div class="text-lg">Behaviors</div>
            <pre class="bg-gray-100 p-4 rounded overflow-auto">{str(data)}</pre>
        </div>
    """
    
    return render_page(username, "Behaviors", content,
                      instance_status='online' if is_fresh else 'offline')

@app.route('/register', methods=['POST'])
def register_instance():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        user_id = data.get('user_id')
        username = data.get('username')
        local_url = data.get('local_url')
        initial_data = data.get('initial_data', {})
        
        if not all([user_id, username, local_url]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if instance already exists
        instance = ExposedInstance.query.filter_by(username=username).first()
        if instance:
            instance.local_url = local_url
            instance.last_heartbeat = datetime.utcnow()
        else:
            instance = ExposedInstance(
                user_id=user_id,
                username=username,
                local_url=local_url,
                token=str(uuid.uuid4())
            )
            db.session.add(instance)
        
        # Store initial data if provided
        if initial_data:
            instance.home_data = initial_data.get('home_data')
            instance.files_data = initial_data.get('files_data')
            instance.behaviors_data = initial_data.get('behaviors_data')
            instance.last_data_sync = datetime.utcnow()
        
        db.session.commit()
        return jsonify(instance.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/heartbeat/<token>', methods=['POST'])
def heartbeat(token):
    try:
        instance = ExposedInstance.query.filter_by(token=token).first()
        if not instance:
            return jsonify({'error': 'Instance not found'}), 404
        
        instance.last_heartbeat = datetime.utcnow()
        
        # Update instance data if provided
        if request.is_json:
            data = request.json
            if data:
                if 'home_data' in data:
                    instance.home_data = data['home_data']
                if 'files_data' in data:
                    instance.files_data = data['files_data']
                if 'behaviors_data' in data:
                    instance.behaviors_data = data['behaviors_data']
                instance.last_data_sync = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/deregister/<token>', methods=['DELETE'])
def deregister_instance(token):
    try:
        instance = ExposedInstance.query.filter_by(token=token).first()
        if instance:
            username = instance.username  # Store username for logging
            db.session.delete(instance)
            db.session.commit()
            print(f"Successfully deregistered instance for user: {username}")
            return jsonify({'status': 'Instance deregistered successfully'}), 200
        return jsonify({'error': 'Instance not found'}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Error during deregistration: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
