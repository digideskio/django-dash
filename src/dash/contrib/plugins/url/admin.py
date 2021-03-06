__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BookmarkAdmin',)

import logging

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from dash.models import DashboardEntry
from dash.contrib.plugins.url.models import Bookmark
from dash.utils import update_plugin_data_for_entries

logger = logging.getLogger(__name__)

class BookmarkAdmin(admin.ModelAdmin):
    """
    Bookmark admin.
    """
    list_display = ('title', 'url', 'external', 'image')

    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'external', 'image')
        }),
    )

    class Meta:
        app_label = _('Bookmark')


    def save_model(self, request, obj, form, change):
        """
        Updating the bookmark plugin entries on bookmarks update.
        """
        super(BookmarkAdmin, self).save_model(request, obj, form, change)

        dashboard_entries = DashboardEntry._default_manager.filter(plugin_uid__startswith='bookmark_')
        try:
            update_plugin_data_for_entries(dashboard_entries=dashboard_entries, request=request)
        except Exception as e:
            logger.debug(str(e))


admin.site.register(Bookmark, BookmarkAdmin)
