import requests
from flask import request, redirect, render_template_string, make_response, session, jsonify, url_for, current_app
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"

def require_atom_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is already authenticated in session
        if session.get('user_email'):
            return f(*args, **kwargs)
        
        # Check for token in cookies
        token = request.cookies.get('atom_token')
        
        # Check for token in Authorization header
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                else:
                    token = auth_header
        
        # If no token is found, show login template
        if not token:
            if request.content_type == 'application/json':
                return jsonify({'error': 'Authentication required'}), 401
            return render_template_string(LOGIN_TEMPLATE, auth_server_url=AUTH_SERVER_URL)
        
        # Verify the token with the auth server
        try:
            response = requests.post(
                f"{AUTH_SERVER_URL}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                session['user_email'] = user_data.get('email')
                
                # Create a response that includes the original response and sets cookies
                resp = make_response(f(*args, **kwargs))
                resp.set_cookie('atom_token', token, httponly=True, samesite='Lax', max_age=86400)  # 24 hours
                
                return resp
            else:
                # Clear any invalid tokens
                resp = make_response(render_template_string(LOGIN_TEMPLATE, auth_server_url=AUTH_SERVER_URL) 
                                   if request.content_type != 'application/json' 
                                   else jsonify({'error': 'Invalid authentication'}))
                resp.delete_cookie('atom_token')
                resp.delete_cookie('atom_email')
                session.pop('user_email', None)
                
                if request.content_type == 'application/json':
                    return jsonify({'error': 'Invalid authentication'}), 401
                return resp
                
        except Exception as e:
            # Log the error for debugging
            print(f"Authentication error: {str(e)}")
            
            # Clear any invalid data
            resp = make_response(render_template_string(LOGIN_TEMPLATE, auth_server_url=AUTH_SERVER_URL)
                               if request.content_type != 'application/json'
                               else jsonify({'error': f'Authentication error: {str(e)}'}))
            resp.delete_cookie('atom_token')
            resp.delete_cookie('atom_email')
            session.pop('user_email', None)
            
            if request.content_type == 'application/json':
                return jsonify({'error': f'Authentication error: {str(e)}'}), 401
            return resp
            
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
            <div id="message" class="mb-4 p-3 rounded-md hidden"></div>
            <form id="emailForm" class="space-y-4">
                <input type="email" id="email" placeholder="Enter your Atom email" 
                    class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button type="submit" id="submitBtn"
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
        const submitBtn = document.getElementById('submitBtn');
        const messageDiv = document.getElementById('message');
        
        // Input validation
        if (!email || !email.includes('@')) {
            messageDiv.textContent = 'Please enter a valid email address';
            messageDiv.className = 'mb-4 p-3 rounded-md bg-red-100 text-red-800';
            messageDiv.classList.remove('hidden');
            return;
        }
        
        // Disable button and show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Verifying...';
        
        try {
            const response = await fetch(`{{ auth_server_url }}/check-email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Set cookies
                document.cookie = `atom_email=${email}; path=/; max-age=86400; samesite=lax`;
                document.cookie = `atom_token=${data.token}; path=/; max-age=86400; samesite=lax`;
                
                // Show success message
                messageDiv.textContent = 'Email verified! Redirecting...';
                messageDiv.className = 'mb-4 p-3 rounded-md bg-green-100 text-green-800';
                messageDiv.classList.remove('hidden');
                
                // Reload after a short delay to apply the new cookies
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                // Show error message
                messageDiv.textContent = data.error || 'Email not found in Atom system. Please register first.';
                messageDiv.className = 'mb-4 p-3 rounded-md bg-red-100 text-red-800';
                messageDiv.classList.remove('hidden');
                
                // Reset button
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-check mr-2"></i> Verify Email';
            }
        } catch (error) {
            console.error('Error:', error);
            
            // Show error message
            messageDiv.textContent = 'Error connecting to authentication server. Please try again.';
            messageDiv.className = 'mb-4 p-3 rounded-md bg-red-100 text-red-800';
            messageDiv.classList.remove('hidden');
            
            // Reset button
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-check mr-2"></i> Verify Email';
        }
    });
    </script>
</body>
</html>
"""