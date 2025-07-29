from .data.setup_engine import setup
from .data.setup_engine import VersionInfo
from .data.version import version_info, __version__
import warnings
warnings.filterwarnings("ignore")
"""
config = setup(
    name="MyModule",
    version="1.2.3",
    version_info=(1, 2, 3, "rc", 1),
    sources=["main.cpp"],
    include_dirs=["include"],
    library_dirs=["libs"],
    libraries=["mylib"],
    define_macros=[("DEBUG", "1"), ("VERSION", '"1.2.3"')],
    extra_compile_args=["-O3", "-Wall"],
    extra_link_args=["-static-libgcc", "-static-libstdc++"],
    std="c++20"
)
"""