import requests
from flask import request, jsonify
from functools import wraps

AUTH_SERVER_URL = "https://atom-auth-prod.onrender.com"  # Change this to your actual auth server URL

def require_auth(f):
    """Decorator to check JWT token via the Auth Server."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Missing token"}), 401
        
        # Validate token with the auth server
        try:
            response = requests.post(f"{AUTH_SERVER_URL}/verify", headers={"Authorization": token})
            if response.status_code != 200:
                return jsonify({"error": "Invalid or expired token"}), 401

            user_data = response.json()  # Example: {"email": "user@example.com"}
            request.user = user_data  # Store user data in the request object
            return f(*args, **kwargs)
        except requests.RequestException:
            return jsonify({"error": "Auth server unavailable"}), 500

    return decorated_function
