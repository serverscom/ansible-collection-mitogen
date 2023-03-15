#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Ansible strategy plugin wrapper to patch mitogen version requirements.

"""

DOCUMENTATION = """
---
name: mitogen
author: |
    Sergey Putko <psvmcc+ansible-galaxy@gmail.com>
    George Shuklin <george.shuklin@gmail.com>
description: Ansible strategy plugin wrapper to patch mitogen version requirements.
short_description: Mitogen patching strategy
"""


from . import patching

with patching.patch_version():
    from ansible_mitogen.plugins.strategy.mitogen import *
