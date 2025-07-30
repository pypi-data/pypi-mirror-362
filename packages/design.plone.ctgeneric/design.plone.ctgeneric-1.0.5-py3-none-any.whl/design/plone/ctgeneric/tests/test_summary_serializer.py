# -*- coding: utf-8 -*-
from design.plone.ctgeneric.testing import DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.testing import RelativeSession
from transaction import commit
from zope.component import getMultiAdapter

import unittest


class SummarySerializerTest(unittest.TestCase):
    layer = DESIGN_PLONE_CTGENERIC_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.document = api.content.create(
            container=self.portal, type="Document", title="Document"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def test_summary_return_persona_role(self):
        api.content.create(
            container=self.portal, type="Persona", title="John Doe", ruolo="unknown"
        )
        api.content.create(container=self.portal, type="Persona", title="Mario Rossi")

        commit()

        brains = api.content.find(portal_type="Persona", id="mario-rossi")
        results = getMultiAdapter((brains, self.request), ISerializeToJson)(
            fullobjects=False
        )

        self.assertEqual(results["items"][0]["ruolo"], None)
        self.assertEqual(results["items"][0]["title"], "Mario Rossi")

        brains = api.content.find(portal_type="Persona", id="john-doe")
        results = getMultiAdapter((brains, self.request), ISerializeToJson)(
            fullobjects=False
        )

        self.assertEqual(results["items"][0]["ruolo"], "unknown")
        self.assertEqual(results["items"][0]["title"], "John Doe")

        # test also with restapi call
        response = self.api_session.get(
            "{}/@search?portal_type=Persona&id=mario-rossi".format(self.portal_url)
        )

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(items[0]["title"], "Mario Rossi")
        self.assertEqual(items[0]["ruolo"], None)

        response = self.api_session.get(
            "{}/@search?portal_type=Persona&id=john-doe".format(self.portal_url)
        )

        result = response.json()
        items = result.get("items", [])

        self.assertEqual(items[0]["title"], "John Doe")
        self.assertEqual(items[0]["ruolo"], "unknown")
