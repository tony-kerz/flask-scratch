import os
import logging
import logging.config
import yaml
import re
from functools import reduce
from box import Box

env = os.getenv('PY_ENV') or 'default'
print(f"env={env}")

# https://stackoverflow.com/a/27232341/2371903
# pattern = re.compile(r'{{(.*)}}')
# pattern = re.compile( r'^\<%= ENV\[\'(.*)\'\] %\>(.*)$' )
# yaml.add_implicit_resolver ( "!pathex", pattern )
#
# def pathex_constructor(loader,node):
#     value = loader.construct_scalar(node)
#     print(f"env-ctor: value={value}, node={node}")
#     env_var, remaining_path = pattern.match(value).groups()
#     return os.environ[env_var] + remaining_path
#
# yaml.add_constructor('!pathex', pathex_constructor)

def dict_if(file):
    if os.path.isfile(file):
        print(f"found {file}")
        return yaml.load(open(file))

# https://stackoverflow.com/a/20666342/2371903
# will overwrite v merge lists


def merge_dict(target, source):
    #print(f"target={target}, source={source}")
    target = target or {}
    if source:
        for key, value in source.items():
            if isinstance(value, dict):
                node = target.setdefault(key, {})
                merge_dict(node, value)
            elif value != None:
                target[key] = value
    return target


def env_dict(target):
    def reducer(result, key):
        val = target[key]
        # print(f"result={result}, key={key}, val={val}")
        result[key] = env_dict(val) if isinstance(
            val, dict) else os.getenv(val)
        return result
    result = reduce(reducer, target.keys(), {})
    return result


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
