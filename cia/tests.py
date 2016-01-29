from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cia.models import Customer


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
    def test_create_event(self):
        """
        Ensure we can create a new event object.
        """

    def test_create_event_failure(self):
        """
        Ensure we can still fail at creating a new event object.
        """


