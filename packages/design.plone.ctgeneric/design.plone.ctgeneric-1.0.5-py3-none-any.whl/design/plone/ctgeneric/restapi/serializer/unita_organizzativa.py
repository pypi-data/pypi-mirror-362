# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from design.plone.contenttypes.restapi.serializers.unita_organizzativa import (
    UOJSONSummarySerializer as BaseSerializer,
)
from design.plone.ctgeneric.interfaces import IDesignPloneCtgenericLayer
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import adapter
from zope.interface import implementer


@implementer(ISerializeToJsonSummary)
@adapter(IUnitaOrganizzativa, IDesignPloneCtgenericLayer)
class UOJSONSummarySerializer(BaseSerializer):
    """
    Override dei fields
    """

    fields = [
        "contact_info",
        "sede",
        "address",
        "city",
        "zip_code",
        "email",
        "telefono",
        "nome_sede",
        "title",
        "quartiere",
        "circoscrizione",
        "street",
    ]
