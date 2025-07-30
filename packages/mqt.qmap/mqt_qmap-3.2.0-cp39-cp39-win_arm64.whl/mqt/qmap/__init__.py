# Copyright (c) 2023 - 2025 Chair for Design Automation, TUM
# Copyright (c) 2025 Munich Quantum Software Company GmbH
# All rights reserved.
#
# SPDX-License-Identifier: MIT
#
# Licensed under the MIT License

"""MQT QMAP library."""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_qmap.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-mqt_qmap-3.2.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-mqt_qmap-3.2.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

import sys

# under Windows, make sure to add the appropriate DLL directory to the PATH
if sys.platform == "win32":

    def _dll_patch() -> None:
        """Add the DLL directory to the PATH."""
        import os
        import sysconfig
        from pathlib import Path

        site_packages = Path(sysconfig.get_paths()["purelib"])
        bin_dir = site_packages / "mqt" / "core" / "bin"
        os.add_dll_directory(str(bin_dir))

        if "Z3_ROOT" in os.environ:  # pragma: no cover
            lib_path = Path(os.environ["Z3_ROOT"]) / "lib"
            if lib_path.exists():
                os.add_dll_directory(str(lib_path))
            bin_path = Path(os.environ["Z3_ROOT"]) / "bin"
            if bin_path.exists():
                os.add_dll_directory(str(bin_path))

        z3_dir = site_packages / "z3"
        if z3_dir.exists():  # pragma: no cover
            lib_path = z3_dir / "lib"
            if lib_path.exists():
                os.add_dll_directory(str(lib_path))
            bin_path = z3_dir / "bin"
            if bin_path.exists():
                os.add_dll_directory(str(bin_path))

    _dll_patch()
    del _dll_patch


from ._version import version as __version__

__all__ = [
    "__version__",
]
