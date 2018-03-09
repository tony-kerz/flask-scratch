import os
# import logging
import logging.config
import yaml
from functools import reduce
from box import Box

env = os.getenv('PY_ENV') or 'default'
print(f"env={env}")


def dict_if(file):
    if os.path.isfile(file):
        print(f"found {file}")
        return yaml.load(open(file))


# https://stackoverflow.com/a/20666342/2371903
# will overwrite v merge lists


def merge_dict(target, source):
    target = target or {}
    if source:
        for key, value in source.items():
            if isinstance(value, dict):
                node = target.setdefault(key, {})
                merge_dict(node, value)
            elif value is not None:
                target[key] = value
    return target


def env_dict(target):
    def reducer(result, key):
        val = target[key]
        result[key] = env_dict(val) if isinstance(
            val, dict) else os.getenv(val)
        return result

    return reduce(reducer, target.keys(), {})


config = dict_if('config/config.yml')
config = merge_dict(target=config, source=dict_if(f"config/config.{env}.yml"))
config = merge_dict(target=config, source=env_dict(
    dict_if('config/config.env.yml')))

print(f"config={config}, type={type(config)}")

if config['logging']:
    logging.config.dictConfig(config['logging'])

config = Box(config)
log = logging.getLogger(__name__)
log.info('configuration complete!')
