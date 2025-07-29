# ruff: noqa: D104


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'moocore.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-moocore-0.1.8.dev0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-moocore-0.1.8.dev0')) as file:
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

from ._moocore import (
    Hypervolume,
    ReadDatasetsError,
    RelativeHypervolume,
    apply_within_sets,
    avg_hausdorff_dist,
    eaf,
    eafdiff,
    epsilon_additive,
    epsilon_mult,
    filter_dominated,
    filter_dominated_within_sets,
    hv_approx,
    hv_contributions,
    hypervolume,
    igd,
    igd_plus,
    is_nondominated,
    is_nondominated_within_sets,
    largest_eafdiff,
    normalise,
    pareto_rank,
    read_datasets,
    total_whv_rect,
    vorob_dev,
    vorob_t,
    whv_hype,
    whv_rect,
)

from ._datasets import (
    get_dataset,
    get_dataset_path,
)

from importlib.metadata import version as _metadata_version

__version__ = _metadata_version("moocore")
# Remove symbols imported for internal use
del _metadata_version


__all__ = [
    "Hypervolume",
    "ReadDatasetsError",
    "RelativeHypervolume",
    "apply_within_sets",
    "avg_hausdorff_dist",
    "eaf",
    "eafdiff",
    "epsilon_additive",
    "epsilon_mult",
    "filter_dominated",
    "filter_dominated_within_sets",
    "get_dataset",
    "get_dataset_path",
    "hv_approx",
    "hv_contributions",
    "hypervolume",
    "igd",
    "igd_plus",
    "is_nondominated",
    "is_nondominated_within_sets",
    "largest_eafdiff",
    "normalise",
    "pareto_rank",
    "read_datasets",
    "total_whv_rect",
    "vorob_dev",
    "vorob_t",
    "whv_hype",
    "whv_rect",
]
