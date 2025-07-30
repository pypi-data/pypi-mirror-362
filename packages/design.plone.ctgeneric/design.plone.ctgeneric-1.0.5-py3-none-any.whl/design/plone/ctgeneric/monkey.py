from design.plone.ctgeneric import _
from plone import api
from zope.i18n import translate


def get_design_meta_type(self):
    ttool = api.portal.get_tool("portal_types")
    tipologia_notizia = getattr(self.context, "tipologia_notizia", "")
    if self.context.portal_type == "News Item" and tipologia_notizia:
        return translate(
            tipologia_notizia,
            domain=_._domain,
            context=self.request,
        )
    return translate(ttool[self.context.portal_type].Title(), context=self.request)
