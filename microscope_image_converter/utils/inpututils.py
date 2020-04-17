import yaml


def load_config(args):
    return load_yaml(args["config_file"])


def load_yaml(path):
    try:
        with open(path) as infile:
            data = yaml.safe_load(infile)

    except IOError:
        raise Exception(
            'Unable to open file: {0}'.format(path))
    return data


def get_cell_images(input_yaml):
    yamldata = load_yaml(input_yaml)

    cell_images = yamldata['cell_images']

    # TODO: is this correct?
    cell_ids = list(cell_images.keys())
    livedead_images = {cell_id: cell_images[cell_id]['livedead'] for cell_id in cell_images}
    cfse_images = {cell_id: cell_images[cell_id]['cfse'] for cell_id in cell_images}

    return livedead_images, cfse_images, cell_ids


