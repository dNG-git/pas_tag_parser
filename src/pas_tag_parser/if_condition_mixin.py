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

from dpt_runtime.binary import Binary

from .source_value_mixin import SourceValueMixin

class IfConditionMixin(SourceValueMixin):
    """
This tag parser mixin provides support for if conditions.

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

    def render_if_condition(self, source, key, operator, value, data):
        """
Checks and renders the content of the "if" condition.

:param data: Conditional data
:param source: Source for comparison
:param key: Key in source for comparison
:param operator: Comparison operator
:param value: Comparison value

:return: (str) Conditional data if successful
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_if_condition({1}, {2}, {3})- (#echo(__LINE__)#)", self, key, operator, value, context = "pas_tag_parser")
        _return = ""

        is_valid = False
        source_value = self.get_source_value(source, key)

        source_value = ("" if (source_value is None) else Binary.str(source_value))
        source_value_type = type(source_value)

        if (source_value_type is bool): source_value = ("1" if (source_value) else "0")
        elif (source_value_type is not str): source_value = str(source_value)

        if (operator == "==" and source_value == value): is_valid = True
        if (operator == "!=" and source_value != value): is_valid = True

        if (is_valid): _return = data
        return _return
    #
#
