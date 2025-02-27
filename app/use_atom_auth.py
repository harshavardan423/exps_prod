import requests
from flask import request, redirect, render_template_string, make_response, session, jsonify, url_for, current_app
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"

def require_atom_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated via session
        if session.get('user_email'):
            return f(*args, **kwargs)
        
        # Check for token in cookies first, then headers
        token = request.cookies.get('atom_token')
        
        if not token:
            # Check headers if no cookie
            auth_header = request.headers.get('Authorization')
            if auth_header:
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                else:
                    token = auth_header
        
        # If no token, redirect to login
        if not token:
            if request.content_type == 'application/json':
                return jsonify({'error': 'Authentication required'}), 401
            return render_template_string(LOGIN_TEMPLATE)
        
        # Verify token with Atom auth server
        try:
            response = requests.post(
                f"{AUTH_SERVER_URL}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                session['user_email'] = user_data.get('email')
                return f(*args, **kwargs)
            else:
                if request.content_type == 'application/json':
                    return jsonify({'error': 'Invalid authentication'}), 401
                return render_template_string(LOGIN_TEMPLATE)
                
        except Exception as e:
            if request.content_type == 'application/json':
                return jsonify({'error': f'Authentication error: {str(e)}'}), 401
            return render_template_string(LOGIN_TEMPLATE)
            
    return decorated_function

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Required</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <div class="text-center mb-8">
                <h1 class="text-2xl font-bold text-gray-800">Welcome to Atom</h1>
                <p class="text-gray-600 mt-2">Verify your Atom account</p>
            </div>
            <form id="emailForm" class="space-y-4">
                <input type="email" id="email" placeholder="Enter your Atom email" 
                       class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button type="submit" 
                        class="w-full flex items-center justify-center bg-blue-600 text-white px-4 py-3 rounded-md hover:bg-blue-700 transition duration-300">
                    <i class="fas fa-check mr-2"></i> Verify Email
                </button>
            </form>
            <div class="mt-6 text-center text-sm text-gray-600">
                <p>Don't have an account? <a href="https://agentsofatom.com/signup" class="text-blue-600 hover:underline">Sign up</a></p>
            </div>
        </div>
    </div>
    <script>
    document.getElementById('emailForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        
        try {
            const response = await fetch(`${AUTH_SERVER_URL}/check-email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });
            
            if (response.ok) {
                const data = await response.json();
                document.cookie = `atom_email=${email}; path=/`;
                document.cookie = `atom_token=${data.token}; path=/`;
                window.location.reload();
            } else {
                alert('Email not found in Atom system. Please register first.');
            }
        } catch (error) {
            alert('Error verifying email. Please try again.');
        }
    });
    </script>
</body>
</html>
"""
