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
                <p class="text-gray-600 mt-2">Sign in or sign up to access this instance</p>
            </div>
            
            <!-- Tab Navigation -->
            <div class="flex border-b border-gray-300 mb-6">
                <button id="loginTab" class="flex-1 py-2 font-medium text-blue-600 border-b-2 border-blue-600">
                    Sign In
                </button>
                <button id="signupTab" class="flex-1 py-2 font-medium text-gray-500 hover:text-gray-700">
                    Sign Up
                </button>
            </div>

            <!-- Login Section -->
            <div id="loginSection" class="space-y-4">
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
                
                <form id="loginForm" method="GET" class="space-y-4">
                    <div>
                        <input type="email" name="email" placeholder="Enter your email" 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <div class="hidden" id="passwordField">
                        <input type="password" id="loginPassword" placeholder="Enter your password" 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <button type="submit" 
                            class="w-full bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition duration-300">
                        Continue
                    </button>
                </form>
                <div id="loginStatus" class="text-center text-sm min-h-6"></div>
            </div>

            <!-- Signup Section (Hidden by Default) -->
            <div id="signupSection" class="space-y-4 hidden">
                <a href="https://agentsofatom.com/signup" 
                   class="w-full flex items-center justify-center bg-blue-600 text-white px-4 py-3 rounded-md hover:bg-blue-700 transition duration-300">
                    <i class="fas fa-user-plus mr-2"></i> Sign up with Atom
                </a>
                
                <div class="relative py-2">
                    <div class="absolute inset-0 flex items-center">
                        <div class="w-full border-t border-gray-300"></div>
                    </div>
                    <div class="relative flex justify-center text-sm">
                        <span class="px-2 bg-white text-gray-500">Or create an account with email</span>
                    </div>
                </div>
                
                <form id="signupForm" class="space-y-4">
                    <div>
                        <input type="email" id="signupEmail" placeholder="Enter your email" 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <div>
                        <input type="password" id="signupPassword" placeholder="Create a password" 
                               class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                    </div>
                    <button type="submit" 
                            class="w-full bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition duration-300">
                        Sign Up
                    </button>
                </form>
                <div id="signupStatus" class="text-center text-sm min-h-6"></div>
            </div>
        </div>
    </div>

    <script>
        const AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com";
        const currentUrl = window.location.href;

        // Tab switching functionality
        const loginTab = document.getElementById('loginTab');
        const signupTab = document.getElementById('signupTab');
        const loginSection = document.getElementById('loginSection');
        const signupSection = document.getElementById('signupSection');

        loginTab.addEventListener('click', () => {
            loginTab.classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
            loginTab.classList.remove('text-gray-500');
            signupTab.classList.add('text-gray-500');
            signupTab.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
            
            loginSection.classList.remove('hidden');
            signupSection.classList.add('hidden');
        });

        signupTab.addEventListener('click', () => {
            signupTab.classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
            signupTab.classList.remove('text-gray-500');
            loginTab.classList.add('text-gray-500');
            loginTab.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
            
            signupSection.classList.remove('hidden');
            loginSection.classList.add('hidden');
        });

        // Helper function for API requests
        async function makeRequest(url, method, body, statusElement) {
            statusElement.innerHTML = '<span class="text-orange-500">⏳ Processing...</span>';
            
            try {
                const res = await fetch(`${AUTH_SERVER_URL}${url}`, {
                    method,
                    headers: { 
                        "Content-Type": "application/json",
                        "Authorization": localStorage.getItem("token") ? `Bearer ${localStorage.getItem("token")}` : ""
                    },
                    body: body ? JSON.stringify(body) : null
                });

                const data = await res.json();
                if (!res.ok) throw new Error(data.error || "Request failed");

                statusElement.innerHTML = '<span class="text-green-500">✅ Success!</span>';
                return data;
            } catch (err) {
                statusElement.innerHTML = `<span class="text-red-500">❌ ${err.message}</span>`;
                return null;
            }
        }

        // Login form handling - maintain original behavior
        document.getElementById("loginForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = e.target.querySelector('input[name="email"]').value;
            const passwordField = document.getElementById("passwordField");
            
            if (passwordField.classList.contains("hidden")) {
                // First submission - just email, show password field
                passwordField.classList.remove("hidden");
                e.target.querySelector("button").textContent = "Sign In";
                return;
            }
            
            // Second submission - email + password
            const password = document.getElementById("loginPassword").value;
            const statusElement = document.getElementById("loginStatus");
            
            const data = await makeRequest("/login", "POST", { email, password }, statusElement);
            
            if (data?.access_token) {
                localStorage.setItem("token", data.access_token);
                
                // Add token to current URL and redirect
                let redirectUrl = new URL(currentUrl);
                if (redirectUrl.searchParams.has("email")) {
                    // Remove email param if it exists
                    redirectUrl.searchParams.delete("email");
                }
                
                // Redirect to the same page (will now pass the auth check with token in localStorage)
                statusElement.innerHTML = '<span class="text-green-500">✅ Login successful! Redirecting...</span>';
                setTimeout(() => window.location.href = redirectUrl.toString(), 1000);
            }
        });

        // Signup form handling
        document.getElementById("signupForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("signupEmail").value;
            const password = document.getElementById("signupPassword").value;
            const statusElement = document.getElementById("signupStatus");
            
            const data = await makeRequest("/register", "POST", { email, password }, statusElement);
            
            if (data) {
                // Switch to login tab after successful registration
                setTimeout(() => {
                    loginTab.click();
                    document.querySelector('input[name="email"]').value = email;
                    document.getElementById("passwordField").classList.remove("hidden");
                    document.getElementById("loginStatus").innerHTML = '<span class="text-green-500">Account created! Please sign in.</span>';
                }, 1000);
            }
        });
    </script>
</body>
</html>
"""
