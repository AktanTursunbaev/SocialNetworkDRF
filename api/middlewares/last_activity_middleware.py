from django.utils.timezone import now
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        if request.user.is_authenticated:
            request.user.last_activity = now()
            request.user.save()
        response = self.get_response(request)
        return response

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        try:
            user_jwt = JWTAuthentication().authenticate(Request(request))
            if user_jwt is not None:
                return user_jwt[0]
        except:
            pass
        return user
