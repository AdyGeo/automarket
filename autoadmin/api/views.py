from rest_framework import viewsets
from autoadmin.models import Autovehicul, Companie
from .serializers import AutovehiculSerializer, CompanieSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.throttling import UserRateThrottle
from rest_framework import permissions
from django.core.mail import EmailMessage
import threading
import json

class PerDayUserThrottle(UserRateThrottle):
    rate = '3/day'

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False)


class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'results': data,
        })

class CompanieViewSet(viewsets.ModelViewSet):
    queryset = Companie.objects.all()
    serializer_class = CompanieSerializer
    http_method_names = ['get']


class AutovehiculeAllViewSet(viewsets.ModelViewSet):
    queryset = Autovehicul.objects.filter(vizibil=True)
    serializer_class = AutovehiculSerializer
    lookup_field = 'slug'
    pagination_class = CustomPagination
    http_method_names = ['get']


class AutovehiculeActiveViewSet(viewsets.ModelViewSet):
    queryset = Autovehicul.objects.filter(vizibil=True, vandut=False)
    serializer_class = AutovehiculSerializer
    lookup_field = 'slug'
    pagination_class = CustomPagination
    http_method_names = ['get']


class AutovehiculeVanduteViewSet(viewsets.ModelViewSet):
    queryset = Autovehicul.objects.filter(vizibil=True, vandut=True)
    serializer_class = AutovehiculSerializer
    lookup_field = 'slug'
    pagination_class = CustomPagination
    http_method_names = ['get']


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
@throttle_classes([PerDayUserThrottle])
def contactByEmail(request):
    body = request.data
    
    contactname = body.get('contactname') or ''
    email_from = body.get('email')
    emailBody = body.get('emailBody')

    email = EmailMessage(
        f'[auto-pitesti.ro] email nou, {contactname.title()}',
        f'''
Salut, {contactname.title()}

Acesta este un raspuns automat.

Iti multumim pentru e-mail. Iti vom raspunde in cel mai scurt timp.


Mesajul tau:
--------------------------------
{emailBody}
        ''',
        'autograndclass@gmail.com',
        [email_from],
        ['autograndclass@gmail.com'],
        reply_to=[email_from],
    )
    EmailThread(email).start()
    
    return Response({"success":True})


