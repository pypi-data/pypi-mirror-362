# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes.interfaces.servizio import IServizio
from design.plone.ctgeneric import _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IServizioV2(model.Schema):
    autenticazione = BlocksField(
        title=_("autenticazione", default="Autenticazione"),
        description=_(
            "autenticazione_help",
            default="Indicare, se previste, le modalità di autenticazione"
            " necessarie per poter accedere al servizio.",
        ),
        required=False,
    )

    model.fieldset("accedi_al_servizio", fields=["autenticazione"])

    form.order_after(autenticazione="canale_digitale")


@implementer(IServizioV2)
@adapter(IServizio)
class ServizioV2(object):
    """"""

    def __init__(self, context):
        self.context = context
