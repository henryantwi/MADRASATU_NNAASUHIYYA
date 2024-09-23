from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("register/", views.register_view, name="register"),
    path(
        "activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"
    ),
    # User Profile
    path("profile/", views.profile_view, name="profile"),
    path("faq/", views.faq_view, name="faq"),
    
    # Password reset
    # path(
    #     "password_reset/",
    #     views.CustomPasswordResetView.as_view(),
    #     name="password_reset",
    # ),
    # path(
    #     "password_reset/done/",
    #     views.CustomPasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "reset/<uidb64>/<token>/",
    #     views.CustomPasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "reset/done/",
    #     views.CustomPasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    
    
]