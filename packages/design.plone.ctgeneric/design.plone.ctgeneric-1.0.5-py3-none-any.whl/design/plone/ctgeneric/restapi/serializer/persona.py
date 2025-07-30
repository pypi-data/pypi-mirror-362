from design.plone.contenttypes.interfaces.persona import IPersona
from design.plone.contenttypes.restapi.serializers.persona import (
    PersonaSerializer as BaseSerializer,
)
from design.plone.ctgeneric.interfaces import IDesignPloneCtgenericLayer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import implementer


@implementer(ISerializeToJson)
@adapter(IPersona, IDesignPloneCtgenericLayer)
class PersonaSerializer(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super().__call__(version=version, include_items=include_items)

        result["incarichi_persona"] = self.get_incarichi_v2()
        # temporary disabled
        result["contact_info"] = self.get_contacts_v2()
        return result

    def get_incarichi_v2(self):
        """
        Add infos about incarichi to emulate v3 schema
        """
        return [
            {
                "compensi": None,
                "compensi_file": [],
                "data_conclusione_incarico": json_compatible(
                    getattr(self.context, "data_conclusione_incarico", "")
                ),
                "data_inizio_incarico": "",
                "data_insediamento": json_compatible(
                    getattr(self.context, "data_insediamento", "")
                ),
                "tipologia_incarico": {
                    "title": getattr(self.context, "tipologia_persona", ""),
                    "token": getattr(self.context, "tipologia_persona", ""),
                },
                "title": getattr(self.context, "ruolo", ""),
                "type_title": "Incarico",
            }
        ]

    def get_contacts_v2(self):
        pdc = []
        for field in ["telefono", "fax", "email"]:
            value = getattr(self.context, field, "")
            if value:
                pdc.append({"pdc_type": field, "pdc_value": value})

        return [
            [
                {
                    "value_punto_contatto": pdc,
                }
            ]
        ]
