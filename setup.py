#!/usr/bin/env python
#
# Copyright (c) 2011, SmartFile <btimby@smartfile.com>
# All rights reserved.
#
# This file is part of django-basic.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with django-basic.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name='django-basic',
    version='0.1',
    description=('An implementation of HTTP Basic Authentication for Django.'),
    long_description=(
"""
django-basic supplies a middleware (HttpBasicMiddleware) that may installed to protect access
to all URLs, a decorator (@httpbasic) that may be applied to selected view functions, and a
simple class (HttpBasicAuthenticator) that can be used to implement custom authentication
scenarios.

django-basic also provides a decorator (@httpmultiple) which can be combined with the @httpdigest
decorator from the django-digest project to provide both authentication schemes together.
"""
    ),
    author='SmartFile',
    author_email='btimby@smartfile.com',
    url='http://code.google.com/p/django-basic/',
    packages=['django_basic'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
     ],
    zip_safe=False,
)