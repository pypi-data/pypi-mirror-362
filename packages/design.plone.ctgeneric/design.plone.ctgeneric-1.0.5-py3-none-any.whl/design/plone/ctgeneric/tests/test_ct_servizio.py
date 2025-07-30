# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_servizio import (
    TestServizioSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api


class TestServizioSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_servizio(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Servizio"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "design.plone.contenttypes.behavior.descrizione_estesa_servizio",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "design.plone.contenttypes.behavior.additional_help_infos",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "plone.locking",
                "design.plone.contenttypes.behavior.argomenti",
                "design.plone.contenttypes.behavior.servizio_v2",
            ),
        )

    def test_servizio_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(len(resp["fieldsets"]), 18)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cose",
                "a_chi_si_rivolge",
                "accedi_al_servizio",
                "cosa_serve",
                "costi_e_vincoli",
                "tempi_e_scadenze",
                "casi_particolari",
                "contatti",
                "documenti",
                "link_utili",
                "informazioni",
                "correlati",
                "categorization",
                "settings",
                "ownership",
                "dates",
                "seo",
            ],
        )

    def test_servizio_required_fields(self):
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(["title", "cosa_serve", "ufficio_responsabile"]),
        )

    def test_servizio_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "sottotitolo",
                "stato_servizio",
                "motivo_stato_servizio",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tassonomia_argomenti",
            ],
        )

    def test_servizio_fields_a_chi_si_rivolge_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["a_chi_si_rivolge", "chi_puo_presentare", "copertura_geografica"],
        )

    def test_servizio_fields_accedi_al_servizio_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "come_si_fa",
                "cosa_si_ottiene",
                "procedure_collegate",
                "canale_digitale",
                "autenticazione",
                "dove_rivolgersi",
                "dove_rivolgersi_extra",
                "prenota_appuntamento",
            ],
        )

    def test_servizio_fields_tempi_e_scadenze_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][6]["fields"],
            ["tempi_e_scadenze"],
        )

    def test_servizio_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["ufficio_responsabile", "area"],
        )

    def test_servizio_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][12]["fields"],
            ["servizi_collegati", "correlato_in_evidenza"],
        )
