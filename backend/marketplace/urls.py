from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # Frontend pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('freelancer-dashboard/', TemplateView.as_view(template_name='freelancer_dashboard.html'), name='freelancer-dashboard'),
    path('provider-dashboard/', TemplateView.as_view(template_name='provider_dashboard.html'), name='provider-dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.BASE_DIR.parent / 'frontend')
