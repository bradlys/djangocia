from cia.models import Customer, Event, Organization, Visit, Transaction
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    last_modified_date = serializers.DateTimeField(read_only=True)
    visits = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'birthday', 'visits', 'created_date', 'last_modified_date')


class EventSerializer(serializers.ModelSerializer):
    last_modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'organization', 'created_date', 'last_modified_date')


class OrganizationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    last_modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Organization
        fields = ('id','name','email', 'created_date', 'last_modified_date')


class TransactionSerializer(serializers.ModelSerializer):
    last_modified_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'organization', 'method', 'created_date', 'last_modified_date')


class VisitSerializer(serializers.ModelSerializer):
    last_modified_date = serializers.DateTimeField(read_only=True)
    customer = serializers.HyperlinkedRelatedField(read_only=True, view_name='customer-detail')
    transaction = serializers.HyperlinkedRelatedField(read_only=True, view_name='transaction-detail')
    event = serializers.HyperlinkedRelatedField(read_only=True, view_name='event-detail')

    class Meta:
        model = Visit
        fields = ('id', 'customer', 'event', 'transaction', 'created_date', 'last_modified_date')

