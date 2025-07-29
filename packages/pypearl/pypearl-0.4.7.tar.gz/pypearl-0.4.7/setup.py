import sys
import os
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

here = os.path.abspath(os.path.dirname(__file__))

# Use C++20 and on macOS point to the system SDK so <stdlib.h> etc. are found
if sys.platform == "darwin":
    sdk_path = subprocess.check_output(
        ["xcrun", "--sdk", "macosx", "--show-sdk-path"]
    ).decode().strip()
    cpp_args = [
        "-std=c++20",
        "-stdlib=libc++",
        "-mmacosx-version-min=10.9",
        "-isysroot", sdk_path,
    ]
    link_args = [
        "-stdlib=libc++",
        "-mmacosx-version-min=10.9",
        "-isysroot", sdk_path,
    ]
else:
    cpp_args  = ["-std=c++20"]
    link_args = []

ext_modules = [
    Extension(
        name="pypearl._pypearl",
        sources=[
            "src/pybinding/binding.cpp",
            "src/pybinding/layerbinding.cpp",
            "src/pybinding/matrixbinding.cpp",
            "src/pybinding/activationbinding/relubinding.cpp",
            "src/pybinding/activationbinding/softmaxbinding.cpp",
            "src/pybinding/lossbinding/ccebinding.cpp",
            "src/pybinding/optimizerbinding/sgdbinding.cpp"
        ],
        include_dirs=[
            # so you can #include "matrix.hpp" and "matrixbinding.hpp"
            os.path.join(here, "src"),
            os.path.join(here, "src", "pybinding"),
        ],
        language="c++",
        extra_compile_args=cpp_args,
        extra_link_args=link_args,
    ),
]

setup(
    name="pypearl",
    version="0.4.7",
    author="Brody Massad",
    author_email="brodymassad@gmail.com",
    description="An efficient Machine Learning Library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    packages=find_packages(),
    package_data={
        "pypearl": ["*.pyi", "py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
)
