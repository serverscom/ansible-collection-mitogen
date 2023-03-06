from . import patching

with patching.patch_version():
    from ansible_mitogen.plugins.strategy.mitogen_free import *
