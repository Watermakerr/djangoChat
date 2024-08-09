from rest_framework import serializers

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', "gender",\
                  "birth_date", "phoneNumber"]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class ReceiverSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        """
        Check if user exists
        """
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

class SenderSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_sender(self, value):
        """
        Check if user exists
        """
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
    
class ProfileSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', "gender", "birth_date", "phoneNumber", 'is_friend']

    def get_is_friend(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.friends.filter(id=request.user.id).exists()
        return False