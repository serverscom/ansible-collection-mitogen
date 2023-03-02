from patching import patch_version

with patch_version():
    from ansible_mitogen.plugins.strategy.mitogen_linear import *
