# -*- coding: utf-8 -*-
from design.plone.ctgeneric import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IDocumentoV2(model.Schema):
    ufficio_responsabile = RelationList(
        title=_(
            "ufficio_responsabile_documento_label",
            default="Ufficio responsabile del documento",
        ),
        description=_(
            "ufficio_responsabile_documento_help",
            default="Seleziona l'ufficio responsabile di questo documento.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Ufficio responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    tipologia_documento = schema.Choice(
        title=_("tipologia_documento_label", default="Tipologia del documento"),
        description=_(
            "tipologia_documento_help",
            default="Seleziona la tipologia del documento.",
        ),
        required=True,
        vocabulary="design.plone.vocabularies.tipologie_documento",
    )

    # custom widgets
    form.widget(
        "ufficio_responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # custom order
    form.order_after(tipologia_documento="identificativo")
    form.order_before(ufficio_responsabile="licenza_distribuzione")

    #  custom fieldsets
    model.fieldset(
        "descrizione",
        label=_("descrizione_label", default="Descrizione"),
        fields=[
            "ufficio_responsabile",
        ],
    )


@implementer(IDocumentoV2)
@adapter(IDexterityContent)
class DocumentoV2(object):
    """ """

    def __init__(self, context):
        self.context = context
