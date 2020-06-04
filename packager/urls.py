"""
packager URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from rest_framework_simplejwt import views as simple_jwt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('packager.core.urls')),

    # Authentication
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token', simple_jwt.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/auth/token/refresh', simple_jwt.TokenRefreshView.as_view(), name='token-refresh')
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
       path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
      + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
