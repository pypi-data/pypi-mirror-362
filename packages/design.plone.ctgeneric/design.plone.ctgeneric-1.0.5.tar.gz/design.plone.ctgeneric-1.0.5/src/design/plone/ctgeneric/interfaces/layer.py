# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from design.plone.contenttypes.interfaces import IDesignPloneContenttypesLayer


class IDesignPloneCtgenericLayer(IDesignPloneContenttypesLayer):
    """Marker interface that defines a browser layer."""
