# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_bando import (
    TestBandoSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING


class TestBandoSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
