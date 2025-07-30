# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from design.plone.contenttypes.behaviors.address import IAddressLocal
from design.plone.contenttypes.behaviors.address import IAddressNomeSede
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from design.plone.ctgeneric import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IAddressUnitaOrganizzativa(IAddress, IAddressNomeSede, IAddressLocal):
    """ """

    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "nome_sede",
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
        ],
    )


@implementer(IAddressUnitaOrganizzativa)
@adapter(IUnitaOrganizzativa)
class AddressUnitaOrganizzativa(object):
    """ """

    def __init__(self, context):
        self.context = context
