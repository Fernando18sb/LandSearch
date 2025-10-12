from django.urls import path
from .views import (
    HouseDetailView, HouseCreateView,
    HouseListView, HouseUpdateView,
    HouseDeleteView, UserHouseListView,
)

urlpatterns = [
    path('', HouseListView.as_view(), name='blog'),
    path('new/', HouseCreateView.as_view(), name='create'),
    path('user/<str:username>/', UserHouseListView.as_view(), name='house-owner'),
    path('detail/<str:access_hash>/', HouseDetailView.as_view(), name='detail'),
    path('detail/<str:access_hash>/update/', HouseUpdateView.as_view(), name='update'),
    path('detail/<str:access_hash>/delete/', HouseDeleteView.as_view(), name='delete')
]