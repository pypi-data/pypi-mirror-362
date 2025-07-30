# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_cartella_modulistica import (
    TestCartellaModulisticaSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING


class TestCartellaModulisticaSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
