# -*- coding: utf-8 -*-
from collective.geolocationbehavior.geolocation import IGeolocatable
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from design.plone.ctgeneric import _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IUnitaOrganizzativaV2(model.Schema, IGeolocatable):
    contact_info = BlocksField(
        title=_("contact_info_label", default="Informazioni di contatto generiche"),
        required=False,
        description=_(
            "uo_contact_info_description",
            default="Inserisci eventuali informazioni di contatto aggiuntive "
            "non contemplate nei campi precedenti. "
            "Utilizza questo campo se ci sono dei contatti aggiuntivi rispetto"
            " ai contatti della sede principale. Se inserisci un collegamento "
            'con un indirizzo email, aggiungi "mailto:" prima dell\'indirizzo'
            ", per farlo aprire direttamente nel client di posta.",
        ),
    )
    nome_sede = schema.TextLine(
        title=_("nome_sede", default="Nome sede"),
        description=_(
            "help_nome_sede",
            default="Inserisci il nome della "
            "sede, se non è presente tra i Luoghi del sito.",
        ),
        required=False,
    )

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info", "nome_sede", "geolocation"],
    )

    form.order_after(geolocation="country")


@implementer(IUnitaOrganizzativaV2)
@adapter(IUnitaOrganizzativa)
class UnitaOrganizzativaV2(object):
    """"""

    def __init__(self, context):
        self.context = context
