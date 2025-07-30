# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_unita_organizzativa import (
    TestUO as BaseTest,
)
from design.plone.contenttypes.tests.test_ct_unita_organizzativa import (
    TestUOSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api
from transaction import commit


class TestUOSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_uo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["UnitaOrganizzativa"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "plone.locking",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.argomenti",
                "plone.textindexer",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "design.plone.contenttypes.behavior.unita_organizzativa_v2",
                "design.plone.contenttypes.behavior.address_uo",
                "design.plone.contenttypes.behavior.geolocation_uo",
                "design.plone.contenttypes.behavior.contatti_uo_v2",
            ),
        )

    def test_uo_required_fields(self):
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "tipologia_organizzazione"]),
        )

    def test_uo_fields_struttura_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            [
                "legami_con_altre_strutture",
                "responsabile",
                "tipologia_organizzazione",
                "assessore_riferimento",
            ],
        )

    def test_uo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            [
                "sede",
                "sedi_secondarie",
                "contact_info",
                "nome_sede",
                "street",
                "zip_code",
                "city",
                "quartiere",
                "circoscrizione",
                "country",
                "geolocation",
                "telefono",
                "fax",
                "email",
                "pec",
                "web",
                "orario_pubblico",
            ],
        )

    def test_uo_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            # ["subjects", "language"] BBB dovrebbe essere così
            # ma nei test esce così perché non viene vista la patch di SchemaTweaks
            ["subjects", "language", "relatedItems"],
        )


class TestUO(BaseTest):
    """"""

    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_cant_patch_uo_that_has_no_required_fields(self):
        """
        in V3 you get a 400, but here you can
        """
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="Foo"
        )
        commit()
        resp = self.api_session.patch(
            uo.absolute_url(),
            json={
                "title": "Foo modified",
            },
        )
        self.assertEqual(resp.status_code, 204)
