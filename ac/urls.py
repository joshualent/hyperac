from django.urls import path
from .views import ACPowerView

urlpatterns = [
    path("power/", ACPowerView.as_view(), name="ac-power"),
]
