# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_event import (
    TestEventSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api


class TestEventSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_event(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Event"].behaviors,
            (
                "plone.eventbasic",
                "plone.leadimage",
                "volto.preview_image",
                "plone.eventrecurrence",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "design.plone.contenttypes.behavior.luoghi_correlati_evento",
                "design.plone.contenttypes.behavior.address_event",
                "design.plone.contenttypes.behavior.geolocation_event",
                "design.plone.contenttypes.behavior.strutture_correlate",
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.relateditems",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.evento_v2",
            ),
        )

    def test_event_required_fields(self):
        """
        Override v3
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "start", "end"]),
        )

    def test_event_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(len(resp["fieldsets"]), 13)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cose",
                "luogo",
                "date_e_orari",
                "costi",
                "contatti",
                "informazioni",
                "correlati",
                "categorization",
                "dates",
                "settings",
                "ownership",
                "seo",
            ],
        )

    def test_event_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "start",
                "end",
                "whole_day",
                "open_end",
                "sync_uid",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "recurrence",
                "tassonomia_argomenti",
                "sottotitolo",
            ],
            # should be like this, but in tests SchemaTweaks does not work
            # [
            #     "title",
            #     "description",
            #     "image",
            #     "image_caption",
            #     "preview_image",
            #     "preview_caption",
            #     "tassonomia_argomenti",
            #     "sottotitolo",
            # ],
        )

    def test_event_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "organizzato_da_interno",
                "organizzato_da_esterno",
                "supportato_da",
                "patrocinato_da",
                "telefono",
                "fax",
                "reperibilita",
                "email",
                "web",
            ],
        )

    def test_event_fields_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["ulteriori_informazioni", "strutture_politiche", "patrocinato_da"],
        )

    def test_event_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
            ["correlato_in_evidenza"],
            # should be like this but SchemaTweaks does not work in tests
            # ["correlato_in_evidenza", "relatedItems"],
        )

    def test_event_fields_categorization_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["subjects", "language", "relatedItems"],
            # should be like this with SchemaTweaks
            # ["subjects", "language"],
        )

    def test_event_fields_dates_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][9]["fields"], ["effective", "expires"])

    def test_event_fields_settings_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][10]["fields"],
            [
                "allow_discussion",
                "exclude_from_nav",
                "id",
                "versioning_enabled",
                "changeNote",
            ],
        )

    def test_event_fields_ownership_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][11]["fields"], ["creators", "contributors", "rights"]
        )

    def test_event_fields_seo_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][12]["fields"],
            [
                "seo_title",
                "seo_description",
                "seo_noindex",
                "seo_canonical_url",
                "opengraph_title",
                "opengraph_description",
                "opengraph_image",
            ],
        )
