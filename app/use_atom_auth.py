import requests
from flask import request, redirect, render_template_string, make_response
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"

def require_atom_user(f):
    """Decorator to check if user exists in Atom Auth system"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        email = request.cookies.get('atom_email')
        token = request.cookies.get('atom_token')
        
        if not email or not token:
            return render_template_string(LOGIN_TEMPLATE)
        
        try:
            verify_response = requests.post(
                f"{AUTH_SERVER_URL}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if verify_response.status_code != 200:
                email_check_response = requests.post(
                    f"{AUTH_SERVER_URL}/check-email",
                    json={"email": email}
                )
                
                if email_check_response.status_code != 200:
                    return render_template_string(LOGIN_TEMPLATE)
                
                new_token = email_check_response.json().get('token')
                if not new_token:
                    return render_template_string(LOGIN_TEMPLATE)
                
                response = make_response(f(*args, **kwargs))
                response.set_cookie('atom_token', new_token)
                return response
            
            return f(*args, **kwargs)
            
        except requests.RequestException:
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
            const response = await fetch(""" + AUTH_SERVER_URL + """/check-email", {
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
