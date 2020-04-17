'''
Created on Jun 6, 2018

@author: dgrewal
'''
import collections
import copy

import yaml
from microscope_image_converter.utils import helpers


def override_config(config, override):
    def update(d, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                d[k] = update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    if not override:
        return config

    cfg = update(config, override)

    return cfg


def get_config_params(override=None):
    input_params = {
        "cluster": "azure", "aligner": "bwa-mem", "refdir": None,
        "reference": "grch37", "smoothing_function": "modal",
        "bin_size": 500000, "copynumber_bin_size": 1000,
        'memory': {'high': 16, 'med': 6, 'low': 2},
        'version': None
    }

    input_params = override_config(input_params, override)

    return input_params


def write_config(params, filepath):
    with open(filepath, 'w') as outputfile:
        yaml.safe_dump(params, outputfile, default_flow_style=False)


def containers(version=None):
    if not version:
        version = helpers.get_version()
        version = 'v'+version

    docker_images = {
        'microscope_image_converter': 'microscope_image_converter:{}'.format(version),
    }

    return {'docker': docker_images}


def get_convert_params(version):
    docker_containers = containers(version)['docker']
    docker_containers = {
        'microscope_image_converter': docker_containers['microscope_image_converter'],
    }

    params = {
        'docker': docker_containers,
        'memory': {'med': 6},
    }

    return {"convert": params}


def get_microscope_image_converter_pipeline_config(config_params, override=None):
    version = config_params['version']
    cluster = config_params["cluster"]

    params = {}

    params.update(get_convert_params(version))

    params = override_config(params, override)

    return params
