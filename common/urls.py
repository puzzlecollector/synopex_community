from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    # account settings
    path("settings/base/", views.base, name="settings_base"),
    # path("settings/password_change/", settings_views.PasswordChangeView.as_view(), name="password_change),
    path("settings/image/", views.profile_modify_image, name="settings_image"),
    # path("settings/image/delete/", settings_views.profile_image_delete, name="settings_image_delete"),
    path('settings/password_reset/', views.password_reset, name='password_reset'),

    # account page
    path("account_page/", views.account_page, name="account_page"),

    # view user questions, answers and comments
    path('user/<int:user_id>/questions/', views.user_questions, name='user_questions'),
    path('user/<int:user_id>/answers/', views.user_answers, name='user_answers'),
    path('user/<int:user_id>/comments/', views.user_comments, name='user_comments'),

]