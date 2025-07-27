import datetime
import os
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from collections import defaultdict
import time


# Ensure logs directory exists
LOG_DIR = os.path.join(settings.BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'requests.log')


class RequestLoggingMiddleware:
    """
    Logs every incoming request: timestamp, user, and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user info
        if request.user.is_authenticated:
            user = request.user.email
        else:
            user = "Anonymous"

        # Log request
        log_entry = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)

        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    """
    Restricts access to chat outside 6 AM - 9 PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.datetime.now().hour

        # Allow access only between 6 AM and 9 PM
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden("Chat is only available from 6 AM to 9 PM.")

        return self.get_response(request)



# In-memory storage for rate limiting (use Redis in production)
ip_request_log = defaultdict(list)

class RateLimitMiddleware:
    """
    Limits number of POST requests (messages) per IP: 5 per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/v1/messages/' and request.method == 'POST':
            client_ip = self.get_client_ip(request)
            now = time.time()

            # Clean old requests (older than 60 seconds)
            ip_request_log[client_ip] = [
                timestamp for timestamp in ip_request_log[client_ip]
                if now - timestamp < 60
            ]

            if len(ip_request_log[client_ip]) >= 5:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Only 5 messages per minute allowed.'},
                    status=429  # Too Many Requests
                )

            # Log this request
            ip_request_log[client_ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



class RolePermissionMiddleware:
    """
    Restricts access to certain paths unless user is 'admin' or 'host'.
    Applies only to paths starting with /api/v1/admin-chat/
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Apply restriction only to protected paths
        if request.path.startswith('/api/v1/admin-chat/'):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Login required.")

            user_role = getattr(request.user, 'role', '')
            if user_role not in ['admin', 'host']:
                return HttpResponseForbidden("Access denied. Admin or host only.")

        return self.get_response(request)