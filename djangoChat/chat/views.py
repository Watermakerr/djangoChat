from django.shortcuts import render
from django.db import models
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status

from user.models import User
from .serializers import UserSerializer, MessageSerializer, UserLastMessageSerializer
from .models import Message



# Create your views here.
def index(request):
    return render(request, 'index/index.html')


class MessagedUsersView(APIView):
    '''
    Get all users that the current user has messaged with.

    This view is used to get all users that the current user has messaged with.
    '''

    def get_queryset(self):
        return get_user_model().objects.all()
    
    def get(self, request, format=None):
        if request.user.is_authenticated:
            sent_users = get_user_model().objects.filter(receiver__sender=request.user).distinct()
            received_users = get_user_model().objects.filter(sender__receiver=request.user).distinct()
            messaged_users = sent_users | received_users
            serializer = UserLastMessageSerializer(messaged_users, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
class UserSearchView(APIView):
    '''
    Search for users.

    This view is used to search for users.

    To search for users, send a GET request with the query parameter 'q' set to the search query.
    '''
    def get_queryset(self):
        return User.objects.all()
    
    def get(self, request, format=None):
        query = request.GET.get('q', '')
        users = User.objects.filter(username__icontains=query)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class MessageViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for messages.

    This viewset is used to get and send messages.
    put the id of the user you want to chat with in the url.
    '''

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs['user_id']
        queryset = Message.objects.filter(
            models.Q(sender=self.request.user, receiver__id=other_user_id) | 
            models.Q(receiver=self.request.user, sender__id=other_user_id)
        ).order_by('id')
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
