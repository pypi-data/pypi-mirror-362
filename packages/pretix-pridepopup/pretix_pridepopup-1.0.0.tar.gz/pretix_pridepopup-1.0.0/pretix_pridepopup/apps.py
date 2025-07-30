from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_pridepopup"
    verbose_name = "Pride Pop-up"

    class PretixPluginMeta:
        name = gettext_lazy("Pride Pop-up")
        author = "Martin Gross"
        description = gettext_lazy(
            "Display the Pride Pop-up (https://www.accept.lgbt/) on your pretix shop"
        )
        visible = True
        version = __version__
        category = "CUSTOMIZATION"
        compatibility = "pretix>=2.7.0"
        settings_links = []
        navigation_links = []

    def ready(self):
        from . import signals  # NOQA
