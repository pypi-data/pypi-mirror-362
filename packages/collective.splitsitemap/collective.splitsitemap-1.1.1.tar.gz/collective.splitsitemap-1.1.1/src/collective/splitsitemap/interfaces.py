# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.splitsitemap import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveSplitsitemapLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ISplitSitemapSettings(Interface):

    enable_split_sitemaps = schema.Bool(
        title=_(
            u"Enable split sitemaps"
        ),
        description=_(
            u"By enabling this setting, the sitemap is split as per "
            u"https://www.sitemaps.org/protocol.html"
        ),
        required=False,
        default=False,
    )

    add_auto_view = schema.Bool(
        title=_(
            u"Automatically add /view at the end of URLs"
        ),
        description=_(
            u"By default Plone adds '/view' at the end of the URLs for some "
            u"specific content types, such as Files and Images. Disabling "
            u"this checkbox will prevent this behavior to happen in sitemap "
            u"generation, and instead the real URL to the item will be used"
        ),
        required=False,
        default=False,
    )

    items_per_sitemap = schema.Int(
        title=_(u"Items per sitemap"),
        description=_(
            u"Specify how many items should be included per sitemap. Acording "
            u"to the protocol, sitemap should have no more than 50.000 items, "
            u"and it should be smaller than 50MB. It is advisable to specify "
            u"a smaller number than 50.000 just to be in the safe side, "
            u"around 40.000."
        ),
        required=False,
        default=40000,
    )

    async_sitemap_generation = schema.Bool(
        title=_(
            u"Sitemaps are generated from a script"
        ),
        description=_(
            u"Enable this if you are generating the sitemaps using the "
            u"instance script provided with the package. Check the product "
            u"README for more information"
        ),
        required=False,
        default=False,
    )

    ignored_types = schema.List(
        title=_(
            u"Select content types to NOT include in sitemap"
        ),
        description=_(
            u"Select from this list which content types should not be "
            u"included when generating the sitemap"
        ),
        required=False,
        default=list(),
        value_type = schema.Choice(
            title=_(u"Content types"),
            vocabulary="plone.app.vocabularies.UserFriendlyTypes",
        )
    )

    ignored_paths = schema.List(
        title=_(
            u"Paths to ignore"
        ),
        description=_(
            u"You can list paths in here to ignore, one per line. If you "
            u"add ':-1' at the end, you will be ignoring that path and all "
            u"of its children. Check the product's README for more information"
        ),
        required=False,
        default=list(),
        value_type = schema.TextLine(
            title=_(u"Path"),
        )
    )
