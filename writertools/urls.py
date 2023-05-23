"""writertools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from genericsite import views as generic

urlpatterns = [
    path("plotboard/", include("plotboard.urls")),
    path("wordtracker/", include("wordtracker.urls")),
    # Genericsite accounts/profile
    path("accounts/profile/", generic.ProfileView.as_view(), name="account_profile"),
    # Use allauth views rather than Django defaults
    path("accounts/", include("allauth.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("", include("genericsite.urls")),
]

if settings.DEBUG:
    # NOTE: When DEBUG and staticfiles is installed, Django automatically adds static
    # urls, but does not automatically serve MEDIA
    from django.conf.urls.static import static

    # Serve static and media files from development server
    # urlpatterns += staticfiles_urlpatterns()  # automatic when DEBUG on
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar

        # Catch-all patterns may block these if appended, hence insert
        urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))
    except ImportError:
        pass
