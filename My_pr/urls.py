from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('articles/', include('articles.urls')),
    path('__debug__/', include('debug_toolbar.urls'))
]

# if settings.DEBUG:
#     urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
