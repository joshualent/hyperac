import httpx
from django.conf import settings


class HomeAssistantError(Exception):
    pass


def call_ha_service(domain: str, service: str, entity_id: str):
    url = f"{settings.HOME_ASSISTANT_URL.rstrip('/')}/api/services/{domain}/{service}"

    try:
        response = httpx.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.HOME_ASSISTANT_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"entity_id": entity_id},
            timeout=10,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HomeAssistantError(str(exc)) from exc

    return response.json()


def toggle_ac():
    return call_ha_service("switch", "toggle", settings.HOME_ASSISTANT_AC_ENTITY_ID)


def turn_ac_on():
    return call_ha_service("switch", "turn_on", settings.HOME_ASSISTANT_AC_ENTITY_ID)


def turn_ac_off():
    return call_ha_service("switch", "turn_off", settings.HOME_ASSISTANT_AC_ENTITY_ID)


def get_ac_status():
    url = f"{settings.HOME_ASSISTANT_URL.rstrip('/')}/api/states/{settings.HOME_ASSISTANT_AC_ENTITY_ID}"

    try:
        response = httpx.get(
            url,
            headers={
                "Authorization": f"Bearer {settings.HOME_ASSISTANT_TOKEN}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HomeAssistantError(str(exc)) from exc

    result = response.json().get("result")
    state = result.get("state")

    return {
        "state": state,
        "is_on": state == "on",
        "last_changed": result.get("last_changed"),
        "last_reported": result.get("last_reported"),
        "last_updated": result.get("last_updated"),
    }
