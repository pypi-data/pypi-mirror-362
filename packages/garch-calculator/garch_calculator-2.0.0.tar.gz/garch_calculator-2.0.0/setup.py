#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11
from setuptools import setup, Extension, find_packages
import os
import sys
import platform
import subprocess

# Read version from garch_lib/__init__.py
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'garch_lib', '__init__.py')
    with open(version_file, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return "1.0.0"

__version__ = get_version()

# Read the README file for long description
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

long_description = get_long_description()

def get_boost_paths():
    """尝试找到Boost库的路径"""
    possible_paths = [
        '/usr/include/boost',
        '/usr/local/include/boost',
        '/opt/boost/include/boost',
        '/opt/homebrew/include/boost',  # macOS Homebrew
        os.path.expanduser('~/boost/include/boost'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.dirname(path), os.path.dirname(path).replace('include', 'lib')
    
    return None, None

def get_compiler_flags():
    """获取编译器特定的标志"""
    flags = []
    
    if platform.system() == "Linux":
        flags.extend([
            "-march=native",
            "-mtune=native", 
            "-ffast-math",
            "-DNDEBUG"
        ])
    elif platform.system() == "Darwin":  # macOS
        flags.extend([
            "-march=native",
            "-ffast-math",
            "-DNDEBUG"
        ])
    elif platform.system() == "Windows":
        flags.extend([
            "/O2",
            "/DNDEBUG"
        ])
    
    return flags

# 获取Boost路径
boost_include, boost_lib = get_boost_paths()

# 包含目录
include_dirs = [
    "include",
    pybind11.get_include()
]

if boost_include:
    include_dirs.append(boost_include)

# 库目录
library_dirs = []
if boost_lib:
    library_dirs.append(boost_lib)

# 库文件
libraries = []
if platform.system() != "Windows":
    libraries.extend(["boost_system", "stdc++"])  # Add explicit C++ standard library linking
else:
    libraries.extend(["boost_system"])

# 编译标志
compile_args = ["-std=c++17", "-O3"] + get_compiler_flags()
link_args = []

if platform.system() == "Darwin":  # macOS
    compile_args.extend(["-stdlib=libc++", "-mmacosx-version-min=10.9"])
    link_args.extend(["-mmacosx-version-min=10.9", "-stdlib=libc++"])
elif platform.system() == "Linux":
    # Ensure proper C++ exception handling linking
    link_args.extend(["-lstdc++", "-lm"])

# 源文件
sources = [
    "python/garch_bindings.cpp",
    "src/garch_calculator.cpp"
]

# 定义扩展模块 - 注意这里模块名要与包结构匹配
ext_modules = [
    Pybind11Extension(
        "garch_lib._garch_calculator",  # 模块的全路径名
        sources,
        include_dirs=include_dirs,
        libraries=libraries,
        library_dirs=library_dirs,
        language='c++',
        cxx_std=17,
        extra_compile_args=compile_args,
        extra_link_args=link_args,
    ),
]

setup(
    name="garch-calculator",
    version=__version__,
    author="biteasquirrel",
    author_email="biteasquirrel@gmail.com",
    url="https://github.com/biteasquirrel/garch-calculator",
    description="High-Performance GARCH Calculator with Incremental Updates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Package discovery
    packages=find_packages(include=['garch_lib', 'garch_lib.*']),
    
    # Extension modules
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    
    # Requirements
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.18.0",
    ],
    extras_require={
        "test": [
            "pytest>=6.0",
            "pytest-cov",
        ],
        "dev": [
            "pytest>=6.0", 
            "pytest-cov",
            "black",
            "isort", 
            "flake8",
            "build",
            "twine",
        ],
        "validation": [
            "yfinance>=0.1.63",
            "pandas>=1.3.0",
            "scikit-learn>=1.0.0",
            "matplotlib>=3.3.0",
            "arch>=5.0.0",
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X", 
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Bug Reports": "https://github.com/biteasquirrel/garch-calculator/issues",
        "Source": "https://github.com/biteasquirrel/garch-calculator",
        "Documentation": "https://github.com/biteasquirrel/garch-calculator/blob/main/README.md",
        "Repository": "https://github.com/biteasquirrel/garch-calculator.git",
    },
    keywords="garch volatility finance econometrics time-series forecasting risk-management",
    
    # Include package data
    include_package_data=True,
    zip_safe=False,
) 