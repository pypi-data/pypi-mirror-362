# -*- coding: utf-8 -*-
from design.plone.ctgeneric.behaviors.persona import IPersonaV2
from plone.indexer.decorator import indexer


@indexer(IPersonaV2)
def ruolo(obj):
    """ """
    return getattr(obj.aq_base, "ruolo", "")
