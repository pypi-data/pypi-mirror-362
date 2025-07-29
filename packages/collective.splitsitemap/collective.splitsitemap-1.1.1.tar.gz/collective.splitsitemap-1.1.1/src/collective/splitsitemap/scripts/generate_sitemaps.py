import argparse
import logging
import os
import sys
import transaction

from DateTime import DateTime
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.User import system
from collective.splitsitemap.interfaces import ICollectiveSplitsitemapLayer
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Testing.makerequest import makerequest
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.interface import alsoProvides
from zope.globalrequest import setRequest


def entrypoint(app, args):
    # Logging configuration
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_file", dest="log_file", default=None)
    parser.add_argument("--plone_site", dest="plone_site", default=None)
    parser.add_argument("--nav_root", dest="nav_root", default=None)
    parser.add_argument("--server_url", dest="server_url", default=None)

    args = parser.parse_args(args[2:])

    if args.log_file:
        logger = logging.getLogger("collective.splitsitemap")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(args.log_file)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    app = makerequest(app)
    newSecurityManager(None, system)

    # Set site
    try:
        if args.plone_site:
            plone_site = args.plone_site
        else:
            for id in app:
                obj = app.get(id)
                if IPloneSiteRoot.providedBy(obj):
                    plone_site = id
        site = app.restrictedTraverse(plone_site)
    except Exception:
        raise ValueError(
            "Wrong site; Please specify an existing "
            "site's path using the --base_path argument."
        )

    setSite(site=site)
    site.REQUEST["PARENTS"] = [site]
    site.REQUEST.setVirtualRoot("/")

    server_url = None
    if args.server_url:
        server_url = args.server_url
    else:
        if os.getenv("SERVER_URL"):
            server_url = os.getenv("SERVER_URL")
    if server_url:
        site.REQUEST["SERVER_URL"] = server_url

    alsoProvides(site.REQUEST, ICollectiveSplitsitemapLayer)
    setRequest(site.REQUEST)
    if args.nav_root:
        context = site.restrictedTraverse(args.nav_root)
    else:
        context = site
    sitemap_view = getMultiAdapter((context, context.REQUEST),
                                   name="sitemap.xml.gz")

    sitemap_view(from_script=True)

    # commit transaction
    transaction.commit()
    app._p_jar.sync()
