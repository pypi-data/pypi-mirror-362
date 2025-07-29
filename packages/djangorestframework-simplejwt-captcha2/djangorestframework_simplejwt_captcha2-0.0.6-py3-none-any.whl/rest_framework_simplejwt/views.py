from typing import Optional
import random
import hashlib
import base64
import string
from captcha.image import ImageCaptcha, random_color
from io import BytesIO
from django.core.cache import cache
from django.utils.module_loading import import_string
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from .authentication import AUTH_HEADER_TYPES
from .exceptions import InvalidToken, TokenError
from .settings import api_settings


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class: Optional[type[BaseSerializer]] = None
    _serializer_class = ""

    www_authenticate_realm = "api"

    def get_serializer_class(self) -> type[BaseSerializer]:
        """
        If serializer_class is set, use it directly. Otherwise get the class from settings.
        """

        if self.serializer_class:
            return self.serializer_class
        try:
            return import_string(self._serializer_class)
        except ImportError as e:
            msg = f"Could not import serializer '{self._serializer_class}'"
            raise ImportError(msg) from e

    def get_authenticate_header(self, request: Request) -> str:
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER


token_obtain_pair = TokenObtainPairView.as_view()


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER


token_refresh = TokenRefreshView.as_view()


class TokenObtainSlidingView(TokenViewBase):
    """
    Takes a set of user credentials and returns a sliding JSON web token to
    prove the authentication of those credentials.
    """

    _serializer_class = api_settings.SLIDING_TOKEN_OBTAIN_SERIALIZER


token_obtain_sliding = TokenObtainSlidingView.as_view()


class TokenRefreshSlidingView(TokenViewBase):
    """
    Takes a sliding JSON web token and returns a new, refreshed version if the
    token's refresh period has not expired.
    """

    _serializer_class = api_settings.SLIDING_TOKEN_REFRESH_SERIALIZER


token_refresh_sliding = TokenRefreshSlidingView.as_view()


class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """

    _serializer_class = api_settings.TOKEN_VERIFY_SERIALIZER


token_verify = TokenVerifyView.as_view()


class TokenBlacklistView(TokenViewBase):
    """
    Takes a token and blacklists it. Must be used with the
    `rest_framework_simplejwt.token_blacklist` app installed.
    """

    _serializer_class = api_settings.TOKEN_BLACKLIST_SERIALIZER


token_blacklist = TokenBlacklistView.as_view()


class CaptchaVerifyView(generics.GenericAPIView):
    """
    Takes a token and captcha_verify it. Must be used with the
    `rest_framework_simplejwt.captcha_verify` app installed.
    """

    def calculation(self, symbol='*'):
        operators = ("+", "*", "-")
        operands = (random.randint(1, 10), random.randint(1, 100))
        operator = random.choice(operators)
        if operands[0] < operands[1] and "-" == operator:
            operands = (operands[1], operands[0])
        challenge = "%d%s%d" % (operands[0], operator, operands[1])
        return (
            "{}".format(challenge.replace("*", symbol)),
            str(eval(challenge)),
        )

    def number(self):
        result = random.sample(string.digits, api_settings.CAPTCHA_LENGTH)
        number_captcha = "".strip().join(result)
        return number_captcha

    def image_uuid(self):
        captcha_type = api_settings.CAPTCHA_TYPE
        if captcha_type == 'calculation':
            compute, captcha = self.calculation()
        else:
            compute, captcha = None, self.number()
        text = captcha + api_settings.SIGNING_KEY
        h = hashlib.md5()
        h.update(text.encode('utf-8'))
        uuid = h.hexdigest()
        cache.set(uuid, captcha, api_settings.CAPTCHA_CACHE_TIME)
        generator = ImageCaptcha()
        image = generator.generate_image(compute) if compute else generator.generate_image(captcha)
        generator.create_noise_curve(image, random_color(1, 255))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img = b"data:image/png;base64," + base64.b64encode(buffered.getvalue())
        data = {
            "uuid": uuid,
            "img": img,
        }
        return data

    def get(self, requests):
        data = self.image_uuid()

        return Response(data)


captcha_verify = CaptchaVerifyView.as_view()


class LoginCaptchaVerifyView(TokenViewBase):
    """
    Takes a token and login_captcha_verify it. Must be used with the
    `rest_framework_simplejwt.login_captcha_verify` app installed.
    """

    _serializer_class = api_settings.CAPTCHA_VERIFY_SERIALIZER


login_captcha_verify = LoginCaptchaVerifyView.as_view()
