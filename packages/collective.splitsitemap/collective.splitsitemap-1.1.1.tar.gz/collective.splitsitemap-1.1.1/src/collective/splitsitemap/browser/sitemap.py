# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from DateTime import DateTime
from collective.splitsitemap.interfaces import ISplitSitemapSettings
from gzip import GzipFile
from persistent.mapping import PersistentMapping
from plone import api
from plone.memoize import ram
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from six import BytesIO
from time import time
from zope.annotation import IAnnotations
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.publisher.interfaces import NotFound

import logging
import math
import six

try:
    from Products.CMFPlone.interfaces import ISiteSchema

    HAVE_P5 = True
except:
    HAVE_P5 = False


logger = logging.getLogger("collective.splitsitemap")
ANN_KEY = "collective.splitsitemap"


def _render_cachekey(fun, self, items=None):
    # Cache by filename
    mtool = getToolByName(self.context, "portal_membership")
    if not mtool.isAnonymousUser():
        raise ram.DontCache

    url = self.context.absolute_url()
    catalog = getToolByName(self.context, "portal_catalog")
    counter = catalog.getCounter()
    return "%s/%s/%s" % (url, self.filename, counter)


class SiteMapView(BrowserView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """

    template = ViewPageTemplateFile("sitemap.xml")
    index_template = ViewPageTemplateFile("sitemap_index_template.xml")

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.num_sitemaps = 0
        self.filename = "sitemap.xml.gz"
        self.split_filename = "sitemap%s.xml.gz"
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISplitSitemapSettings)

    def sitemaps(self):
        now = DateTime().ISO8601()
        items = list()
        for num in range(self.num_sitemaps):
            sitemap_n = num + 1
            loc = "%s/%s" % (
                self.context.absolute_url(),
                self.split_filename % sitemap_n,
            )
            items.append(
                {
                    "loc": loc,
                    "lastmod": now,
                    # 'changefreq': 'always',
                    #  hourly/daily/weekly/monthly/yearly/never
                    # 'prioriy': 0.5, # 0.0 to 1.0
                }
            )
        return items

    def objects(self, sitemap_n=None, total_items=None):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, "portal_catalog")
        utils = getToolByName(self.context, "plone_utils")

        query = {"portal_type": list()}
        for pt in utils.getUserFriendlyTypes():
            if pt not in self.settings.ignored_types:
                query["portal_type"].append(pt)
            else:
                logger.info("Ignoring content type: %s" % pt)

        if HAVE_P5:
            registry = getUtility(IRegistry)
            typesUseViewActionInListings = frozenset(
                registry.get("plone.types_use_view_action_in_listings", [])
            )
        else:
            sp = getToolByName(self.context, "portal_properties").site_properties
            typesUseViewActionInListings = frozenset(sp.typesUseViewActionInListings)

        is_plone_site_root = IPloneSiteRoot.providedBy(self.context)
        if not is_plone_site_root:
            query["path"] = "/".join(self.context.getPhysicalPath())

        query["is_default_page"] = True
        default_page_modified = OOBTree()

        keywords = self.extra_search_parameters()

        split_sitemap = sitemap_n and total_items and True or False

        for item in catalog.searchResults(query, Language='all', **keywords):
            key = item.getURL().rsplit("/", 1)[0]
            value = (item.modified.micros(), item.modified.ISO8601())
            default_page_modified[key] = value

        returned = 0
        to_skip = 0
        # The plone site root is not catalogued.
        if is_plone_site_root and (sitemap_n is None or sitemap_n == 1):
            loc = self.context.absolute_url()
            date = self.context.modified()
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            yield {
                "loc": loc,
                "lastmod": lastmod,
                # 'changefreq': 'always',
                #  hourly/daily/weekly/monthly/yearly/never
                # 'prioriy': 0.5, # 0.0 to 1.0
            }
            returned += 1

        if is_plone_site_root and not (sitemap_n is None or sitemap_n == 1):
            to_skip -= 1

        if split_sitemap:
            to_skip += (sitemap_n - 1) * total_items

        query["is_default_page"] = False
        for item in catalog.searchResults(query, Language='all', **keywords):
            loc = item.getURL()
            ignore_item = False
            if self.settings.ignored_paths:
                for ignore_path in self.settings.ignored_paths:
                    ignored_url = u"%s%s" % (self.context.absolute_url(), ignore_path)

                    if ignored_url.endswith(":-1"):
                        if loc.startswith(ignored_url[:-3]):
                            ignore_item = True
                            break
                    else:
                        if loc == ignored_url:
                            ignore_item = True
                            break

            if ignore_item:
                logger.info("Not including: %s" % loc)
                continue

            if to_skip > 0:
                to_skip -= 1
                continue

            if total_items and returned == total_items:
                return

            date = item.modified
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            if self.settings.add_auto_view:
                if item.portal_type in typesUseViewActionInListings:
                    loc += "/view"
            yield {
                "loc": loc,
                "lastmod": lastmod,
                # 'changefreq': 'always',
                #  hourly/daily/weekly/monthly/yearly/never
                # 'prioriy': 0.5, # 0.0 to 1.0
            }
            returned += 1

    def _generate(self, items=None):
        """Generates the Gzipped sitemap."""
        alsoProvides(self.request, IDisableCSRFProtection)

        results = ""
        ctx_path = "/".join(self.context.getPhysicalPath())
        logger.info("Generating sitemap.xml.gz for %s" % ctx_path)

        if items:
            logger.info("Maximum number of items per sitemap: %s" % items)
            catalog = getToolByName(self.context, "portal_catalog")
            utils = getToolByName(self.context, "plone_utils")
            query = {}
            is_plone_site_root = IPloneSiteRoot.providedBy(self.context)
            if not is_plone_site_root:
                query["path"] = "/".join(self.context.getPhysicalPath())

            query["portal_type"] = list()
            for pt in utils.getUserFriendlyTypes():
                if pt not in self.settings.ignored_types:
                    query["portal_type"].append(pt)

            catalogued_items = catalog(query, Language='all')
            num_cat_items = len(catalogued_items)

            if self.settings.ignored_paths:
                for ignore_path in self.settings.ignored_paths:
                    if ignore_path.endswith(":-1"):
                        query["path"] = "%s%s" % (
                            "/".join(self.context.getPhysicalPath()),
                            ignore_path[:-3],
                        )
                        catalogued_items = catalog(query, Language='all')
                        num_cat_items -= len(catalogued_items)

                    else:
                        query["path"] = {
                            "query": "%s%s"
                            % ("/".join(self.context.getPhysicalPath()), ignore_path),
                            "depth": 0,
                        }
                        catalogued_items = catalog(query, Language='all')
                        num_cat_items -= len(catalogued_items)

            logger.info("Number of items to include in sitemap: %s" % num_cat_items)
            if num_cat_items > items:
                self.num_sitemaps = int(math.ceil(float(num_cat_items) / float(items)))
                logger.info("Will create %s sitemaps" % self.num_sitemaps)

                # First, remove all possible sitemapN.xml.gz that might exist
                for id in self.context:
                    with api.env.adopt_roles(['Manager']):
                        if id.startswith("sitemap") and id.endswith(".xml.gz"):
                            logger.info("Deleting %s" % id)
                            self.context.manage_delObjects(id)

                for num in range(self.num_sitemaps):
                    sitemap_n = num + 1
                    xml = self.template(sitemap_n=sitemap_n, total_items=items)
                    fp = BytesIO()
                    fname = self.split_filename % sitemap_n
                    gzip = GzipFile(fname, "wb", 9, fp)
                    if isinstance(xml, six.text_type):
                        xml = xml.encode("utf8")
                    gzip.write(xml)
                    gzip.close()
                    with api.env.adopt_roles(['Manager']):
                        self.context.manage_addFile(
                            fname, file=fp, content_type="application/octet-stream"
                        )
                        logger.info("Created %s" % fname)

                logger.info("Creating index %s" % self.filename)
                xml = self.index_template()
            else:
                logger.info("Not enough items in site, not splitting sitemap")
                xml = self.template()

        else:
            logger.info("No limit in the number of items to add to sitemap.")
            xml = self.template()

        fp = BytesIO()
        gzip = GzipFile(self.filename, "wb", 9, fp)
        if isinstance(xml, six.text_type):
            xml = xml.encode("utf8")
        gzip.write(xml)
        gzip.close()
        results = fp.getvalue()
        fp.close()

        logger.info("Done creating sitemap.xml.gz")
        return results

    @ram.cache(_render_cachekey)
    def generate(self, items=None):
        """Generates the Gzipped sitemap."""
        data = self._generate(items)
        return data

    def __call__(self, from_script=False):
        """Checks if the sitemap feature is enable and returns it."""
        registry = getUtility(IRegistry)
        if HAVE_P5:
            settings = registry.forInterface(ISiteSchema, prefix="plone")
            if not settings.enable_sitemap:
                raise NotFound(self.context, self.filename, self.request)
        else:
            sp = getToolByName(self.context, "portal_properties").site_properties
            if not sp.enable_sitemap:
                raise NotFound(self.context, self.filename, self.request)

        results = ""
        items = None
        if self.settings.enable_split_sitemaps:
            items = self.settings.items_per_sitemap

        if self.settings.async_sitemap_generation:
            if from_script:
                logger.info(
                    "View called from script. Generating sitemap and saving "
                    "results"
                )
                data = self._generate(items)
                ann = IAnnotations(self.context)
                sitemap_data = ann.setdefault(ANN_KEY, PersistentMapping())
                sitemap_data["data"] = data
                sitemap_data["generated"] = DateTime().ISO8601()
                return

            else:
                ann = IAnnotations(self.context)
                sitemap_data = ann.get(ANN_KEY, {})
                results = sitemap_data.get("data", "")

        else:
            results = self.generate(items)

        self.request.response.setHeader("Content-Type", "application/octet-stream")

        return results

    def extra_search_parameters(self):
        """Allows extra filtering of the sitemap
        for use (in particular) by LinguaPlone

        :returns: a dictionary of keyword parameters to pass into
        catalog.searchResults()
        """
        return {}
