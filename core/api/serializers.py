from rest_framework import serializers


class TokenAPIViewResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshAPIViewResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
