# (c) ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, 2021-2025.
# See the LICENSE file for more details.

import io

import setuptools

long_description = io.open("README.md", encoding="utf-8").read()
version = __import__("django_epflmisc").__version__
source_url = "https://github.com/epfl-si/django-epfl-misc"

setuptools.setup(
    name="django-epfl-misc",
    version=version,
    url=source_url,
    author="William Belle",
    author_email="william.belle@gmail.com",
    description="A Django application with helper functions and utilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    zip_safe=False,
    project_urls={
        "Changelog": source_url + "/blob/main/CHANGELOG.md",
        "Source": source_url,
        "Tracker": source_url + "/issues",
    },
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
)
