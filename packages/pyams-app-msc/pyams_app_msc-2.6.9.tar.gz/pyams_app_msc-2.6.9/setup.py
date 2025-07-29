#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""
This module contains PyAMS MSC application package
"""
import os
from setuptools import setup, find_namespace_packages


DOCS = os.path.join(os.path.dirname(__file__),
                    'docs')

README = os.path.join(DOCS, 'README.rst')
HISTORY = os.path.join(DOCS, 'HISTORY.rst')

version = '2.6.9'
long_description = open(README).read() + '\n\n' + open(HISTORY).read()

tests_require = [
    'pyams_content_themes',
    'pyramid_zcml',
    'zope.exceptions'
]

setup(name='pyams_app_msc',
      version=version,
      description="PyAMS application for cinema reservation management",
      long_description=long_description,
      classifiers=[
          "License :: OSI Approved :: Zope Public License",
          "Development Status :: 4 - Beta",
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Pyramid PyAMS',
      author='Thierry Florac',
      author_email='tflorac@ulthar.net',
      url='https://pyams.readthedocs.io',
      license='ZPL',
      packages=find_namespace_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=[],
      package_data={
          'pyams_msc_app.static': [
              '*.rst', '*.txt', '*.pt', '*.pot', '*.po', '*.mo',
              '*.png', '*.gif', '*.jpeg', '*.jpg', '*.svg',
              '*.ttf', '*.eot', '*.woff', '*.woff2',
              '*.scss', '*.css', '*.js', '*.map'
          ]
      },
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.7',
      # uncomment this to be able to run tests with setup.py
      # test_suite="pyams_app_msc.tests.test_utilsdocs.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'colander',
          'cornice',
          'elasticsearch_dsl',
          'fanstatic',
          'hypatia',
          "importlib_resources; python_version < '3.9'",
          'persistent',
          'pillow',
          'pyams_catalog >= 2.1.0',
          'pyams_content >= 2.2.0',
          'pyams_content_api >= 2.1.0',
          'pyams_content_es >= 2.2.0',
          'pyams_file',
          'pyams_form >= 2.1.0',
          'pyams_i18n',
          'pyams_layer',
          'pyams_mail',
          'pyams_pagelet',
          'pyams_portal',
          'pyams_scheduler >= 2.7.0',
          'pyams_security >= 2.2.1',
          'pyams_security_views',
          'pyams_sequence',
          'pyams_site',
          'pyams_skin >= 2.2.3',
          'pyams_table',
          'pyams_utils >= 2.3.1',
          'pyams_viewlet',
          'pyams_workflow',
          'pyams_zmi >= 2.6.0',
          'pyams_zmq',
          'pyramid',
          'pyramid_mailer',
          'reportlab',
          'requests',
          'transaction',
          'ZODB',
          'zope.annotation',
          'zope.container',
          'zope.copy',
          'zope.dublincore',
          'zope.interface',
          'zope.intid',
          'zope.lifecycleevent',
          'zope.location',
          'zope.principalannotation',
          'zope.schema',
          'zope.traversing'
      ],
      entry_points={
          'fanstatic.libraries': [
              'msc = pyams_app_msc.zmi:library',
              'mscapp = pyams_app_msc.skin:library'
          ]
      })
