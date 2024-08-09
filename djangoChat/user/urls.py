from django.urls import path
from .views import UserRegister, Login, SendFriendRequest, AcceptFriendRequest,\
      RejectFriendRequest, FriendRequestList, FriendList, Profile,PasswordResetConfirmView, \
      ChangePasswordView, ProfileChangeView, SearchProfile,PasswordResetRequestView,\
        VerifyResetPasswordToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('token/',  TokenVerifyView.as_view(), name='token_verify'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('send-friend-request/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('accept-friend-request/', AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('reject-friend-request/', RejectFriendRequest.as_view(), name='reject_friend_request'),
    path('friend-requests/', FriendRequestList.as_view(), name='friend_requests'),
    path('friends/', FriendList.as_view(), name='friends'),
    path('profile/<int:user_id>/', Profile.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile-change/', ProfileChangeView.as_view(), name='profile_change'),
    path('search-profile/', SearchProfile.as_view(), name='search_profile'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('verify/<uidb64>/<token>/', VerifyResetPasswordToken.as_view(), name='password_reset_confirm'),


    
]
