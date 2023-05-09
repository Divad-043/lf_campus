from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')), 
    path("accounts/", include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('dashboard.urls')),
    path('messages/', include('user_messages.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
