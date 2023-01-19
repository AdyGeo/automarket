from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from autoadmin.models import Autovehicul 


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['homepage','contact', 'despre-noi']
    def priority(self, item):
        return {'homepage':0.8, 'contact': 0.5, 'despre-noi': 0.5}[item]
    def changefreq(self, item):
        return {'homepage':'monthly', 'contact': 'monthly', 'despre-noi': 'monthly'}[item]
    def location(self, item):
        return {'homepage':'/', 'contact': '/contact/', 'despre-noi': '/despre-noi/'}[item]

class AutoViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    def items(self):
        autovehicule = Autovehicul.objects.filter(vizibil=True, vandut=False)
        return autovehicule
    def lastmod(seld, obj):
        return obj.data_modificare

class AutoVanduteViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    def items(self):
        autovehicule = Autovehicul.objects.filter(vizibil=True, vandut=True)
        return autovehicule
    def lastmod(seld, obj):
        return obj.data_modificare

