# -*- coding: utf-8 -*-
from design.plone.ctgeneric import _
from plone.app.contenttypes.interfaces import INewsItem
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class INewsV2(model.Schema):
    tipologia_notizia = schema.Choice(
        title=_("tipologia_notizia_label", default="Tipologia notizia"),
        description=_(
            "tipologia_notizia_help",
            default="Seleziona la tipologia della notizia.",
        ),
        required=True,
        vocabulary="design.plone.vocabularies.tipologie_notizia",
    )

    # custom fieldsets and order
    form.order_after(tipologia_notizia="descrizione_estesa")


@implementer(INewsV2)
@adapter(INewsItem)
class NewsV2(object):
    """ """

    def __init__(self, context):
        self.context = context
