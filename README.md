# Ansible collection for mitogen EXAMPLE

## Install
```
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

## Usage
Add to your ansible.cfg
```
strategy_plugins = psvmcc.mitogen
strategy = psvmcc.mitogen.mitogen_linear
```

> based on https://github.com/mitogen-hq/mitogen/issues/961#issuecomment-1236291061
