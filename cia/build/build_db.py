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


def createEvents(amount, org_id):
    for i in range(amount):
        name = names[random.randint(0, len(names)-1)]
        eventName = name + "'s event"
        eventDate = datetime.datetime.fromtimestamp(random.randint(454293720, 2054293720)).strftime('%G-%m-%d')
        event = Event.objects.create(name=eventName, date=eventDate, organization=Organization.objects.get(pk=org_id))

def createCustomers(amount):
    for i in range(amount):
        name = names[random.randint(0, len(names))]
        Customer.objects.create(name=name)

def createVisits(amount, org_id):
    organization = Organization.objects.get(pk=org_id)
    events = Event.objects.filter(organization=org_id).all()
    if events.count() < 1:
        return None
    customers = Customer.objects.all()
    i = 0
    j = 0
    while i < amount and j < amount * 5:
        customer = random.choice(customers)
        event = random.choice(events)
        if Visit.objects.filter(customer=customer, event=event).count() == 0:
            transaction = Transaction.objects.create(customer=customer, organization=organization, amount=5, method='CA')
            Visit.objects.create(customer=customer, event=event, transaction=transaction)
            customer.visits += 1
            customer.save()
            i += 1
        j += 1

class BuildOrganization(APIView):
    def get(self, request, frmt=None):
        name = names[random.randint(0, len(names)-1)]
        orgName = name + "'s organziation"
        orgEmail = name + '@gmail.com'
        org = Organization.objects.create(name=orgName)
        if request.query_params.get('full'):
            createEvents(20, org.id)
            createCustomers(350)
            createVisits(1500, org.id)
        return HttpResponse('Built Organization')


class BuildEvent(APIView):
    def get(self, request, pk, frmt=None):
        amount = request.query_params.get('amount', None)
        if amount is None:
            amount = 25
        amount = int(amount)
        if amount < 0:
            raise HttpResponse('Bad amount')
        createEvents(amount, pk)
        return HttpResponse('Built Event')


class BuildCustomer(APIView):
    def get(self, request, frmt=None):
        amount = request.query_params.get('amount', None)
        if amount is None:
            amount = 1000
        amount = int(amount)
        if amount < 0:
            raise HttpResponse('Bad amount')
        createCustomers(amount)
        return HttpResponse('Built  Customer')


class BuildVisit(APIView):
    def get(self, request, pk, frmt=None):
        amount = request.query_params.get('amount', None)
        if amount is None:
            amount = 2500
        amount = int(amount)
        if amount < 0:
            raise HttpResponse('Bad amount')
        createVisits(amount, pk)
        return HttpResponse('Built Visit')



