from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, reverse

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.views.generic import TemplateView



def logout_(request):
    logout(request)
    return render(request, 'registration/logout-confirmation.html')

class LogOutRenderView(TemplateView):
    template_name = "registration/logout-confirmation.html"


urlpatterns = [
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    # path('accounts/logout-confirmation/', logout_, name='logout'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout-confirmation/', LogOutRenderView.as_view(), name='logout-confirmation'),

    # path("accounts/password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    # path("accounts/password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    # path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    # path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # path("accounts/register/", auth_views.RegisterView.as_view(), name="register"),
    # path("accounts/register/done/", auth_views.RegisterDoneView.as_view(), name="register_done"),
    # path("accounts/profile/", auth_views.ProfileUpdateView.as_view(), name="user_update"),
    # path("accounts/profile/done/", auth_views.ProfileUpdateDoneView.as_view(), name="user_update_done"),

    path("admin/", admin.site.urls),
    
    path('course/', include('course.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
