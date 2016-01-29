from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cia.models import Customer, Event, Organization, Transaction
from decimal import *

class CustomerTests(APITestCase):
    def test_create_customer(self):
        """
        Ensure we can create a new customer object.
        """
        url = reverse('customer-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().name, 'DabApps')
        data = {'name':'Jimmy Bob', 'birthday':'1990-08-28'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(str(Customer.objects.get(name='Jimmy Bob').birthday), '1990-08-28')
        data['email'] = 'bimbob@yipyip.com'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(Customer.objects.filter(name='Jimmy Bob').count(), 2)
        # supplying read only parameters shouldn't affect anything (they should be ignored)
        data['visits'] = 342
        # change the name, and this isn't read only
        data['name'] = 'Hard Names'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 4)
        self.assertEqual(response.data.get('visits'), 0)
        self.assertEqual(Customer.objects.get(name='Hard Names').visits, 0)

    def test_create_customer_failure(self):
        """
        Ensure we can still fail at creating a new customer object.
        """
        url = reverse('customer-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'birthday':'1990-08-28'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'name':''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'name':'Jimmy', 'birthday':'1990-08-32'}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['birthday'] = '1990-08-28'
        data['email'] = 'abad emailaddress@gmail.com'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)

    def test_get_customer_detail(self):
        """
        Get a newly created customer detail via API methods
        """
        customerList = reverse('customer-list')
        customerDetail = reverse('customer-detail', kwargs={'pk':1})
        data = {'name':'Jimmy Bob', 'birthday':'1990-08-28'}
        self.client.post(customerList, data, format='json')
        response = self.client.get(customerDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData['name'], 'Jimmy Bob')

    def test_get_customer_detail(self):
        """
        Get a newly created customer list via API methods
        """
        customerList = reverse('customer-list')
        data = {'name':'Jimmy Bob', 'birthday':'1990-08-28'}
        self.client.post(customerList, data, format='json')
        response = self.client.get(customerList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData[0]['name'], 'Jimmy Bob')

    def test_put_customer(self):
        """
        Put a newly created customer via API methods
        """
        customerList = reverse('customer-list')
        customerDetail = reverse('customer-detail', kwargs={'pk':1})
        data = {'name':'Jimmy Bob', 'birthday':'1990-08-28'}
        self.client.post(customerList, data, format='json')
        response = self.client.get(customerDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.get(name='Jimmy Bob').name, 'Jimmy Bob')
        data['name'] = 'Billy Bob'
        response = self.client.put(customerDetail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.get(name='Billy Bob').name, 'Billy Bob')
        self.assertEqual(Customer.objects.count(), 1)

    def test_delete_customer(self):
        """
        Delete a newly created customer via API methods
        """
        customerList = reverse('customer-list')
        data = {'name':'Jimmy Bob', 'birthday':'1990-08-28'}
        self.client.post(customerList, data, format='json')
        customerDetail = reverse('customer-detail', kwargs={'pk':1})
        response = self.client.delete(customerDetail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)


class EventTests(APITestCase):
    def setUp(self):
        self.organization_id = Organization.objects.create(name="Bobby's Organization").id

    def test_create_event(self):
        """
        Ensure we can create a new event object.
        """
        eventList = reverse('event-list')
        data = {'name':'Best Event', 'date':'2001-03-20', 'organization': self.organization_id}
        response = self.client.post(eventList, data, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['name'], 'Best Event')
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get(name='Best Event').name, 'Best Event')

    def test_create_event_failure(self):
        """
        Ensure we can still fail at creating a new event object.
        """
        eventList = reverse('event-list')
        data = {}
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['name'] = ''
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['name'] = 'banana'
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['date'] = ''
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['date'] = '2014-52-12'
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['date'] = '2014-01-01'
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['organization'] = 2
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['organization'] = ''
        response = self.client.post(eventList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 0)

    def test_get_event_detail(self):
        """
        Get a newly created event detail via API methods
        """
        eventList = reverse('event-list')
        eventDetail = reverse('event-detail', kwargs={'pk':1})
        data = {'name':'Bobs Event', 'date':'2020-08-28', 'organization': 1}
        self.client.post(eventList, data, format='json')
        response = self.client.get(eventDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData['name'], 'Bobs Event')

    def test_get_event_list(self):
        """
        Get a newly created event list via API methods
        """
        eventList = reverse('event-list')
        data = {'name':'Bobs Event', 'date':'2020-08-28', 'organization': 1}
        self.client.post(eventList, data, format='json')
        response = self.client.get(eventList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData[0]['name'], 'Bobs Event')

    def test_put_event(self):
        """
        Put a newly created event via API methods
        """
        eventList = reverse('event-list')
        eventDetail = reverse('event-detail', kwargs={'pk':1})
        data = {'name':'Bobs Event', 'date':'2020-08-28', 'organization': 1}
        self.client.post(eventList, data, format='json')
        response = self.client.get(eventDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(name='Bobs Event').name, 'Bobs Event')
        data['name'] = 'Joes Event'
        response = self.client.put(eventDetail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(name='Joes Event').name, 'Joes Event')
        self.assertEqual(Event.objects.count(), 1)

    def test_delete_event(self):
        """
        Delete a newly created event via API methods
        """
        eventList = reverse('event-list')
        data = {'name':'Bobs Event', 'date':'2020-08-28', 'organization': 1}
        self.client.post(eventList, data, format='json')
        eventDetail = reverse('event-detail', kwargs={'pk':1})
        response = self.client.delete(eventDetail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)


class OrganizationTests(APITestCase):

    def test_create_organization(self):
        """
        Ensure we can create a new organization object.
        """
        organizationList = reverse('organization-list')
        data = {'name':'Best organization', 'email':'best@org.org'}
        response = self.client.post(organizationList, data, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['name'], 'Best organization')
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Organization.objects.get(name='Best organization').name, 'Best organization')

    def test_create_organization_failure(self):
        """
        Ensure we can still fail at creating a new organization object.
        """
        organizationList = reverse('organization-list')
        data = {}
        response = self.client.post(organizationList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['name'] = ''
        response = self.client.post(organizationList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['email'] = ''
        response = self.client.post(organizationList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['email'] = 'ljasdfjklaxf'
        response = self.client.post(organizationList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['name'] = 'best organization'
        response = self.client.post(organizationList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Organization.objects.count(), 0)

    def test_get_organization_detail(self):
        """
        Get a newly created organization detail via API methods
        """
        organizationList = reverse('organization-list')
        organizationDetail = reverse('organization-detail', kwargs={'pk':1})
        data = {'name':'Bobs organization', 'email':'banana@gmail.com'}
        self.client.post(organizationList, data, format='json')
        response = self.client.get(organizationDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData['name'], 'Bobs organization')

    def test_get_organization_list(self):
        """
        Get a newly created organization list via API methods
        """
        organizationList = reverse('organization-list')
        data = {'name':'Bobs organization', 'email':'banana@gmail.com'}
        self.client.post(organizationList, data, format='json')
        response = self.client.get(organizationList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData[0]['name'], 'Bobs organization')

    def test_put_organization(self):
        """
        Put a newly created organization via API methods
        """
        organizationList = reverse('organization-list')
        organizationDetail = reverse('organization-detail', kwargs={'pk':1})
        data = {'name':'Bobs organization', 'email':'banana@gmail.com'}
        self.client.post(organizationList, data, format='json')
        response = self.client.get(organizationDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(name='Bobs organization').name, 'Bobs organization')
        data['name'] = 'Joes organization'
        response = self.client.put(organizationDetail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(name='Joes organization').name, 'Joes organization')
        self.assertEqual(Organization.objects.count(), 1)

    def test_delete_organization(self):
        """
        Delete a newly created organization via API methods
        """
        organizationList = reverse('organization-list')
        data = {'name':'Bobs organization', 'email':'banana@gmail.com'}
        self.client.post(organizationList, data, format='json')
        organizationDetail = reverse('organization-detail', kwargs={'pk':1})
        response = self.client.delete(organizationDetail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 0)

class TransactionTests(APITestCase):

    def setUp(self):
        self.customer_id = Customer.objects.create(name='Banana-Man').id
        self.organization_id = Organization.objects.create(name="Bobby's Organization").id

    def test_create_transaction(self):
        """
        Ensure we can create a new transaction object.
        """
        transactionList = reverse('transaction-list')
        data = {'amount':7, 'method':'CA', 'customer': self.customer_id, 'organization': self.organization_id}
        response = self.client.post(transactionList, data, format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['amount'], '7.000')
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get(method='CA').customer.id, self.customer_id)

    def test_create_transaction_failure(self):
        """
        Ensure we can still fail at creating a new transaction object.
        """
        transactionList = reverse('transaction-list')
        data = {}
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['amount'] = ''
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['amount'] = 5
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['method'] = 'CA'
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['customer'] = self.customer_id
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['organization'] = self.organization_id
        del data['amount']
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['amount'] = None
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['amount'] = 5
        data['method'] = 'Cash'
        response = self.client.post(transactionList, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_get_transaction_detail(self):
        """
        Get a newly created transaction detail via API methods
        """
        transactionList = reverse('transaction-list')
        transactionDetail = reverse('transaction-detail', kwargs={'pk':1})
        data = {'amount':7, 'method':'CA', 'customer': self.customer_id, 'organization': self.organization_id}
        self.client.post(transactionList, data, format='json')
        response = self.client.get(transactionDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData['amount'], '7.000')

    def test_get_transaction_list(self):
        """
        Get a newly created transaction list via API methods
        """
        transactionList = reverse('transaction-list')
        data = {'amount':7, 'method':'CA', 'customer': self.customer_id, 'organization': self.organization_id}
        self.client.post(transactionList, data, format='json')
        response = self.client.get(transactionList)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonData = response.json()
        self.assertEqual(jsonData[0]['amount'], '7.000')

    def test_put_transaction(self):
        """
        Put a newly created transaction via API methods
        """
        transactionList = reverse('transaction-list')
        transactionDetail = reverse('transaction-detail', kwargs={'pk':1})
        data = {'amount':7, 'method':'CA', 'customer': self.customer_id, 'organization': self.organization_id}
        self.client.post(transactionList, data, format='json')
        response = self.client.get(transactionDetail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.get(pk=1).amount, Decimal('7.000'))
        data['amount'] = 9
        response = self.client.put(transactionDetail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.get(pk=1).amount, Decimal('9.000'))
        self.assertEqual(Transaction.objects.count(), 1)

    def test_delete_transaction(self):
        """
        Delete a newly created transaction via API methods
        """
        transactionList = reverse('transaction-list')
        data = {'amount':7, 'method':'CA', 'customer': self.customer_id, 'organization': self.organization_id}
        self.client.post(transactionList, data, format='json')
        transactionDetail = reverse('transaction-detail', kwargs={'pk':1})
        response = self.client.delete(transactionDetail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

