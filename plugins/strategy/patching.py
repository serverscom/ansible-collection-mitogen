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


def loaders_path():
    import ansible_mitogen

    loaders_path = os.path.join(os.path.dirname(ansible_mitogen.__file__), "loaders.py")
    return loaders_path


class patch_version(ContextDecorator):
    ORIG_LINE = "ANSIBLE_VERSION_MAX = (2, 13)\n"
    PATCH_LINE = "ANSIBLE_VERSION_MAX = (2, 16)\n"

    def __enter__(self):
        self.patched = False
        self.lp = loaders_path()
        self.lp_orig = self.lp + ".orig"

        with open(self.lp) as f:
            if not self.ORIG_LINE in f.read():
                return self

        if os.path.isfile(self.lp_orig):
            return self

        os.rename(self.lp, self.lp_orig)
        self.patched = True
        with open(self.lp_orig) as source:
            with open(self.lp, "w") as dest:
                for line in source.readlines():
                    if line == ORIG_LINE:
                        line = PATCH_LINE
                    dest.write(line)
        return self

    def __exit__(self, *exc):
        if self.patched:
            os.rename(self.lp_orig, self.lp)
        return False
