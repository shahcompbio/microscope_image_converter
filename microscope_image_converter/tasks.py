import os
import re

import numpy as np
import skimage
import skimage.io
import yaml

import microscope_image_converter


def convert(red_path, cyan_path, output_path):
    red = skimage.io.imread(red_path)
    red_adj = skimage.exposure.rescale_intensity(red, out_range=(0, 255)).astype('uint8')

    cyan = skimage.io.imread(cyan_path)
    cyan_adj = skimage.exposure.rescale_intensity(cyan, out_range=(0, 255)).astype('uint8')

    zero_array = np.zeros(cyan_adj.shape).astype('uint8')

    reshaped = np.dstack((red_adj, cyan_adj, zero_array))

    skimage.io.imsave(output_path, reshaped, format='png')


class InputException(Exception):
    pass


def get_version():
    version = microscope_image_converter.__version__
    # strip setuptools metadata
    version = version.split("+")[0]
    return version


def generate_and_upload_metadata(
        command, root_dir, filepaths, output, template=None,
        input_yaml_data=None, input_yaml=None, metadata={}, type=None
):
    if not metadata:
        metadata = {}

    if isinstance(filepaths, dict):
        filepaths = filepaths.values()
    filepaths = list(filepaths)

    metadata['command'] = ' '.join(command)
    metadata['version'] = get_version()

    if type:
        metadata['type'] = type

    if template:
        assert len(template) == 3
        instances, template_path, instance_key = template
        assert re.match('.*\{.*\}.*', template_path)
        template_path = os.path.relpath(template_path, root_dir)
        metadata['bams'] = {}
        metadata['bams']['template'] = template_path
        instances = [{instance_key: instance} for instance in instances]
        metadata['bams']['instances'] = instances

    if input_yaml_data:
        if not input_yaml:
            raise InputException("missing yaml file to write to")
        with open(input_yaml, 'wt') as yaml_writer:
            yaml.safe_dump(input_yaml_data, yaml_writer)

        if not input_yaml.startswith(root_dir) and root_dir in input_yaml:
            input_yaml = input_yaml[input_yaml.index(root_dir):]
            if input_yaml.endswith('.tmp'):
                input_yaml = input_yaml[:-4]

        metadata['input_yaml'] = os.path.relpath(input_yaml, root_dir)
        filepaths.append(input_yaml)

    generate_meta_yaml_file(
        output, filepaths=filepaths, metadata=metadata, root_dir=root_dir
    )


def generate_meta_yaml_file(
        metadata_file,
        filepaths=None,
        metadata=None,
        root_dir=None
):
    if not root_dir:
        final_paths = filepaths
    else:
        final_paths = []
        for filepath in filepaths:
            if not filepath.startswith(root_dir):
                error = 'file {} does not have {} in path'.format(
                    filepath, root_dir
                )
                raise Exception(error)

            filepath = os.path.relpath(filepath, root_dir)
            final_paths.append(filepath)

    metadata = {
        'filenames': final_paths,
        'meta': metadata,
    }

    with open(metadata_file, 'w') as output:
        yaml.safe_dump(metadata, output, default_flow_style=False)
