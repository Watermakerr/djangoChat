from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import index, MessagedUsersView, UserSearchView, MessageViewSet

urlpatterns = [
    path('', index, name='index'),
    path('messaged-users/', MessagedUsersView.as_view(), name='messaged-users'),
    path('search-users/', UserSearchView.as_view(), name='search-users'),
    path('messages/<int:user_id>/', MessageViewSet.as_view({'get': 'list'}), name='messages'),
]

