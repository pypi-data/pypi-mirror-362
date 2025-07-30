from django import forms
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm


class PridePopUpSettingsForm(SettingsForm):
    pridepopup_interval = forms.IntegerField(
        label=_("Display Pride Pop-up every"),
        required=True,
        min_value=0,
        initial=1,
        widget=forms.NumberInput(attrs={"addon_after": _("days")}),
    )
