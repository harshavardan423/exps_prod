import requests
from flask import request, redirect, render_template_string, make_response, session, jsonify, url_for, current_app
from functools import wraps

AUTH_SERVER_URL = "https://auth.agentsofatom.com:10000"

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
            return render_template_string(
                LOGIN_TEMPLATE, 
                auth_server_url=AUTH_SERVER_URL,
                return_url=request.url
            )
        
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
                resp = make_response(render_template_string(
                    LOGIN_TEMPLATE, 
                    auth_server_url=AUTH_SERVER_URL,
                    return_url=request.url
                ))
                resp.delete_cookie('atom_token')
                session.pop('user_email', None)
                
                if request.content_type == 'application/json':
                    return jsonify({'error': 'Invalid authentication'}), 401
                return resp
                
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            resp = make_response(render_template_string(
                LOGIN_TEMPLATE, 
                auth_server_url=AUTH_SERVER_URL,
                return_url=request.url
            ))
            resp.delete_cookie('atom_token')
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
        const returnUrl = "{{ return_url }}";
        
        document.getElementById('emailForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const submitBtn = document.getElementById('submitBtn');
            const messageDiv = document.getElementById('message');
            
            // Input validation
            if (!email || !email.includes('@')) {
                showMessage('Please enter a valid email address', 'error');
                return;
            }
            
            // Disable button and show loading state
            setLoadingState(true);
            
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
                    
                    showMessage('Email verified! Redirecting...', 'success');
                    
                    // Redirect to the original URL or reload
                    setTimeout(() => {
                        window.location.href = returnUrl || window.location.href;
                    }, 1000);
                } else {
                    showMessage(data.error || 'Email not found in Atom system. Please register first.', 'error');
                    setLoadingState(false);
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('Error connecting to authentication server. Please try again.', 'error');
                setLoadingState(false);
            }
        });

        function showMessage(message, type) {
            const messageDiv = document.getElementById('message');
            messageDiv.textContent = message;
            messageDiv.className = `mb-4 p-3 rounded-md ${
                type === 'error' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
            }`;
            messageDiv.classList.remove('hidden');
        }

        function setLoadingState(loading) {
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.disabled = loading;
            submitBtn.innerHTML = loading ? 
                '<i class="fas fa-spinner fa-spin mr-2"></i> Verifying...' :
                '<i class="fas fa-check mr-2"></i> Verify Email';
        }
    </script>
</body>
</html>

"""
