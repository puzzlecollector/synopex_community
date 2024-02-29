from django.contrib import admin
from django.urls import path, include
from synopex.views import base_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('synopex/', include('synopex.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'common.views.page_not_found'