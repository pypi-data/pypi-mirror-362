# This package provides a hook for PyInstaller
# needed to successfully freeze
# the :doc:`pyi_hooksample package <../__init__.py>`.
# It also provides test-data for that hook.
import os

# Functions
# =========
#
# .. _get_hook_dirs:
#
# get_hook_dirs
# -------------
#
# Tell PyInstaller where to find hooks provided by this distribution;
# this is referenced by the :ref:`hook registration <hook_registration>`.
# This function returns a list containing only the path to this
# directory, which is the location of these hooks.

def get_hook_dirs():
    return [os.path.dirname(__file__)]

# .. _get_PyInstaller_tests:
#
# get_PyInstaller_tests
# ---------------------
#
# Tell PyInstaller where to find test-data of the hooks provided by this
# distribution; this is referenced by the :ref:`test-data registration
# <tests_registration>`. This function returns a list containing only
# the path to this directory, which is the location of these test-data.

def get_PyInstaller_tests():
    return [os.path.dirname(__file__)]