#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Ansible strategy plugin wrapper to patch mitogen version requirements.

"""

DOCUMENTATION = """
---
name: mitogen_free
author: |
    Sergey Putko <psvmcc+ansible-galaxy@gmail.com>
    George Shuklin <george.shuklin@gmail.com>
description: Ansible strategy plugin wrapper to patch mitogen version requirements.
short_description: Mitogen patching strategy
"""

# Double licensing: You can either GPLv3 or MIT licence.

# GPLv3 license header
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from . import patching

with patching.patches():
    from ansible_mitogen.plugins.strategy.mitogen_free import *
