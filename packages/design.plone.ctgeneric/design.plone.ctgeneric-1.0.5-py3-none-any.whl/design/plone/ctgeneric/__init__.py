# -*- coding: utf-8 -*-
"""Init and utils."""
from design.plone.contenttypes.events import common
from design.plone.contenttypes.vocabularies import tags_vocabulary
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("design.plone.ctgeneric")


subfolders_mapping = common.SUBFOLDERS_MAPPING
persona_folders = [
    x
    for x in subfolders_mapping["Persona"].get("content", [])
    if x["allowed_types"] != ("Incarico",)
]
persona_folders.extend(
    [
        {"id": "compensi", "title": "Compensi", "contains": ("File",)},
        {
            "id": "importi-di-viaggio-e-o-servizi",
            "title": "Importi di viaggio e/o servizi",
            "contains": ("File",),
        },
    ]
)

subfolders_mapping["Persona"] = {"allowed_types": [], "content": persona_folders}

common.SUBFOLDERS_MAPPING = subfolders_mapping


tags_vocabulary.TAGS_MAPPING = [
    ("anziano", _("Anziano")),
    ("fanciullo", _("Fanciullo")),
    ("giovane", _("Giovane")),
    ("famiglia", _("Famiglia")),
    ("studente", _("Studente")),
    ("associazione", _("Associazione")),
    ("istruzione", _("Istruzione")),
    ("abitazione", _("Abitazione")),
    ("animale-domestico", _("Animale domestico")),
    ("integrazione-sociale", _("Integrazione sociale")),
    ("protezione-sociale", _("Protezione sociale")),
    ("comunicazione", _("Comunicazione")),
    ("urbanistica-edilizia", _("Urbanistica ed edilizia")),
    ("formazione-professionale", _("Formazione professionale")),
    (
        "condizioni-organizzazione-lavoro",
        _("Condizioni e organizzazione del lavoro"),
    ),
    ("trasporto", _("Trasporto")),
    ("matrimonio", _("Matrimonio")),
    ("elezione", _("Elezione")),
    ("tempo-libero", _("Tempo libero")),
    ("cultura", _("Cultura")),
    ("immigrazione", _("Immigrazione")),
    ("inquinamento", _("Inquinamento")),
    ("area-parcheggio", _("Area di parcheggio")),
    ("traffico-urbano", _("Traffico urbano")),
    ("acqua", _("Acqua")),
    ("gestione-rifiuti", _("Gestione dei rifiuti")),
    ("salute", _("Salute")),
    ("sicurezza-pubblica", _("Sicurezza pubblica")),
    ("sicurezza-internazionale", _("Sicurezza internazionale")),
    ("spazio-verde", _("Spazio verde")),
    ("sport", _("Sport")),
    ("trasporto-stradale", _("Trasporto stradale")),
    ("turismo", _("Turismo")),
    ("energia", _("Energia")),
    (
        "informatica-trattamento-dati",
        _("Informatica e trattamento dei dati"),
    ),
]
