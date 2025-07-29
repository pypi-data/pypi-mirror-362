# -*- coding: utf-8 -*-

from plone import api
from plone.api.exc import InvalidParameterError
from plone.memoize import view
from Products.Five import BrowserView
from rer.pubblicazioni.browser.interfaces import IRerPubblicazioniUtilsView
from zope.interface import implementer
from rer.pubblicazioni import logger


@implementer(IRerPubblicazioniUtilsView)
class RerPubblicazioniUtilsView(BrowserView):
    """ """

    @view.memoize
    def extract_value_from_settings(self, entry_name):
        """ this one is the one to get a simple value"""
        setting_name = "{}{}{}".format(
            'rer.pubblicazioni.browser.',
            'settings.IRerPubblicazioniSettings.',
            entry_name
        )
        try:
            value = api.portal.get_registry_record(setting_name)
        except (InvalidParameterError, AttributeError) as err:
            logger.exception(err)
            return ""
        if not value:
            return ""
        return value
