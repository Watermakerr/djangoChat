from rest_framework import serializers

from .models import Message
from user.models import User
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id','username', 'first_name', 'last_name'


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'
        ordering = ['-timestamp']

class LastMessageSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Message 
        fields = ('id','message', 'timestamp')

class UserLastMessageSerializer(serializers.ModelSerializer): 
    last_message = serializers.SerializerMethodField()

    class Meta: 
        model = User 
        fields = ('id', 'first_name', 'last_name', 'last_message')

    def get_last_message(self, obj):
        request = self.context.get('request')
        latest_message = Message.objects.filter(
            Q(sender=obj, receiver=request.user) | Q(sender=request.user, receiver=obj)
        ).order_by('-id').first()
        return LastMessageSerializer(latest_message).data if latest_message else None
