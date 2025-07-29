# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone.app.contenttypes.browser.collection import CollectionView
from Products.Five import BrowserView
from plone import api
from Products.CMFCore.utils import getToolByName


class PubblicazioneView(BrowserView):
    """
    Vista del contenuto Pubblicazione
    """

    def toLocalizedTime(self, publication_date):
        plone_view = api.content.get_view(
            name='plone',
            context=self.context,
            request=self.request
        )
        time = DateTime(publication_date.strftime('%Y-%m-%d'))
        return plone_view.toLocalizedTime(time, False, False)

    def get_mime_type(self, context):
        portal = api.portal.get()
        mimereg = getToolByName(portal, 'mimetypes_registry')
        filename = context.publicationFile.filename
        return mimereg.lookupExtension(filename).extensions[0].upper()

    def get_file_size(self, context):
        return format(
            context.publicationFile.getSize()/float(1024*1024), '.2f'
        )


class PubblicazioniCollectionView(CollectionView):
    """
    Vista del contenuto Pubblicazione
    """

    def toLocalizedTime(self, publication_date):
        plone_view = api.content.get_view(
            name='plone',
            context=self.context,
            request=self.request
        )
        time = DateTime(publication_date.strftime('%Y-%m-%d'))
        return plone_view.toLocalizedTime(time, False, False)
