import datetime
import time
import logging
from django.http import HttpResponseForbidden, JsonResponse


# === 1. Request Logging Middleware ===
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)
        return self.get_response(request)


# === 2. Restrict Access by Time ===
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            hour = datetime.datetime.now().hour
            if hour < 6 or hour > 21:
                return HttpResponseForbidden("Chat access is only allowed between 6 AM and 9 PM.")
        return self.get_response(request)


# === 3. Rate Limit by IP ===
ip_message_count = {}
RATE_LIMIT = 5
TIME_WINDOW = 60


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/messages/' and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()
            ip_message_count[ip] = [t for t in ip_message_count.get(ip, []) if now - t < TIME_WINDOW]
            if len(ip_message_count[ip]) >= RATE_LIMIT:
                return JsonResponse(
                    {'error': 'Message limit exceeded. Only 5 messages allowed per minute.'},
                    status=429
                )
            ip_message_count[ip].append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


# === 4. Role-Based Permission Middleware ===
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected = ['/api/admin/', '/moderate/']
        if any(request.path.startswith(p) for p in protected):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            if not request.user.is_staff:
                return HttpResponseForbidden("Admin or moderator access required.")
        return self.get_response(request)