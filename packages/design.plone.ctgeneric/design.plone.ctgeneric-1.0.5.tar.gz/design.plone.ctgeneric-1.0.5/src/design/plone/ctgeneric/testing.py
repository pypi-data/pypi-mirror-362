# -*- coding: utf-8 -*-
from design.plone.contenttypes.testing import DesignPloneContenttypesLayer
from design.plone.contenttypes.testing import DesignPloneContenttypesRestApiLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.testing import z2

import design.plone.ctgeneric
import plone.supermodel


class DesignPloneCtgenericLayer(DesignPloneContenttypesLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=design.plone.ctgeneric)
        self.loadZCML(package=plone.supermodel)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "design.plone.ctgeneric:default")


class DesignPloneCtgenericRestApiLayer(DesignPloneContenttypesRestApiLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=design.plone.ctgeneric)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "design.plone.contenttypes:default")
        applyProfile(portal, "design.plone.ctgeneric:default")


DESIGN_PLONE_CTGENERIC_FIXTURE = DesignPloneCtgenericLayer()
DESIGN_PLONE_CTGENERIC_API_FIXTURE = DesignPloneCtgenericRestApiLayer()

DESIGN_PLONE_CTGENERIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DESIGN_PLONE_CTGENERIC_FIXTURE,),
    name="DesignPloneCtgenericLayer:IntegrationTesting",
)

DESIGN_PLONE_CTGENERIC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CTGENERIC_FIXTURE,),
    name="DesignPloneCtgenericLayer:FunctionalTesting",
)

DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DESIGN_PLONE_CTGENERIC_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneCtgenericRestApiLayer:Functional",
)
