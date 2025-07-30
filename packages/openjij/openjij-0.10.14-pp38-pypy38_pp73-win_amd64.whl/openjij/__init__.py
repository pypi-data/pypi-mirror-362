"""""" # start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'openjij.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-openjij-0.10.14')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-openjij-0.10.14')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

from openjij import cxxjij

from openjij.model.model import BinaryPolynomialModel, BinaryQuadraticModel
from openjij.sampler.csqa_sampler import CSQASampler
from openjij.sampler.response import Response
from openjij.sampler.sa_sampler import SASampler
from openjij.sampler.sqa_sampler import SQASampler
from openjij.utils.benchmark import solver_benchmark
from openjij.utils.res_convertor import convert_response
from openjij.variable_type import BINARY, SPIN, Vartype, cast_vartype
from openjij.sampler.base_sa_sample_hubo import base_sample_hubo


__all__ = [
    "cxxjij",
    "SPIN",
    "BINARY",
    "Vartype",
    "cast_vartype",
    "Response",
    "SASampler",
    "SQASampler",
    "CSQASampler",
    "BinaryQuadraticModel",
    "BinaryPolynomialModel",
    "solver_benchmark",
    "convert_response",
    "base_sample_hubo",
]
