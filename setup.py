from setuptools import setup, find_packages

"""
:author: abuztrade
:license: MIT License, see LICENSE file.
:copyright: (c) 2025 by abuztrade.
"""


version = '1.0'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="proxyseller",
    version=version,

    author="abuztrade",
    author_email="abuztrade.work@gmail.com",

    url="https://github.com/makarworld/proxyseller.git",
    download_url=f"https://github.com/makarworld/proxyseller/archive/refs/tags/v{version}.zip",

    description="Unofficial python library for working with proxy-seller.com",

    packages=['proxyseller'],
    install_requires=['requests'],

    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Communications :: Email",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.10",

        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    include_package_data=True, # for MANIFEST.in
    python_requires='>=3.10.0',

    package_data={package: ["py.typed", "*.pyi", "**/*.pyi"] for package in find_packages()},
    zip_safe=False,
)