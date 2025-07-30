# -*- coding: utf-8 -*-
from design.plone.ctgeneric import _
from plone.restapi.controlpanels.interfaces import IControlpanel
from zope.interface import Interface
from zope.schema import SourceText

import json


class IDesignPloneV2SettingsControlpanel(IControlpanel):
    """ """


class IDesignPloneV2Settings(Interface):
    tipologie_notizia = SourceText(
        title=_("tipologie_notizia_label", default="Tipologie Notizia"),
        description=_(
            "tipologie_notizia_help",
            default="Inserisci i valori utilizzabili per le tipologie di una"
            " Notizia. Se il sito è multilingua, puoi inserire valori diversi"
            " a seconda delle lingue del sito.",
        ),
        required=True,
        default=json.dumps({"it": ["Avviso", "Comunicato (stampa)", "Notizia"]}),
    )
    tipologie_documento = SourceText(
        title=_("tipologie_documento_label", default="Tipologie Documento"),
        description=_(
            "tipologie_documento_help",
            default="Inserisci i valori utilizzabili per le tipologie di un "
            "Documento. Se il sito è multilingua, puoi inserire "
            "valori diversi a seconda delle lingue del sito.",
        ),
        required=True,
        default=json.dumps(
            {
                "it": [
                    "Accordi tra enti",
                    "Atti normativi",
                    "Dataset",
                    "Documenti (tecnici) di supporto",
                    "Documenti albo pretorio",
                    "Documenti attività politica",
                    "Documenti funzionamento interno",
                    "Istanze",
                    "Modulistica",
                ]
            }
        ),
    )
    tipologie_unita_organizzativa = SourceText(
        title=_(
            "tipologie_unita_organizzativa_label",
            default="Tipologie Unità Organizzativa",
        ),
        description=_(
            "tipologie_unita_organizzativa_help",
            default="Inserisci i valori utilizzabili per le tipologie di un' "
            "Unità Organizzativa. Se il sito è multilingua, puoi inserire "
            "valori diversi a seconda delle lingue del sito.",
        ),
        required=True,
        default=json.dumps({"it": ["Politica", "Amministrativa", "Altro"]}),
    )
    tipologie_persona = SourceText(
        title=_("tipologie_persona_label", default="Tipologie Persona"),
        description=_(
            "tipologie_persona_help",
            default="Inserisci i valori utilizzabili per le tipologie di "
            "una Persona. Se il sito è multilingua, puoi inserire "
            "valori diversi a seconda delle lingue del sito.",
        ),
        required=True,
        default=json.dumps({"it": ["Amministrativa", "Politica", "Altro tipo"]}),
    )

    ruoli_persona = SourceText(
        title=_("ruoli_persona_label", default="Ruoli Persona"),
        description=_(
            "ruoli_persona_help",
            default="Inserisci i valori utilizzabili per il ruolo di "
            "una Persona. Se il sito è multilingua, puoi inserire "
            "valori diversi a seconda delle lingue del sito.",
        ),
        required=True,
        default=json.dumps(
            {
                "it": [
                    "Assessore",
                    "Sindaco",
                    "Consigliere",
                    "Referente ufficio",
                    "Responsabile",
                    "Presidente",
                ]
            }
        ),
    )
