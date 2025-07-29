from __future__ import absolute_import

from pyrpmdb._pyinstaller import get_hook_dirs, get_PyInstaller_tests
__all__ = [
    "get_hook_dirs",
    "get_PyInstaller_tests",
    "get_rpm_db_info"
]

"""Extract buildinfo from go built binaries"""

import ctypes
import json
import os
from sysconfig import get_config_var
from pathlib import Path


# Location of shared library
here = Path(__file__).absolute().parent
ext_suffix = get_config_var('EXT_SUFFIX')
so_file = os.path.join(here, ('_pyrpmdb' + ext_suffix))

# Load functions from shared library set their signatures
so = ctypes.cdll.LoadLibrary(so_file)
get_get_rpm_db_info_so = so.getrpmdbInfo
get_get_rpm_db_info_so.argtypes = [ctypes.c_char_p]
get_get_rpm_db_info_so.restype = ctypes.c_void_p
free = so.free
free.argtypes = [ctypes.c_void_p]


def get_rpm_db_info(file_name):
    """Check (in parallel) digital signature of all files in root_dir.
    We assume there's a sha1sum.txt file under root_dir
    """
    res = get_get_rpm_db_info_so(file_name.encode('utf-8'))
    if res is not None:
        result = {"error": "Error converting result to json"}
        try:
            result = json.loads(ctypes.string_at(res).decode('utf-8'))
        except json.JSONDecodeError as e:
            pass
        finally:
            free(res)
        return (result)

