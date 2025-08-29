from django.urls import path
from .views import UserProfileView,AddressListCreateView,AddressDetailView

urlpatterns = [
    path('profile/',UserProfileView.as_view(),name='user-profile'),
    path('addresses/',AddressListCreateView.as_view(),name='address-list'),
    path('addresses/<int:pk>/',AddressDetailView.as_view(),name='address-detail')
]
