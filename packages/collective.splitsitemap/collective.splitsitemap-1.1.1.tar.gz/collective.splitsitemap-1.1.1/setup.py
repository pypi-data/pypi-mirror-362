# -*- coding: utf-8 -*-
"""Installer for the collective.splitsitemap package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.splitsitemap',
    version='1.1.1',
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Enfold Systems, Inc.',
    author_email='info@enfoldsystems.com',
    url='https://github.com/collective/collective.splitsitemap',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.splitsitemap',
        'Source': 'https://github.com/collective/collective.splitsitemap',
        'Tracker': 'https://github.com/collective/collective.splitsitemap/issues',
        # 'Documentation': 'https://collective.splitsitemap.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'six',
        'z3c.jbot',
        'Products.GenericSetup>=1.8.2',
        'plone.schema',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.splitsitemap.locales.update:update_locale
    [zopectl.command]
    generate_sitemaps = collective.splitsitemap.scripts.generate_sitemaps:entrypoint
    """,
)
