import requests
from flask import request, redirect, render_template_string
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"  # Auth server URL

def require_auth(f):
    """Decorator to check JWT token via the Auth Server.
    If not authenticated, shows a login template instead of redirecting."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for auth token in headers or cookies
        token = request.headers.get("Authorization")
        
        # Check for email in query parameters (for access via email)
        email = request.args.get("email")
        if email:
            # Here you would validate email access if applicable
            # For now, we'll just store it in the request object
            request.user = {"email": email}
            return f(*args, **kwargs)
            
        if not token:
            # Show login template instead of redirecting
            return render_template_string(LOGIN_TEMPLATE)
        
        # Validate token with the auth server
        try:
            response = requests.post(
                f"{AUTH_SERVER_URL}/verify", 
                headers={"Authorization": token}
            )
            
            if response.status_code != 200:
                # Token invalid or expired - show login template
                return render_template_string(LOGIN_TEMPLATE)
            
            user_data = response.json()  # {"email": "user@example.com"}
            request.user = user_data  # Store user data in request object
            return f(*args, **kwargs)
            
        except requests.RequestException:
            # Auth server unreachable - show login template
            return render_template_string(LOGIN_TEMPLATE)
    
    return decorated_function


# Login template that will be shown when authentication is required
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
                <p class="text-gray-600 mt-2">Sign in to access this instance</p>
            </div>
            
            <div class="space-y-4">
                <a href="https://agentsofatom.com/login" 
                   class="w-full flex items-center justify-center bg-blue-600 text-white px-4 py-3 rounded-md hover:bg-blue-700 transition duration-300">
                    <i class="fas fa-sign-in-alt mr-2"></i> Sign in with Atom
                </a>
                
                <div class="relative py-2">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-300"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-2 bg-white text-gray-500">Or continue with email</span>
                    </div>
                </div>
                
                <form method="GET" class="space-y-4">
                    <div>
                        <input type="email" name="email" placeholder="Enter your email" 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <button type="submit" 
                            class="w-full bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition duration-300">
                        Continue
                    </button>
                </form>
            </div>
            
            <div class="mt-6 text-center text-sm text-gray-600">
                <p>Don't have an account? <a href="https://agentsofatom.com/signup" class="text-blue-600 hover:underline">Sign up</a></p>
            </div>
        </div>
    </div>
</body>
</html>
"""
