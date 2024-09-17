from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('logout/', views.sign_out, name='logout'),
    
    path("profile/", views.profile_view, name="profile"),
    path("faq/", views.faq_view, name="faq"),
]
