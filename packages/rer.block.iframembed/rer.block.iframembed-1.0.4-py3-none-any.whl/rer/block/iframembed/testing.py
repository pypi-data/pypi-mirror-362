# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import rer.block.iframembed


class RerBlockIframembedLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=rer.block.iframembed)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rer.block.iframembed:default')


RER_BLOCK_IFRAMEMBED_FIXTURE = RerBlockIframembedLayer()


RER_BLOCK_IFRAMEMBED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RER_BLOCK_IFRAMEMBED_FIXTURE,),
    name='RerBlockIframembedLayer:IntegrationTesting',
)


RER_BLOCK_IFRAMEMBED_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RER_BLOCK_IFRAMEMBED_FIXTURE,),
    name='RerBlockIframembedLayer:FunctionalTesting',
)


RER_BLOCK_IFRAMEMBED_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RER_BLOCK_IFRAMEMBED_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RerBlockIframembedLayer:AcceptanceTesting',
)
