# messaging_app/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # Endpoint for obtaining access and refresh tokens (login)
    TokenRefreshView,    # Endpoint for refreshing access tokens using a refresh token
    TokenBlacklistView   # Endpoint for blacklisting refresh tokens (logout)
)

urlpatterns = [
    path('admin/', admin.site.urls), # Django Admin site
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), # Used for JWT logout
    path('api/', include('chats.urls')), # Include URLs from your 'chats' app, prefixed with /api/
]
