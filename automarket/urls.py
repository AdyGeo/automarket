"""automarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from autoadmin.api.urls import urlpatterns as apiurls
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, AutoViewSitemap, AutoVanduteViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'auto': AutoViewSitemap,
    'auto-vandute': AutoVanduteViewSitemap
}

base_patterns = [
   
    path('api/', include(apiurls)),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
   
] 

urlpatterns = [
    # re_path('^(?!app).*$',TemplateView.as_view(template_name='index.html'), name="app"),
    path('app/', include(base_patterns))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)