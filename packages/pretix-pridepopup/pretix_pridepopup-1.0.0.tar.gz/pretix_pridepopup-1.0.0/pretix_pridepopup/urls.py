from django.urls import path

from pretix_pridepopup.views import PridePopUpSettingsView

urlpatterns = [
    path(
        "control/event/<str:organizer>/<str:event>/settings/pridepopup/",
        PridePopUpSettingsView.as_view(),
        name="settings",
    ),
]
