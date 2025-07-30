# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_luogo import (
    TestLuogoApi as BaseTestLuogoApi,
)
from design.plone.contenttypes.tests.test_ct_luogo import (
    TestLuogoSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api
from transaction import commit
from uuid import uuid4


class TestLuogoSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_luogo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Venue"].behaviors,
            (
                "plone.app.content.interfaces.INameFromTitle",
                "plone.app.dexterity.behaviors.id.IShortName",
                "plone.app.dexterity.behaviors.metadata.IBasic",
                "plone.app.dexterity.behaviors.metadata.ICategorization",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "volto.preview_image",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.address_venue",
                "design.plone.contenttypes.behavior.geolocation_venue",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "design.plone.contenttypes.behavior.contatti_venue_v2",
                "design.plone.contenttypes.behavior.luogo_v2",
            ),
        )

    def test_luogo_required_fields(self):
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                ]
            ),
        )

    def test_luogo_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tassonomia_argomenti",
                "nome_alternativo",
            ],
        )

    def test_luogo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "telefono",
                "fax",
                "email",
                "pec",
                "web",
                "struttura_responsabile_correlati",
                "struttura_responsabile",
                "riferimento_telefonico_struttura",
                "riferimento_fax_struttura",
                "riferimento_mail_struttura",
                "riferimento_pec_struttura",
            ],
        )

    def test_luogo_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Venue").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            # ["subjects", "language"] BBB dovrebbe essere così
            # ma nei test esce così perché non viene vista la patch di SchemaTweaks
            ["subjects", "language", "relatedItems"],
        )


class TestLuogoApi(BaseTestLuogoApi):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_venue_geolocation_deserializer_right_structure(self):
        venue = api.content.create(
            container=self.portal, type="Venue", title="Example venue"
        )

        commit()
        self.assertEqual(venue.geolocation, None)

        text_uuid = str(uuid4())
        response = self.api_session.patch(
            venue.absolute_url(),
            json={
                "@type": "Venue",
                "title": "Foo",
                "geolocation": {"latitude": 11.0, "longitude": 10.0},
                "modalita_accesso": {
                    "blocks": {
                        text_uuid: {
                            "@type": "text",
                            "text": {"blocks": [{"text": "Test", "type": "paragraph"}]},
                        }
                    },
                    "blocks_layout": {"items": [text_uuid]},
                },
            },
        )
        self.assertEqual(response.status_code, 204)
