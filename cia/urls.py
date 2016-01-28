from django.conf.urls import url
from cia.views import (CustomerDetailAPIView, CustomerListAPIView, EventDetailAPIView, EventListAPIView,
OrganizationDetailAPIView, OrganizationListAPIView, TransactionDetailAPIView, TransactionListAPIView,
VisitDetailAPIView, VisitListAPIView)


urlpatterns = [
    url(r'^customer/$', CustomerListAPIView.as_view(), name='customer-list'),
    url(r'^customer/(?P<pk>[0-9]+)/$', CustomerDetailAPIView.as_view(), name='customer-detail'),
    url(r'^event/$', EventListAPIView.as_view(), name='event-list'),
    url(r'^event/(?P<pk>[0-9]+)/$', EventDetailAPIView.as_view(), name='event-detail'),
    url(r'^organization/$', OrganizationListAPIView.as_view(), name='organization-list'),
    url(r'^organization/(?P<pk>[0-9]+)/$', OrganizationDetailAPIView.as_view(), name='organization-detail'),
    url(r'^transaction/$', TransactionListAPIView.as_view(), name='transaction-list'),
    url(r'^transaction/(?P<pk>[0-9]+)/$', TransactionDetailAPIView.as_view(), name='transaction-detail'),
    url(r'^visit/$', VisitListAPIView.as_view(), name='visit-list'),
    url(r'^visit/(?P<pk>[0-9]+)/$', VisitDetailAPIView.as_view(), name='visit-detail')
]



