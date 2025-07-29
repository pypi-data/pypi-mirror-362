# -*- coding: utf-8 -*-

from BTrees.IIBTree import intersection
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.vocabularies.terms import safe_encode
from plone.app.vocabularies.terms import safe_simplevocabulary_from_values
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.site.hooks import getSite
from plone import api
from plone.volto.vocabularies.subject import (
    KeywordsVocabulary as BaseKeywordsVocabulary,
)


@implementer(IVocabularyFactory)
class Lingue(object):
    """Factory creating a 'lingue' vocabulary"""

    def get_terms(self, context):
        view = getMultiAdapter(
            (context, context.REQUEST), name="rer-pubblicazioni-utils-view"
        )
        if not view.extract_value_from_settings("lingue"):
            terms = [
                SimpleTerm(
                    title="-- aggiungi lingue dal pannello di controllo --", value=""
                )
            ]
            return terms
        terms = [
            SimpleTerm(title=value, value=value)
            for value in view.extract_value_from_settings("lingue")
        ]
        # terms.insert(0, SimpleTerm(title=u'-- select a value --', value=''))
        return terms

    def __call__(self, context):
        terms = self.get_terms(context)
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class Tipologie(object):
    """Factory creating a 'lingue' vocabulary"""

    def get_terms(self, context):
        view = getMultiAdapter(
            (context, context.REQUEST), name="rer-pubblicazioni-utils-view"
        )
        if not view.extract_value_from_settings("tipologie"):
            terms = [
                SimpleTerm(
                    title="-- aggiungi tipologie dal pannello di controllo --", value=""
                )
            ]
            return terms
        terms = [
            SimpleTerm(title=value, value=value)
            for value in view.extract_value_from_settings("tipologie")
        ]
        return terms

    def __call__(self, context):
        terms = self.get_terms(context)
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class KeywordsVocabulary(BaseKeywordsVocabulary):
    # Allow users to customize the index to easily create
    # KeywordVocabularies for other keyword indexes
    keyword_index = "authors"
    path_index = "path"


KeywordsVocabularyFactory = KeywordsVocabulary()


class BaseIndexValuesVocabulary(object):
    def __call__(self, context, query=None):
        portal = api.portal.get()
        pc = getToolByName(portal, "portal_catalog")

        values = pc.uniqueValuesFor(self.INDEX)
        values = sorted(values)
        terms = [SimpleTerm(title=v, value=v) for v in values if v]
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class PublicationUsedLanguagesVocabulary(BaseIndexValuesVocabulary):
    INDEX = "publication_language"


PublicationUsedLanguagesVocabularyFactory = PublicationUsedLanguagesVocabulary()  # noqa


@implementer(IVocabularyFactory)
class PublicationUsedAuthorsVocabulary(BaseIndexValuesVocabulary):
    INDEX = "authors"


PublicationUsedAuthorsVocabularyFactory = PublicationUsedAuthorsVocabulary()


@implementer(IVocabularyFactory)
class PublicationUsedTypesVocabulary(BaseIndexValuesVocabulary):
    INDEX = "publication_types"


PublicationUsedTypesVocabularyFactory = PublicationUsedTypesVocabulary()
