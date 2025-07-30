from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.template.loader import get_template
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.middleware import _merge_csp, _parse_csp, _render_csp
from pretix.base.settings import settings_hierarkey
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import html_head, process_response


@receiver(html_head, dispatch_uid="pridepopup_html_head")
def html_head_presale(sender, request=None, **kwargs):
    template = get_template("pretix_pridepopup/presale_head.html")
    ctx = {
        "interval": sender.settings.pridepopup_interval,
    }
    return template.render(ctx)


@receiver(nav_event_settings, dispatch_uid="pridepopup_nav_event_settings")
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(
        request.organizer, request.event, "can_change_event_settings", request=request
    ):
        return []
    return [
        {
            "label": _("Pride Pop-up"),
            "url": reverse(
                "plugins:pretix_pridepopup:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_pridepopup",
        }
    ]


@receiver(signal=process_response, dispatch_uid="pridepopup_middleware_resp")
def signal_process_response(
    sender, request: HttpRequest, response: HttpResponse, **kwargs
):
    if "Content-Security-Policy" in response:
        h = _parse_csp(response["Content-Security-Policy"])
    else:
        h = {}

    csps = {
        "style-src": ["'sha256-jitL/q5kwk/i4TsCCNU08PlRBUSdilYYowPwFDL70yw='"],
    }

    _merge_csp(h, csps)

    if h:
        response["Content-Security-Policy"] = _render_csp(h)
    return response


settings_hierarkey.add_default("pridepopup_interval", 1, int)
