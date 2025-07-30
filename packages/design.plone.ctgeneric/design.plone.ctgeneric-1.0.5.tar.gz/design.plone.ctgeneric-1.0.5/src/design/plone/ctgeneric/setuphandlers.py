# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import ISearchSchema
from zope.component import getUtility
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "design.plone.ctgeneric:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["design.plone.ctgeneric.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    disable_searchable_types()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def disable_searchable_types():
    # remove some types from search enabled ones
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISearchSchema, prefix="plone")
    remove_types = [
        "Dataset",
        "Documento Personale",
        "Messaggio",
        "Pratica",
        "RicevutaPagamento",
        "Incarico",
    ]
    types = [x for x in settings.types_not_searched if x not in remove_types]
    settings.types_not_searched = tuple(types)
