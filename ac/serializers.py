from rest_framework import serializers


class ACPowerCommandRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=[
            ("on", "On"),
            ("off", "Off"),
            ("toggle", "Toggle"),
        ]
    )


class ACPowerCommandResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    action = serializers.ChoiceField(choices=["on", "off", "toggle"])
    result = serializers.JSONField()


class ACPowerCommandInvalidResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class ACPowerStatusResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    result = serializers.JSONField()


class HomeAssistantErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    error = serializers.CharField()
