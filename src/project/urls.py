from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include, reverse

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.views.generic import TemplateView

from course.views import test

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
    # Django Admin
    path("admin/", admin.site.urls),
    
    path('test/', test, name='test'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
