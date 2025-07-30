# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_documento import (
    TestDocumentoSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api


class TestDocumentoSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_documento(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Documento"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.dublincore",
                "plone.relateditems",
                "plone.locking",
                "plone.constraintypes",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.descrizione_estesa_documento",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "design.plone.contenttypes.behavior.documento_v2",
                "design.plone.contenttypes.behavior.argomenti_documento_v2",
            ),
        )

    def test_documento_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "identificativo",
                "tipologia_documento",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tassonomia_argomenti",
            ],
        )

    def test_documento_fields_descrizione_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "ufficio_responsabile",
                "area_responsabile",
                "autori",
                "licenza_distribuzione",
                "descrizione_estesa",
            ],
        )

    def test_documento_required_fields(self):
        resp = self.api_session.get("@types/Documento").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["tipologia_documento", "title", "ufficio_responsabile"]),
        )
