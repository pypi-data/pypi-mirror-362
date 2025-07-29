.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.splitsitemap.svg?branch=master
    :target: https://travis-ci.org/collective/collective.splitsitemap

.. image:: https://coveralls.io/repos/github/collective/collective.splitsitemap/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.splitsitemap?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/collective.splitsitemap.svg
    :target: https://pypi.python.org/pypi/collective.splitsitemap/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.splitsitemap.svg
    :target: https://pypi.python.org/pypi/collective.splitsitemap
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.splitsitemap.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.splitsitemap.svg
    :target: https://pypi.python.org/pypi/collective.splitsitemap/
    :alt: License


collective.splitsitemap
#######################

By default, Plone creates 1 sitemap, following the protocol https://www.sitemaps.org/protocol.html

The problem arises on big sites, when the amount of items exceeds 50.000 items. The main goal of this product is to address this, by splitting it into several sitemaps and providing a sitemap index file. In addition it provides some extra advanced features.

Features
********

- Allow to split the sitemap into several sitemaps, and provide a sitemap index
- Allow to generate the sitemap using an external script
- Allow to specify the number of items to include in each split sitemap
- Allow to decide, whether or not "/view" is automatically added in links
- Allow to specify portal types to ignore and not include in the sitemap(s)
- Allow to list specific paths to be ignored and not include in the sitemap(s)


Detailed description
********************

Control panel
=============

This product provides a control panel to configure the different settings. It can be found under the Plone control panel with the name "Split Sitemap Settings" (/@@splitsitemap-settings).

Split sitemaps
==============

This setting allows the sitemap to be split into several and an index sitemap to be generated. The number of items in each sitemap can be tweaked using the "Items per sitemap" setting. When a request to the "sitemap.xml.gz" is performed in your site, and this setting is enabled, several sitemaps will be generated and stored at the location where the sitemap was requested. When the process finishes, the sitemap.xml.gz will be provided with the location of each generated sitemap.

Add /view automatically
=======================

By default, Plone adds "/view" automatically at the end of some URLs, specifically for Files and Images. Unmarking this checkbox, allows to prevent this behavior to happen, only for links in the sitemap. Notice that this setting simply prevents or allows the "/view" to be added automatically, based on how Plone is configured. If Plone does not add "/view" at the end of some URLs, enabling this setting will have no effect.

Generate sitemap from script
============================

This setting allows to use an external script to generate the sitemap, allowing visitors and bots to simply retrieve it without waiting for it to be generated. Notice that if this setting is enabled and the script is not configured to generate the sitemap, then visitors will receive an empty sitemap.xml.gz. Detailed information on the script usage can be found in this README

Specify content types to not include
====================================

From this setting you can choose content types to be completely ignored and not included when generating the sitemap.

Paths to ignore
===============

This setting allows to list specific paths to be ignored from the sitemap. Notice that this path is absolute to the root of the site. If the path is a folder, you can add ":-1" at the end of the path, to ignore that path and all of its children. For example, lets assume this setting is configured as::

    /foo:-1
    /bar

This means that /foo and everything inside will not be included in the sitemap. Additionally /bar will be excluded as well, however if /bar is a folder, its children will not be excluded

External script
***************

This product provides a new zopectl command, which allows to generate sitemaps asynchronously with a cronjob or similar mechanism. Notice that if the "Sitemaps are generated from a script" setting is not enabled, running this script will not improve the sitemap generation in any way. The command is "generate_sitemaps" and its usage is as follows::

  ./bin/instance generate_sitemaps

The script provides 4 optional arguments:

- log_file
- plone_site
- nav_root
- server_url

log_file
========

Specify a file to be used to log the sitemap generation process

plone_site
==========

Specify the id of the Plone site. If not provided, the script will use the first Plone site it finds.

nav_root
========

This is needed, provided your site has different folders used as navigation root (ie. providing the INavigationRoot interface), and you would like to generate a sitemap for that specific folder.

server_url
==========

This setting allows you to generate proper URLs in the sitemap. When running tasks from scripts, there is no way for Plone to know what's the FQDN for your site, or how your Apache/Nginx configuration looks like. Using this setting, you can directly specify your site's URL to be included at the beginning of the link URL. If omitted, the script will attempt to use "SERVER_URL" environment variable.

Example using all parameters
============================

  ``./bin/instance generate_sitemaps --log_file /path/to/sitemap.log --plone_site Plone --nav_root folder-a --server_url https://my-great-site.org``


Installation
************

Install collective.splitsitemap by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.splitsitemap


Then running ``bin/buildout``, and finally installing it from the "Add-ons" Plone control panel.


Contribute
**********

- Issue Tracker: https://github.com/collective/collective.splitsitemap/issues
- Source Code: https://github.com/collective/collective.splitsitemap


TODO
****

- Write tests


License
*******

The project is licensed under the GPLv2.
