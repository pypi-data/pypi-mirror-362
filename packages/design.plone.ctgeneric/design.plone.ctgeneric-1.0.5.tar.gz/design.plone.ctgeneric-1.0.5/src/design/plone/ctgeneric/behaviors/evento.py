# -*- coding: utf-8 -*-
from design.plone.ctgeneric import _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IEventoV2(model.Schema):
    """
    Campi custom solo per la v2
    """

    telefono = schema.TextLine(
        title=_("telefono_event_help", default="Telefono"),
        description=_(
            "telefono_event_label",
            default="Indicare un riferimento telefonico per poter contattare"
            " gli organizzatori.",
        ),
        required=False,
    )
    fax = schema.TextLine(
        title=_("fax_event_help", default="Fax"),
        description=_("fax_event_label", default="Indicare un numero di fax."),
        required=False,
    )
    reperibilita = schema.TextLine(
        title=_("reperibilita", default="Reperibilità organizzatore"),
        required=False,
        description=_(
            "reperibilita_help",
            default="Indicare gli orari in cui l'organizzatore è"
            " telefonicamente reperibile.",
        ),
    )
    email = schema.TextLine(
        title=_("email_event_label", default="E-mail"),
        description=_(
            "email_event_help",
            default="Indicare un indirizzo mail per poter contattare"
            " gli organizzatori.",
        ),
        required=False,
    )

    web = schema.TextLine(
        title=_("web_event_label", default="Sito web"),
        description=_(
            "web_event_help",
            default="Indicare un indirizzo web di riferimento a " "questo evento.",
        ),
        required=False,
    )

    # custom tabs
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "telefono",
            "fax",
            "reperibilita",
            "email",
            "web",
        ],
    )

    form.order_after(telefono="organizzato_da_esterno")
    form.order_after(fax="telefono")
    form.order_after(reperibilita="fax")
    form.order_after(email="reperibilita")
    form.order_after(web="email")


@implementer(IEventoV2)
@adapter(IDexterityContent)
class EventoV2(object):
    """ """

    def __init__(self, context):
        self.context = context
