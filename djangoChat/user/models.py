from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models
choice = [(0, "Male"),[1, "Female"]]
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    friends = models.ManyToManyField("User", blank=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="userprofile_set",
        related_query_name="userprofile",
    )
    gender = models.IntegerField(choices=choice, default=0, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="userprofile_set",
        related_query_name="userprofile",
    )

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendrequest_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendrequest_receiver")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return str(self.sender) + " to " + str(self.receiver) + " at " + str(self.timestamp)