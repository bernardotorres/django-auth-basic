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

from django_basic import HttpBasicAuthenticator, HttpResponseUnauthorized

# Uses the HttpBasicAuthenticator to enforce HTTP basic authentication for
# a single view.

class HttpDummyResponse(object):
    pass


# http://djangosnippets.org/snippets/1871/
class HttpResponseMultiValue(HttpResponseUnauthorized):
    def __init__(self, *args, **kwargs):
        self._multi_value_headers = {}
        super(HttpResponseMultiValue, self).__init__(*args, **kwargs)
        for item in super(HttpResponseMultiValue, self).items():
            self[item[0]] = item[1]

    def __str__(self):
        return '\n'.join(['%s: %s' % (key, value)
                          for key, value in self.items()]) + '\n\n' + self.content
    
    def __setitem__(self, header, value):
        header, value = self._convert_to_ascii(header, value)
        self._multi_value_headers[header.lower()] = [(header, value)]

    def __getitem__(self, header):
        return self._multi_value_headers[header.lower()][0][1]

    def items(self):
        items = []
        for header_values in self._multi_value_headers.values():
            for entry in header_values:
                items.append((entry[0], entry[1]))
        return items

    def get(self, header, alternate):
        return self._multi_value_headers.get(header.lower(), [(None, alternate)])[0][1]

    def add_header_value(self, header, value):
        header, value = self._convert_to_ascii(header, value)
        self._multi_value_headers.setdefault(header.lower(), []).append((header, value))

    def get_header_values(self, header):
        header = self._convert_to_ascii(header)
        return [header[1] for header in self._multi_value_headers.get(header.lower(), [])]


def httpbasic(realm='WebDAV'):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if authenticator.authenticate(request):
                return view(request, *args, **kwargs)
            return authenticator.challenge(request)
        return wrapper
    authenticator = HttpBasicAuthenticator(realm)
    return decorator


def httpmultiple(*providers):
    def decorator(view):
        def dummy(request, *args, **kwargs):
            return HttpDummyResponse()
        def wrapper(request, *args, **kwargs):
            headers = []
            is_authenticated = False
            for provider in providers:
                response = provider(dummy)(request, *args, **kwargs)
                if isinstance(response, HttpDummyResponse):
                    is_authenticated = True
                    break
                header = response.get('WWW-Authenticate', None)
                if header:
                    headers.append(header)
            if is_authenticated or not headers:
                return view(request, *args, **kwargs)
            response = HttpResponseMultiValue()
            for header in headers:
                response.add_header_value('WWW-Authenticate', header)
            return response
        return wrapper
    return decorator