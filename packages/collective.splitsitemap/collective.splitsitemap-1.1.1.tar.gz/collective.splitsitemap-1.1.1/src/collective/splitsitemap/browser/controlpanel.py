# -*- encoding: utf-8 -*-

from collective.splitsitemap import _
from collective.splitsitemap.interfaces import ISplitSitemapSettings
from plone.app.registry.browser.controlpanel import (ControlPanelFormWrapper,
                                                     RegistryEditForm)
from plone.z3cform import layout


class SitemapControlPanelForm(RegistryEditForm):
    schema = ISplitSitemapSettings
    id = "sitemap-settings"
    label = _(u"Split Sitemap Settings")
    description = _(u"Configure here all of split sitemap related settings")


SitemapControlPanelView = layout.wrap_form(
    SitemapControlPanelForm, ControlPanelFormWrapper)
