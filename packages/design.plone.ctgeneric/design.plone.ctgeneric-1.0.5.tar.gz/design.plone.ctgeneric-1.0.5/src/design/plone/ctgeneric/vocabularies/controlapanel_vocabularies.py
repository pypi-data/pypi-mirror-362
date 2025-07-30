# -*- coding: utf-8 -*-
from design.plone.ctgeneric.utils import get_settings_for_language
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger(__name__)


class BaseVocabulary(object):
    def __call__(self, context):
        values = get_settings_for_language(field=self.field)
        if not values:
            return SimpleVocabulary([])

        terms = [SimpleTerm(value=x, token=x, title=x) for x in values]
        terms.insert(
            0,
            SimpleTerm(value="", token="", title="-- seleziona un valore --"),
        )

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class RuoliPersona(BaseVocabulary):
    field = "ruoli_persona"


@implementer(IVocabularyFactory)
class TipologieNotizia(BaseVocabulary):
    """
    V2 Vocabulary
    """

    field = "tipologie_notizia"


@implementer(IVocabularyFactory)
class TipologieUnitaOrganizzativaVocabulary(BaseVocabulary):
    """
    V2 Vocabulary
    """

    field = "tipologie_unita_organizzativa"


@implementer(IVocabularyFactory)
class TipologieDocumento(BaseVocabulary):
    """
    V2 Vocabulary
    """

    field = "tipologie_documento"


@implementer(IVocabularyFactory)
class TipologiePersona(BaseVocabulary):
    """
    V2 Vocabulary
    """

    field = "tipologie_persona"


RuoliPersonaFactory = RuoliPersona()
TipologieNotiziaFactory = TipologieNotizia()
TipologieDocumentoFactory = TipologieDocumento()
TipologiePersonaFactory = TipologiePersona()
TipologieUnitaOrganizzativaVocabularyFactory = TipologieUnitaOrganizzativaVocabulary()
