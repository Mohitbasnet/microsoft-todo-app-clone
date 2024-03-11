from django.urls import path
from .views import SignUpView, CustomLoginView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]