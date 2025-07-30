# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.persona import IPersona
from design.plone.contenttypes.restapi.serializers.summary import (
    DefaultJSONSummarySerializer as BaseSerializer,
)
from design.plone.contenttypes.restapi.serializers.summary import (
    PersonaDefaultJSONSummarySerializer as BasePersonaSerializer,
)
from design.plone.ctgeneric.interfaces import IDesignPloneCtgenericLayer
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IDesignPloneCtgenericLayer)
class DefaultJSONSummarySerializer(BaseSerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        if self.context.portal_type == "Persona":
            res["ruolo"] = getattr(self.context, "ruolo", "")
            res["incarichi"] = getattr(self.context, "ruolo", "")
        return res


@implementer(ISerializeToJsonSummary)
@adapter(IPersona, IDesignPloneCtgenericLayer)
class PersonaDefaultJSONSummarySerializer(BasePersonaSerializer):
    def __call__(self, **kwargs):
        res = super().__call__(**kwargs)
        res["ruolo"] = getattr(self.context, "ruolo", "")
        res["incarichi"] = getattr(self.context, "ruolo", "")
        return res
