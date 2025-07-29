# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from .interfaces import IPubblicazione
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.app.textfield.value import IRichTextValue
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode


def SearchableText(obj):
    text = ""
    if obj.abstract:
        textvalue = obj.abstract
        if IRichTextValue.providedBy(textvalue):
            transforms = getToolByName(obj, "portal_transforms")
            text = (
                transforms.convertTo(
                    "text/plain",
                    safe_unicode(textvalue.raw),
                    mimetype=textvalue.mimeType,
                )
                .getData()
                .strip()
            )

    subject = " ".join([safe_unicode(s) for s in obj.Subject()])

    return " ".join(
        (
            safe_unicode(obj.id),
            safe_unicode(obj.title) or "",
            safe_unicode(obj.description) or "",
            safe_unicode(text),
            safe_unicode(subject),
        )
    )


@indexer(IPubblicazione)
def author_indexer(obj, **kw):
    """Factory method per l'indicizzazione del campo autori di una
    pubblicazione.
    """
    return getattr(obj, "publicationAuthor", ())


@indexer(IPubblicazione)
def publication_types_indexer(obj, **kw):
    """
    index the publication type
    """
    return obj.publicationType


@indexer(IPubblicazione)
def publication_language_indexer(obj, **kw):
    """
    index the publication language
    """
    return obj.publicationLanguage


@indexer(IPubblicazione)
def publication_date_indexer(obj, **kw):
    """
    index the publication date
    """
    return obj.publicationDate


@indexer(IPubblicazione)
def publication_searchable_text(obj, **kw):
    return _unicode_save_string_concat(SearchableText(obj))
