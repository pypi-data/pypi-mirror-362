# test-pywipe.py

import unittest
from unittest.mock import patch
from pywipe import core, utils

class TestPyWipe(unittest.TestCase):

    @patch('pywipe.core.get_installed_packages')
    def test_get_packages_to_uninstall(self, mock_get_installed):
        mock_get_installed.return_value = ['requests', 'numpy', 'pip', 'setuptools', 'my-tool']
        whitelist = ['my-tool']
        result = core.get_packages_to_uninstall(whitelist)
        self.assertIn('requests', result)
        self.assertIn('numpy', result)
        self.assertNotIn('pip', result)
        self.assertNotIn('setuptools', result)
        self.assertNotIn('my-tool', result)

    @patch('sys.prefix', '/usr/local')
    @patch('sys.base_prefix', '/usr')
    def test_is_in_virtualenv_true(self):
        self.assertTrue(utils.is_in_virtualenv())

    @patch('sys.prefix', '/usr')
    @patch('sys.base_prefix', '/usr')
    def test_is_in_virtualenv_false(self):
        self.assertFalse(utils.is_in_virtualenv())

if __name__ == '__main__':
    unittest.main()