from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .home_assistant import (
    turn_ac_off,
    turn_ac_on,
    toggle_ac,
    get_ac_status,
    HomeAssistantError,
)
from .serializers import (
    ACPowerCommandRequestSerializer,
    ACPowerCommandResponseSerializer,
    ACPowerStatusResponseSerializer,
    ACPowerCommandInvalidResponseSerializer,
    HomeAssistantErrorResponseSerializer,
)


class ACPowerView(APIView):
    # extend schema for get and post method for OpenAPI schema generation
    @extend_schema(
        responses={
            200: ACPowerStatusResponseSerializer,
            502: HomeAssistantErrorResponseSerializer,
        },
    )
    def get(self, request):
        try:
            result = get_ac_status()

        except HomeAssistantError as exc:
            return Response(
                {"detail": "Home Assistant request failed", "error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response({"success": True, "result": result})

    @extend_schema(
        request=ACPowerCommandRequestSerializer,
        responses={
            200: ACPowerCommandResponseSerializer,
            400: ACPowerCommandInvalidResponseSerializer,
            502: HomeAssistantErrorResponseSerializer,
        },
    )
    def post(self, request):
        action = request.data.get("action")

        try:
            if action == "on":
                result = turn_ac_on()
            elif action == "off":
                result = turn_ac_off()
            elif action == "toggle":
                result = toggle_ac()
            else:
                return Response(
                    {"detail": "action must be one of: on, off, toggle"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except HomeAssistantError as exc:
            return Response(
                {"detail": "Home Assistant request failed", "error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({"success": True, "action": action, "result": result})
