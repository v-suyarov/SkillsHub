from django.contrib import admin
from django.urls import path
from MainSite import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:id>', views.user_profile, name='profile'),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('admin/', admin.site.urls, name="admin"),
    path('upload/', views.upload_students, name='upload_students'),
    path('profile/edit/<int:id>', views.profile_edit, name='profile_edit'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('test/', views.test, name="test")
]
