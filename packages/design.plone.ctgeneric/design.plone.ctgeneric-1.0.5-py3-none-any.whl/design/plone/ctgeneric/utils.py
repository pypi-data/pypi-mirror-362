from design.plone.ctgeneric.interfaces import IDesignPloneV2Settings
from plone import api

import json
import logging
import six


logger = logging.getLogger(__name__)


def get_settings_for_language(field):
    values = api.portal.get_registry_record(
        field, interface=IDesignPloneV2Settings, default=[]
    )
    if not values:
        return []
    if not isinstance(values, six.text_type):
        return values
    try:
        json_data = json.loads(values)
    except Exception as e:
        logger.exception(e)
        return values
    lang = api.portal.get_current_language()
    return json_data.get(lang, [])
