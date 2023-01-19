from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()

router.register('auto-de-vanzare', views.AutovehiculeActiveViewSet, 'auto-de-vanzare')
router.register('auto-vandute', views.AutovehiculeVanduteViewSet, 'auto-vandute')
router.register('auto-all', views.AutovehiculeAllViewSet, 'auto-all')
router.register('companie', views.CompanieViewSet, 'companie')

urlpatterns = [
    path('contact-email/', views.contactByEmail)
]
urlpatterns += router.urls
