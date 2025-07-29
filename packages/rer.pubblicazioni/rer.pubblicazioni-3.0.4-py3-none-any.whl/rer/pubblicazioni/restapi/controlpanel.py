from plone.restapi.controlpanels import RegistryConfigletPanel
from rer.pubblicazioni.browser.settings import IRerPubblicazioniSettings
from rer.pubblicazioni.interfaces import IRerPubblicazioniLayer
from rer.pubblicazioni.interfaces import IRerPubblicazioniRestapiControlpanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, IRerPubblicazioniLayer)
@implementer(IRerPubblicazioniRestapiControlpanel)
class PubblicazioniSettingsControlpanel(RegistryConfigletPanel):
    schema = IRerPubblicazioniSettings
    configlet_id = "PubblicazioniSettings"
    configlet_category_id = "Products"
    schema_prefix = None
