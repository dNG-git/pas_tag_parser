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

try: from collections.abc import Mapping
except ImportError: from collections import Mapping

from .abstract_mixin import AbstractMixin

class SourceValueMixin(AbstractMixin):
    """
This tag parser mixin provides support to find a key in a given source dict.

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

    def get_source_value(self, source, key):
        """
Returns the value in the source dict identified by the given key.

:param source: Source where key is defined
:param key: Key in source

:return: (mixed) Source value; None if not found
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.get_source_value({1})- (#echo(__LINE__)#)", self, key, context = "pas_tag_parser")
        _return = None

        if (isinstance(source, Mapping)):
            key_list = key.split(".", 1)

            if (key_list[0] in source):
                if (len(key_list) > 1): _return = self.get_source_value(source[key_list[0]], key_list[1])
                else: _return = source[key]
            #
        #

        return _return
    #
#
