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

import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Provides the HttpBasicAuthenticator to perform HTTP basic authentication.

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self):
        super(HttpResponseUnauthorized, self).__init__('Authorization Required')


class HttpBasicAuthenticator(object):
    def __init__(self, realm):
        self.realm = realm

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            return False
        auth = auth.split()
        if len(auth) != 2 or auth[0].lower() != 'basic':
            return False
        username, password = base64.b64decode(auth[1]).split(':')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return True

    def challenge(self, request):
        response = HttpResponseUnauthorized()
        response['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        return response
