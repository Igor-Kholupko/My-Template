from django.contrib.admin import AdminSite as _AdminSite, register as _register
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class AdminSite(_AdminSite):
    """
    Overriding of default AdminSite with custom title, header and url values.
    """
    # Text to put at the end of each page's <title>.
    site_title = _('Templater site admin')

    # Text to put in each page's <h1>.
    site_header = _('Templater administration')

    # URL for the "View site" link at the top of each admin page.
    site_url = reverse_lazy('home')

    def get_model_admin(self, model):
        return self._registry.get(model)


site = AdminSite()


def register(*models):
    return _register(*models, site=site)
