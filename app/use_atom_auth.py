import requests
from flask import request, redirect, render_template_string, make_response
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"

def require_atom_user(f):
    """Decorator to check if user exists in Atom Auth system"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for email in cookie first
        email = request.cookies.get('atom_email')
        token = request.cookies.get('atom_token')
        
        if not email or not token:
            # Show login template if no email/token
            return render_template_string(LOGIN_TEMPLATE)
        
        # Verify email exists in Atom system
        try:
            # Verify token
            verify_response = requests.post(
                f"{AUTH_SERVER_URL}/verify",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if verify_response.status_code != 200:
                # Token invalid - check email exists
                email_check_response = requests.post(
                    f"{AUTH_SERVER_URL}/check-email",
                    json={"email": email}
                )
                
                if email_check_response.status_code != 200:
                    # Email doesn't exist in Atom system
                    return render_template_string(LOGIN_TEMPLATE)
                    
                # Email exists, set new token
                new_token = email_check_response.json()['token']
                response = make_response(f(*args, **kwargs))
                response.set_cookie('atom_token', new_token)
                return response
            
            # Token valid, proceed
            return f(*args, **kwargs)
            
        except requests.RequestException:
            # Auth server unreachable
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
                &lt;p class="text-gray-600 mt-2"&gt;Verify your Atom account&lt;/p&gt;
            &lt;/div&gt;
            
            &lt;form id="emailForm" class="space-y-4"&gt;
                &lt;input type="email" id="email" placeholder="Enter your Atom email" 
                       class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"&gt;
                &lt;button type="submit" 
                        class="w-full flex items-center justify-center bg-blue-600 text-white px-4 py-3 rounded-md hover:bg-blue-700 transition duration-300"&gt;
                    &lt;i class="fas fa-check mr-2"&gt;&lt;/i&gt; Verify Email
                &lt;/button&gt;
            &lt;/form&gt;
            
            &lt;div class="mt-6 text-center text-sm text-gray-600"&gt;
                &lt;p&gt;Don't have an account? &lt;a href="https://agentsofatom.com/signup" class="text-blue-600 hover:underline"&gt;Sign up&lt;/a&gt;&lt;/p&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;

    &lt;script&gt;
    document.getElementById('emailForm').addEventListener('submit', async (e) =&gt; {
        e.preventDefault();
        const email = document.getElementById('email').value;
        
        try {
            const response = await fetch('""" + AUTH_SERVER_URL + """/check-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });
            
            if (response.ok) {
                const data = await response.json();
                // Set cookies
                document.cookie = `atom_email=${email}; path=/`;
                document.cookie = `atom_token=${data.token}; path=/`;
                // Reload page to access protected content
                window.location.reload();
            } else {
                alert('Email not found in Atom system. Please register first.');
            }
        } catch (error) {
            alert('Error verifying email. Please try again.');
        }
    });
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;
"""