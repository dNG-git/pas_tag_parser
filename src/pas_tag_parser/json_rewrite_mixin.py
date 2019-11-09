# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;tag_parser

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasTagParserVersion)#
#echo(__FILEPATH__)#
"""

from dpt_json import JsonResource
from dpt_runtime.binary import Binary

from .abstract_mixin import AbstractMixin

class JsonRewriteMixin(AbstractMixin):
    """
This tag parser mixin provides support for JSON based rewrite statements.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def render_json_rewrite(self, json_resource, json_base_path, json_value_path):
        """
Renders the data identified by the given node value path in the JSON
resource.

:param json_resource: JSON resource instance
:param json_base_path: JSON base node path
:param json_value_path: JSON value node path

:return: (str) Rendered content
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_json_rewrite({1}, {2})- (#echo(__LINE__)#)", self, json_base_path, json_value_path, context = "pas_tag_parser")

        if (json_base_path != ""): json_value_path = "{0} {1}".format(json_base_path, json_value_path)

        _return = (json_resource.get_node(json_value_path)
                   if (isinstance(json_resource, JsonResource)) else
                   ""
                  )

        _return = ("" if (_return is None) else Binary.str(_return))
        if (type(_return) is not str): _return = str(_return)

        return _return
    #
#
