# -*- coding: utf-8 -*-
from design.plone.ctgeneric.interfaces import IDesignPloneV2Settings
from design.plone.ctgeneric.interfaces import IDesignPloneV2SettingsControlpanel
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, Interface)
@implementer(IDesignPloneV2SettingsControlpanel)
class DesignPloneV2Settings(RegistryConfigletPanel):
    schema = IDesignPloneV2Settings
    configlet_id = "DesignPloneV2Settings"
    configlet_category_id = "Products"
    schema_prefix = None
