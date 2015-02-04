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
from django.contrib.auth import login, authenticate
from django_basic import HttpBasicAuthenticator, HttpResponseUnauthorized

# Uses the HttpBasicAuthenticator to enforce HTTP basic authentication for
# an entire application.

class HttpBasicMiddleware(object):
    realm = "Auth"
        
    def process_request(self, request):
        if request.user.is_authenticated():
            return 
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth:
            auth = auth.split()
            if len(auth) == 2 and auth[0].lower() == 'basic':
                username, password = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    return
        response = HttpResponseUnauthorized()
        response['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        return response

class HttpMultipleMiddleware(object):
    def __init__(self, *components):
        self.components = components

    def process_request(self, request):
        headers = []
        for comp in self.components:
            response = comp.process_request(request)
            if response is not None:
                if response.status_code != 401:
                    return response
                header = response.get('WWW-Authenticate', None)
                if header:
                    headers.append(header)
        if headers:
            pass

    def process_response(self, request, response):
        return None
