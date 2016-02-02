from cia.models import Customer, Event, Organization, Visit, Transaction
from cia.serializers import CustomerSerializer, EventSerializer, OrganizationSerializer, TransactionSerializer, VisitSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import django_filters
from django.conf import settings
from rest_framework.settings import api_settings
from rest_framework.pagination import _get_displayed_page_numbers


class PaginatedAPIView(APIView):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset, request):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset=queryset, request=request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class CustomerListAPIView(APIView):

    def get(self, request, frmt=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, frmt=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, frmt=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, frmt=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, frmt=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventSearchForCustomerAPIView(PaginatedAPIView):

    def get(self, request, pk, frmt=None):
        customers = Customer.objects.all()
        name = request.query_params.get('name', None)
        if name is not None:
            # searching for customers by name and returning visit info along with it
            customers = customers.filter(name__contains=name)
        customers = customers.order_by('-visits', 'name', 'id')
        page = self.paginate_queryset(customers, self.request)
        if page is not None:
            serializer = CustomerSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)



class EventListAPIView(APIView):

    def get(self, request, frmt=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, frmt=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, frmt=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, frmt=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, frmt=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationListAPIView(APIView):

    def get(self, request, frmt=None):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    def post(self, request, frmt=None):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Organization.objects.get(pk=pk)
        except Organization.DoesNotExist:
            raise Http404

    def get(self, request, pk, frmt=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def put(self, request, pk, frmt=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, frmt=None):
        organization = self.get_object(pk)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionListAPIView(APIView):

    def get(self, request, frmt=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, frmt=None):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, frmt=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, frmt=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, frmt=None):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VisitListAPIView(APIView):

    def get(self, request, frmt=None):
        visits = Visit.objects.all()
        serializer = VisitSerializer(visits, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, frmt=None):
        serializer = VisitSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            raise Http404

    def get(self, request, pk, frmt=None):
        visit = self.get_object(pk)
        serializer = VisitSerializer(visit, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, frmt=None):
        visit = self.get_object(pk)
        serializer = VisitSerializer(visit, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, frmt=None):
        visit = self.get_object(pk)
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




