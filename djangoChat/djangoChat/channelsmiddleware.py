import jwt
from urllib.parse import parse_qs
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django.db import close_old_connections
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


@database_sync_to_async
def get_user(token):
    try:
        # This will handle checking if the token is valid, as well as the `token_type`
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        return AnonymousUser()
    else:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        return get_user_model().objects.get(id=decoded_data["user_id"])

class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token
        query_string = parse_qs(scope["query_string"].decode("utf8"))
        token = query_string.get("token")
        if not token:
            raise ValueError("Missing token")
        else:
            token = token[0]

        # Try to authenticate the user
        scope["user"] = await get_user(token)

        # Print the user if connection is successful
        print(f"Connected user: {scope['user']}")

        # Then call the inner application, and pass it the scope, send and receive
        return await self.inner(scope, receive, send)