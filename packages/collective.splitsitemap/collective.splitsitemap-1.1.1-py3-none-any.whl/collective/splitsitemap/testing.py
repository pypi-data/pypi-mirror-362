# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.splitsitemap


class CollectiveSplitsitemapLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.splitsitemap)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.splitsitemap:default')


COLLECTIVE_SPLITSITEMAP_FIXTURE = CollectiveSplitsitemapLayer()


COLLECTIVE_SPLITSITEMAP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SPLITSITEMAP_FIXTURE,),
    name='CollectiveSplitsitemapLayer:IntegrationTesting',
)


COLLECTIVE_SPLITSITEMAP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SPLITSITEMAP_FIXTURE,),
    name='CollectiveSplitsitemapLayer:FunctionalTesting',
)


COLLECTIVE_SPLITSITEMAP_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SPLITSITEMAP_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveSplitsitemapLayer:AcceptanceTesting',
)
