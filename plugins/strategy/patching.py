from contextlib import ContextDecorator
import os


def loaders_path():
    import ansible_mitogen

    loaders_path = os.path.join(os.path.dirname(ansible_mitogen.__file__), "loaders.py")
    return loaders_path


class patch_version(ContextDecorator):
    ORIG_LINE = "ANSIBLE_VERSION_MAX = (2, 13)\n"
    PATCH_LINE = "ANSIBLE_VERSION_MAX = (2, 15)\n"

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
                    if line == "ANSIBLE_VERSION_MAX = (2, 13)\n":
                        line = "ANSIBLE_VERSION_MAX = (2, 15)\n"
                    dest.write(line)
        return self

    def __exit__(self, *exc):
        if self.patched:
            os.rename(self.lp_orig, self.lp)
        return False
