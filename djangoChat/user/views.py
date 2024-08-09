from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView

from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ReceiverSerializer, SenderSerializer, ProfileSerializer
from .models import User, FriendRequest
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
class UserRegister(GenericAPIView):
    """
    Register API

    Enter username, email, first name, last name and password to register
    (email, first name and last name are optional)
    """
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Login(GenericAPIView):
    """
    Login API

    Enter username and password to get access token and refresh token
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = TokenObtainPairSerializer.get_token(user)
            data = {
                'user_id': user.id,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error_message': 'Invalid username or password',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        
class SendFriendRequest(GenericAPIView):
    """
    Send Friend Request API

    Enter the username of the user you want to send a friend request 
    """
    serializer_class = ReceiverSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                try:
                    sender = User.objects.get(id=request.user.id)
                    receiver = User.objects.get(id=serializer.validated_data["id"])
                    if sender != receiver:
                        FriendRequest.objects.create(sender=sender, receiver=receiver)
                        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message": "You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AcceptFriendRequest(GenericAPIView):
    """
    Accept Friend Request API

    Enter the id of the user you want to accept the friend request from
    """
    serializer_class = SenderSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                try:
                    receiver = User.objects.get(id=serializer.validated_data["id"])
                    sender = request.user
                    friend_request = FriendRequest.objects.get(sender=receiver, receiver=sender)
                    friend_request.delete()
                    receiver.friends.add(sender)
                    sender.friends.add(receiver)
                    return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                except FriendRequest.DoesNotExist:
                    return Response({"message": "Friend request does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
            
class RejectFriendRequest(GenericAPIView):
    """
    Reject Friend Request API

    Enter the username of the user you want to reject the friend request from
    """
    serializer_class = SenderSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                try:
                    sender = User.objects.get(id=request.user.id)
                    receiver = User.objects.get(id=serializer.validated_data["id"])
                    friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
                    friend_request.delete()
                    return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                except FriendRequest.DoesNotExist:
                    return Response({"message": "Friend request does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
    
class FriendRequestList(APIView):
    """
    List of Friend Requests API

    Get a list of friend requests
    """
    queryset = FriendRequest.objects.all()

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            friend_requests = FriendRequest.objects.filter(receiver=user)
            friend_requests_list = []
            for friend_request in friend_requests:
                sender_serializer = ProfileSerializer(friend_request.sender)
                friend_requests_list.append(sender_serializer.data)
            return Response({"friend_requests": friend_requests_list}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
class FriendList(APIView):
    """
    List of Friends API

    Get a list of friends
    """
    queryset = User.objects.all()

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            friends = user.friends.all().order_by('last_name')
            friends_list = []
            for friend in friends:
                friend_serializer = ProfileSerializer(friend)
                friends_list.append(friend_serializer.data)
            return Response({"friends": friends_list}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
class Profile(APIView):
    """
    Profile API

    Get the profile of the user
    """
    queryset = User.objects.all()

    def get(self, request, user_id=None):
        if request.user.is_authenticated:
            if user_id is not None:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                user = request.user
            serializer = ProfileSerializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data.get('phoneNumber')
        user = User.objects.filter(phoneNumber=phone_number).first()
        if user:
            email = user.email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://localhost:5173/reset-password/{uid}/{token}"
            send_mail(
                "Password Reset Request",
                f"To reset your password, visit the following link: {reset_url}",
                "noreply@yourdomain.com",
                [email],
            )
            return Response({"message": "If an account with the provided phone number exists, we have sent an email with password reset instructions."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetConfirmView(APIView):
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Password reset unsuccessful."}, status=status.HTTP_400_BAD_REQUEST)
        
from django.contrib.auth.hashers import check_password

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not check_password(old_password, user.password):
            return Response({"error": "Old password is not correct"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

class VerifyResetPasswordToken(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
                            
class ProfileChangeView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchProfile(APIView):
    """
    Search Profile API

    Search for a user by phone number
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        phoneNumber = request.query_params.get('phone')
        print(phoneNumber)
        if phoneNumber is not None:
            users = User.objects.filter(phoneNumber__icontains=phoneNumber).exclude(id=request.user.id)
            print(users)
            users_list = []
            for user in users:
                user_serializer = ProfileSerializer(user, context={'request': request})
                users_list.append(user_serializer.data)
            return Response({"users": users_list}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Phone number not provided"}, status=status.HTTP_400_BAD_REQUEST)