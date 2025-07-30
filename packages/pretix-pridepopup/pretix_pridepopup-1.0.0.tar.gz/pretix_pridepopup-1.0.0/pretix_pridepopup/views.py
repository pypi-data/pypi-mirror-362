from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin

from pretix_pridepopup.forms import PridePopUpSettingsForm


class PridePopUpSettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = PridePopUpSettingsForm
    template_name = "pretix_pridepopup/settings.html"
    permission = "can_change_settings"
