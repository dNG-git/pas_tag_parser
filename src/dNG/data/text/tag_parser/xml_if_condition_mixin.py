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

# pylint: disable=import-error, no-name-in-module

from dNG.data.binary import Binary

from .abstract_mixin import AbstractMixin

class XmlIfConditionMixin(AbstractMixin):
    """
This tag parser mixin provides support for if conditions based on XML
values.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: tag_parser
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def render_xml_if_condition(self, xml_parser, xml_base_path, xml_value_path, operator, value, data):
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

        if (self._log_handler is not None): self._log_handler.debug("#echo(__FILEPATH__)# -{0!r}.render_xml_if_condition({1}, {2}, {3}, {4})- (#echo(__LINE__)#)", self, xml_base_path, xml_value_path, operator, value, context = "pas_tag_parser")
        _return = ""

        is_valid = False
        xml_value = xml_parser.get_node_value("{0} {1}".format(xml_base_path, xml_value_path))

        xml_value = ("" if (xml_value is None) else Binary.str(xml_value))
        if (type(xml_value) is not str): xml_value = str(xml_value)

        if (operator == "==" and xml_value == value): is_valid = True
        if (operator == "!=" and xml_value != value): is_valid = True

        if (is_valid): _return = data
        return _return
    #
#
