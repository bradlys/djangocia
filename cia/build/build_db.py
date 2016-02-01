from cia.models import *
from cia.serializers import *
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import django_filters
from django.conf import settings
import random
import datetime
from .special import names


class BuildOrganization(APIView):

    def get(self, request, frmt=None):
        name = names[random.randint(0, len(names)-1)]
        orgName = name + "'s organziation"
        orgEmail = name + '@gmail.com'
        org = Organization.objects.create(name=orgName)
        return HttpResponse('')


class BuildEvent(APIView):

    def get(self, request, pk, frmt=None):
        amount = request.query_params.get('amount', None)
        if amount is None or amount < 0:
            amount = 25
        for i in range(amount):
            name = names[random.randint(0, len(names)-1)]
            eventName = name + "'s event"
            eventDate = str(datetime.datetime.fromtimestamp(random.randint(454293720, 2054293720)))
            event = Event.objects.create(name=eventName, date=eventDate, organization=Organization.objects.get(pk=pk))
        return HttpResponse('')


class BuildCustomer(APIView):

    def get(self, request, amount, frmt=None):
        amount = request.query_params.get('amount', None)
        if amount is None or amount < 0:
            amount = 1000
        for i in range(amount):
            name = names[random.randint(0, len(names))]
            Customer.objects.create(name=name)
        return HttpResponse('')


class BuildVisit(APIView):

    def get(self, request, frmt=None):
        amount = request.query_params.get('amount', None)
        if amount is None or amount < 0:
            amount = 2500
        org_id = request.query_params.get('organization', None)
        if org_id is None:
            return HttpResponse('')
        organization = Organization.objects.get(pk=org_id)
        events = Event.objects.all()
        customers = Customer.objects.all()
        i = 0
        j = 0
        while i < amount and j < amount * 5:
            customer = random.choice(customers)
            event = random.choice(events)
            if Visit.objects.filter(customer=customer, event=event).count() == 0:
                transaction = Transaction.objects.create(customer=customer, organization=organization, amount=5, method='CA')
                visit = Visit.object.create(customer=customer, event=event, transaction=transaction)
                i += 1
            j += 1
        return HttpResponse('')



