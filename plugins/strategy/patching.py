# -*- coding: utf-8 -*-
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

from contextlib import ContextDecorator
import os
import difflib


# Written by @AKrumov
# https://github.com/mitogen-hq/mitogen/issues/1034#issuecomment-1851557386
patch_1034_v1 = """
--- core.old    2024-02-29 14:53:29.478417261 +0200
+++ core.py     2024-02-29 14:53:48.846102667 +0200
@@ -842,11 +842,15 @@
         s, n = LATIN1_CODEC.encode(s)
         return s

+    def _unpickle_ansible_unsafe_text(self, serialized_obj):
+        return serialized_obj
+
     def _find_global(self, module, func):
         \"""
         Return the class implementing `module_name.class_name` or raise
         `StreamError` if the module is not whitelisted.
         \"""
+        print(module, __name__)
         if module == __name__:
             if func == '_unpickle_call_error' or func == 'CallError':
                 return _unpickle_call_error
@@ -860,6 +864,8 @@
                 return Secret
             elif func == 'Kwargs':
                 return Kwargs
+        elif module == 'ansible.utils.unsafe_proxy' and func == 'AnsibleUnsafeText':
+            return self._unpickle_ansible_unsafe_text
         elif module == '_codecs' and func == 'encode':
             return self._unpickle_bytes
         elif module == '__builtin__' and func == 'bytes':
"""


def loaders_path():
    import ansible_mitogen

    loaders_path = os.path.join(os.path.dirname(ansible_mitogen.__file__), "loaders.py")
    return loaders_path


def core_path():
    from mitogen import core

    return core.__file__


class patches(ContextDecorator):
    ORIG_LINE = "ANSIBLE_VERSION_MAX = (2, 13)\n"
    PATCH_LINE = "ANSIBLE_VERSION_MAX = (2, 16)\n"

    def mv(self, src, dst):
        os.move(src, dst)
        self.renames.append({"module": src, "original": dst})

    def __enter__(self):
        # did this process patched it or it's concurrent process?
        self.patched = False
        self.renames = []
        loader_module_file = loaders_path()
        loader_module_file_orig = loader_module_file + ".orig"

        # pre-guard
        with open(loader_module_file) as f:
            if self.ORIG_LINE not in f.read():
                return self

        # atomic-lock
        try:
            os.link(loader_module_file, loader_module_file_orig)
            os.unlink(loader_module_file)
        except FileExistsError:
            raise Exception(
                f"Race other patching, or stale {loader_module_file_orig} file"
            )

        # post-guard
        with open(loader_module_file_orig) as f:
            if self.ORIG_LINE not in f.read():
                # unlucky situation, we moved file after someone patched it
                # We move it back and do not touch anything
                os.rename(loader_module_file_orig, loader_module_file)
                raise Exception(
                    "Race post-condition with other mitogen patching, aborting"
                )

        # if we moved file, and the moved file is not patched, we have exclusive
        # lock for patching.

        self.patched = True

        # version patch
        self.renames.append(
            {
                "module": loader_module_file,
                "original": loader_module_file_orig,
            }
        )
        with open(loader_module_file_orig) as source:
            with open(loader_module_file, "w") as dest:
                for line in source.readlines():
                    if line == self.ORIG_LINE:
                        line = self.PATCH_LINE
                    dest.write(line)
        return self

        # bug 1034 patch
        core_module = core_path()
        core_module_orig = core_module + ".orig"
        self.mv(core_module, core_module_orig)

    def __exit__(self, *exc):
        if self.patched:
            for rename in self.renames:
                os.rename(rename["original"], rename["module"])
        return False
