# -*- coding: utf-8 -*-
from design.plone.contenttypes.tests.test_ct_news import (
    TestNewsSchema as BaseSchemaTest,
)
from design.plone.ctgeneric.interfaces import IDesignPloneV2Settings
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import json
import transaction
import unittest


class TestNewsSchema(BaseSchemaTest):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def test_behaviors_enabled_for_news(self):
        portal_types = api.portal.get_tool(name="portal_types")

        self.assertEqual(
            portal_types["News Item"].behaviors,
            (
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "plone.versioning",
                "plone.locking",
                "volto.preview_image",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "design.plone.contenttypes.behavior.news_v2",
                "design.plone.contenttypes.behavior.argomenti",
            ),
        )

    def test_news_item_required_fields(self):
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "tipologia_notizia",
                ]
            ),
        )

    def test_news_item_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "descrizione_estesa",
                "tipologia_notizia",
                "numero_progressivo_cs",
                "a_cura_di",
                "a_cura_di_persone",
                "luoghi_correlati",
                "notizie_correlate",
                "tassonomia_argomenti",
            ],
        )

    def test_news_item_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News%20Item").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["correlato_in_evidenza"],
        )


class TestNewsApi(unittest.TestCase):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )

        # we need it because of vocabularies
        api.portal.set_registry_record(
            "tipologie_notizia",
            json.dumps({"en": ["foo", "bar"]}),
            interface=IDesignPloneV2Settings,
        )
        transaction.commit()

    def tearDown(self):
        self.api_session.close()
        super().setUp()

    def test_newsitem_required_fields(self):
        response = self.api_session.post(
            self.portal_url,
            json={"@type": "News Item", "title": "Foo"},
        )
        self.assertEqual(response.status_code, 400)

        response = self.api_session.post(
            self.portal_url,
            json={"@type": "News Item", "title": "Foo", "tipologia_notizia": "foo"},
        )
        self.assertEqual(response.status_code, 201)

    def test_newsitem_substructure_created(self):
        self.api_session.post(
            self.portal_url,
            json={
                "@type": "News Item",
                "title": "Foo",
                "tipologia_notizia": "foo",
                "a_cura_di": self.document.UID(),
            },
        )

        transaction.commit()
        news = self.portal["foo"]

        self.assertEqual(["multimedia", "documenti-allegati"], news.keys())

        self.assertEqual(news["multimedia"].portal_type, "Document")
        self.assertEqual(news["multimedia"].constrain_types_mode, 1)
        self.assertEqual(news["multimedia"].locally_allowed_types, ("Link", "Image"))

        self.assertEqual(news["documenti-allegati"].portal_type, "Document")
        self.assertEqual(news["documenti-allegati"].constrain_types_mode, 1)
        self.assertEqual(
            news["documenti-allegati"].locally_allowed_types, ("File", "Image")
        )
