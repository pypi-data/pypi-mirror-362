## https://www.juniper.net/documentation/us/en/software/junos-pyez/junos-pyez-developer/topics/task/junos-pyez-tables-views-loading.html

"""
Load tables/views
"""

from os.path import splitext
import yaml
from jnpr.junos.factory import FactoryLoader


_YAML_ = splitext(__file__)[0] + ".yml"

with open(_YAML_, encoding="utf-8") as f:
    yaml_str = f.read()

globals().update(FactoryLoader().load(yaml.safe_load(yaml_str)))
