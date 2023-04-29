from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class TokenAPIView(TokenObtainPairView):
    token_apiview_description = """
        Returns JWT tokens.

        Credentials for testing purposes:
        * e: admin@mail.com p: admin (SU + seller)
        * e: seller@mail.com p: seller
        * e: customer@mail.com p: customer
    """

    @swagger_auto_schema(
        operation_description=token_apiview_description,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshAPIView(TokenRefreshView):
    @swagger_auto_schema(
        operation_description="Returns refreshed access token.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
