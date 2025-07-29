# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from rer.pubblicazioni.testing import RER_PUBBLICAZIONI_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that rer.pubblicazioni is properly installed."""

    layer = RER_PUBBLICAZIONI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if rer.pubblicazioni is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'rer.pubblicazioni'))

    def test_browserlayer(self):
        """Test that IRerPubblicazioniLayer is registered."""
        from rer.pubblicazioni.interfaces import (
            IRerPubblicazioniLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRerPubblicazioniLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RER_PUBBLICAZIONI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['rer.pubblicazioni'])

    def test_product_uninstalled(self):
        """Test if rer.pubblicazioni is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'rer.pubblicazioni'))

    def test_browserlayer_removed(self):
        """Test that IRerPubblicazioniLayer is removed."""
        from rer.pubblicazioni.interfaces import \
            IRerPubblicazioniLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IRerPubblicazioniLayer,
           utils.registered_layers())
