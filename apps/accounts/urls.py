from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    register_view,
    login_view,
    logout_view,
    google_auth_view,
    verify_email_view,
    password_reset_request_view,
    password_reset_confirm_view,
    me_view,
    GuestProfileViewSet,
    DriverProfileViewSet,
    CarViewSet,
    my_profile_view
)

router = DefaultRouter()
router.register(r'profile/guest', GuestProfileViewSet, basename='guest-profile')
router.register(r'profile/driver', DriverProfileViewSet, basename='driver-profile')
router.register(r'car', CarViewSet, basename='car')

urlpatterns = [
    # Аутентификация
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('google/', google_auth_view, name='google-auth'),
    path('verify-email/', verify_email_view, name='verify-email'),
    path('password-reset/', password_reset_request_view, name='password-reset'),
    path('password-reset-confirm/', password_reset_confirm_view, name='password-reset-confirm'),
    path('me/', me_view, name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Профили
    path('my-profile/', my_profile_view, name='my-profile'),

    # Router URLs
    path('', include(router.urls)),
]