# -*- coding: utf-8 -*-
from design.plone.contenttypes.restapi.services.types.get import TypesGet as BaseGet
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
    def customize_venue_schema(self, result):
        """
        Tolgo l'obbligatorietà forzata dal v3
        """
        schema = super().customize_venue_schema(result=result)

        fields = ["description", "image", "street", "city", "zip_code", "geolocation"]

        schema["required"] = [x for x in result.get("required", []) if x not in fields]
        return schema

    def customize_servizio_schema(self, result):
        """
        Tolgo l'obbligatorietà forzata dal v3
        """
        schema = super().customize_servizio_schema(result=result)

        fields = ["description"]

        schema["required"] = [x for x in result.get("required", []) if x not in fields]
        return schema

    def customize_evento_schema(self, result):
        """
        Tolgo l'obbligatorietà forzata dal v3
        """
        schema = super().customize_evento_schema(result=result)

        fields = ["description"]

        schema["required"] = [x for x in result.get("required", []) if x not in fields]
        return schema

    def customize_uo_schema(self, result):
        """
        Tolgo l'obbligatorietà forzata dal v3 e invalido la modifica
        """
        schema = result

        fields = ["description"]

        schema["required"] = [x for x in result.get("required", []) if x not in fields]
        return schema

    def customize_news_schema(self, result):
        """
        Tolgo l'obbligatorietà forzata dal v3
        """
        schema = super().customize_news_schema(result=result)

        fields = ["description"]

        schema["required"] = [x for x in result.get("required", []) if x not in fields]
        return schema

    def customize_documento_schema(self, result):
        """
        Tolgo l'obbligatorietà forzata dal v3
        """
        schema = super().customize_documento_schema(result=result)

        fields = ["description"]

        schema["required"] = [x for x in result.get("required", []) if x not in fields]
        return schema
