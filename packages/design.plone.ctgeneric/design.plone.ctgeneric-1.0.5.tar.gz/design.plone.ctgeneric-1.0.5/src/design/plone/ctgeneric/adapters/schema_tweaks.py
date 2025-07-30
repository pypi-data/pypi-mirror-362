from design.plone.contenttypes.interfaces.documento import IDocumento
from design.plone.contenttypes.interfaces.persona import IPersona
from design.plone.contenttypes.interfaces.servizio import IServizio
from design.plone.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.interfaces import OMITTED_KEY
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.interfaces import ISchemaPlugin
from plone.supermodel.model import Fieldset
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import logging


logger = logging.getLogger(__name__)


@implementer(ISchemaPlugin)
@adapter(IFormFieldProvider)
class SchemaTweaks(object):
    """
    Fix fields for content-types to be like v2 of design.plone.contenttypes
    """

    order = 99999

    def __init__(self, schema):
        self.schema = schema

    def __call__(self):
        self.fix_documento_schema()
        self.fix_event_schema()
        self.fix_news_schema()
        self.fix_persona_schema()
        self.fix_servizio_schema()
        self.fix_unita_organizzativa_schema()
        self.fix_luogo_schema()

    def move_field(
        self,
        schema,
        fieldname,
        to_fieldset_name,
        label=None,
        description=None,
        order=None,
    ):
        """
        Copied from https://community.plone.org/t/moving-behavior-fields-to-different-fieldset/6219/7
        Moves a field named "fieldname" on a Zope "schema" to a new fieldset "to_field_name".

        - creates a new fieldset on demand (then label, description and order are passed to the new one).
        - if value of "to_fieldset_name" is "default", then the field sticks on the main form.
        """
        # find schema with field in inheritance tree
        schema_with_field = None
        for pschema in reversed(schema.__iro__):
            if pschema.direct(fieldname):
                schema_with_field = pschema
                break
        if schema_with_field is None:
            raise KeyError(f"field '{fieldname}' does not exist on {schema}.")

        # remove field from fieldset (if in any)
        fieldsets_direct = schema_with_field.queryDirectTaggedValue(FIELDSETS_KEY)
        if fieldsets_direct is not None:
            for fieldset in fieldsets_direct:
                if fieldname in fieldset.fields:
                    fieldset.fields.remove(fieldname)
                    break

        if to_fieldset_name == "default":
            # default means to fieldset, but on main form
            return

        if fieldsets_direct is None:
            # no tagged value set so far!
            fieldsets_direct = list()
            schema.setTaggedValue(FIELDSETS_KEY, fieldsets_direct)

        # try to find the fieldset, append and exit
        for fieldset in fieldsets_direct:
            if fieldset.__name__ == to_fieldset_name:
                fieldset.fields.append(fieldname)
                return

        # not found, need to create new fieldset
        new_fieldset = Fieldset(
            to_fieldset_name,
            fields=[fieldname],
        )
        if label is not None:
            new_fieldset.label = label
        if description is not None:
            new_fieldset.description = description
        if order is not None:
            new_fieldset.order = order
        fieldsets_direct.append(new_fieldset)
        # Done!

    def fix_documento_schema(self):
        """fix Documento fields"""
        IDocumento["formati_disponibili"].required = False
        IDocumento["ufficio_responsabile"].required = False
        IDocumento.setTaggedValue(
            OMITTED_KEY,
            [
                (Interface, "protocollo", "true"),
                (Interface, "data_protocollo", "true"),
                (Interface, "formati_disponibili", "true"),
                (Interface, "dataset", "true"),
            ],
        )
        if self.schema.getName() == "IArgomentiDocumento":
            self.schema["tassonomia_argomenti"].required = False

    def fix_event_schema(self):
        """fix Documento fields"""
        if self.schema.getName() == "IArgomentiEvento":
            self.schema["tassonomia_argomenti"].required = False
            self.move_field(
                schema=self.schema,
                fieldname="correlato_in_evidenza",
                to_fieldset_name="correlati",
            )
        if self.schema.getName() == "IEvento":
            self.schema["descrizione_estesa"].required = False
            self.schema["descrizione_destinatari"].required = False
            self.move_field(
                schema=self.schema,
                fieldname="patrocinato_da",
                to_fieldset_name="informazioni",
            )

    def fix_news_schema(self):
        """fix News Item fields"""
        if self.schema.getName() == "IArgomentiNews":
            self.schema["tassonomia_argomenti"].required = False
        if self.schema.getName() == "INewsAdditionalFields":
            self.schema["descrizione_estesa"].required = False
            self.schema["a_cura_di"].required = False
            self.move_field(
                schema=self.schema,
                fieldname="notizie_correlate",
                to_fieldset_name="default",
            )

    def fix_persona_schema(self):
        """fix Persona fields"""
        IPersona.setTaggedValue(OMITTED_KEY, [(Interface, "incarichi_persona", "true")])

    def fix_servizio_schema(self):
        """fix Persona fields"""
        if self.schema.getName() == "IArgomentiServizio":
            self.schema["tassonomia_argomenti"].required = False
            self.move_field(
                schema=self.schema,
                fieldname="correlato_in_evidenza",
                to_fieldset_name="correlati",
            )
        IServizio.setTaggedValue(
            OMITTED_KEY,
            [
                (Interface, "condizioni_di_servizio", "true"),
                (Interface, "canale_digitale_link", "true"),
                (Interface, "canale_fisico", "true"),
                (Interface, "timeline_tempi_scadenze", "true"),
            ],
        )
        IServizio["a_chi_si_rivolge"].required = False
        IServizio["come_si_fa"].required = False
        IServizio["cosa_si_ottiene"].required = False
        IServizio["tempi_e_scadenze"].required = False
        self.move_field(
            schema=IServizio,
            fieldname="codice_ipa",
            to_fieldset_name="categorization",
        )
        self.move_field(
            schema=IServizio,
            fieldname="settore_merceologico",
            to_fieldset_name="categorization",
        )

    def fix_unita_organizzativa_schema(self):
        """fix UnitaOrganizzativa fields"""
        IUnitaOrganizzativa["competenze"].required = False
        IUnitaOrganizzativa["sede"].required = False
        IUnitaOrganizzativa.setTaggedValue(
            OMITTED_KEY, [(Interface, "documenti_pubblici", "true")]
        )

    def fix_luogo_schema(self):
        """fix UnitaOrganizzativa fields"""
        if self.schema.getName() == "ILuogo":
            self.schema["modalita_accesso"].required = False
