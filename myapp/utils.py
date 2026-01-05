import jwt
from datetime import datetime, timedelta
from django.conf import settings

def get_tokens_for_user(user):
    access_payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow()
    }

    refresh_payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow()
    }

    return {
        "access": jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256"),
        "refresh": jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")
    }