from flask import request, redirect, render_template_string, make_response, session
import requests
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for token in session first
        token = session.get('token')
        
        if not token:
            # If no token in session, check headers
            token = request.headers.get("Authorization")
            
        if not token:
            # No token found - show login template
            return render_template_string(LOGIN_TEMPLATE)
        
        # Validate token with auth server
        try:
            response = requests.post(
                f"{AUTH_SERVER_URL}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                # Clear invalid token from session
                session.pop('token', None)
                return render_template_string(LOGIN_TEMPLATE)
            
            user_data = response.json()
            request.user = user_data
            return f(*args, **kwargs)
            
        except requests.RequestException:
            return render_template_string(LOGIN_TEMPLATE)
            
    return decorated_function


    
LOGIN_TEMPLATE = """
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Login Required&lt;/title&gt;
    &lt;script src="https://cdn.tailwindcss.com"&gt;&lt;/script&gt;
    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
    &lt;link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet"&gt;
&lt;/head&gt;
&lt;body class="bg-gray-100"&gt;
    &lt;div class="min-h-screen flex items-center justify-center"&gt;
        &lt;div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md"&gt;
            &lt;div class="text-center mb-8"&gt;
                &lt;h1 class="text-2xl font-bold text-gray-800"&gt;Welcome to Atom&lt;/h1&gt;
                &lt;p class="text-gray-600 mt-2"&gt;Sign in to access this instance&lt;/p&gt;
            &lt;/div&gt;
            
            &lt;div class="space-y-4"&gt;
                &lt;a href="https://agentsofatom.com/login?callback=https://exps-prod.onrender.com/auth/callback" 
                   class="w-full flex items-center justify-center bg-blue-600 text-white px-4 py-3 rounded-md hover:bg-blue-700 transition duration-300"&gt;
                    &lt;i class="fas fa-sign-in-alt mr-2"&gt;&lt;/i&gt; Sign in with Atom
                &lt;/a&gt;
            &lt;/div&gt;
            
            &lt;div class="mt-6 text-center text-sm text-gray-600"&gt;
                &lt;p&gt;Don't have an account? &lt;a href="https://agentsofatom.com/signup" class="text-blue-600 hover:underline"&gt;Sign up&lt;/a&gt;&lt;/p&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
"""