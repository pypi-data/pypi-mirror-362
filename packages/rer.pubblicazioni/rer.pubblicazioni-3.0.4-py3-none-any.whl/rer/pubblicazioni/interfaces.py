# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.namedfile.field import NamedBlobFile
from rer.pubblicazioni import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.restapi.controlpanels.interfaces import IControlpanel


class IRerPubblicazioniLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRerPubblicazioniRestapiControlpanel(IControlpanel):
    """
    Marker interface for controlpanel
    """


class IPubblicazione(Interface):
    abstract = RichText(
        title=_("rer_description_abstract", default="Description/Abstract"),
        description=_(
            "help_rer_description_abstract", default="An abstract of the publication."
        ),
        required=False,
    )

    publicationAuthor = schema.Tuple(
        title=_("rer_pub_author_tags", default="Author/Authors"),
        description=_(
            "help_rer_pub_author_tags",
            default="Autore/autori della pubblicazione",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
        default=(),
    )
    directives.widget(
        "publicationAuthor",
        AjaxSelectFieldWidget,
        vocabulary="rer.pubblicazioni.autori",
    )

    publicationDate = schema.Date(
        title=_("rer_publication_date", default="Publication date"),
        description=_(
            "help_rer_publication_date", default="Insert the date for this publication"
        ),
        required=True,
    )

    publicationType = schema.List(
        title=_("rer_publication_type", default="Publication type"),
        description=_(
            "help_rer_publication_type",
            default="Insert a list of types for this publication",
        ),
        required=False,
        default=[],
        missing_value=[],
        value_type=schema.Choice(vocabulary="rer.pubblicazioni.tipologie"),
    )

    publicationLanguage = schema.Choice(
        title=_("rer_publication_language", default="Language"),
        description=_(
            "help_rer_publication_language",
            default="Select the language of this publication",
        ),
        required=False,
        default="",
        missing_value="",
        vocabulary="rer.pubblicazioni.lingue",
    )

    # "Pubblicato in" - era "Collana"
    publicationSeries = schema.Text(
        title=_("rer_published_in", default="Published in"),
        description=_("help_rer_publication_series", default=""),
        required=False,
    )

    publicationEditor = schema.Text(
        title=_("rer_publication_editor", default="Editor"),
        description=_("help_rer_publication_editor", default=""),
        required=False,
    )

    publicationRights = schema.Text(
        title=_("rer_publication_rights", default="Copyrights"),
        description=_("help_rer_rer_publication_rights", default=""),
        required=False,
    )

    publicationFile = NamedBlobFile(
        title=_("rer_publication_file", default="File"),
        description=_("help_rer_publication_file", default=""),
        required=False,
    )

    publicationURL = schema.TextLine(
        title=_("rer_publication_url", default="URL"),
        description=_("help_rer_publication_url", default=""),
        default="",
        required=False,
    )
