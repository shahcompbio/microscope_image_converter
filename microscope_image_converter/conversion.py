import os
import sys

import pypeliner
import pypeliner.managed as mgd
import yaml


def docker_containers():
    containers = {
        'microscope_image_converter': 'microscope_image_converter:v0.0.1'
    }

    return containers


def load_yaml(path):
    try:
        with open(path) as infile:
            data = yaml.safe_load(infile)
    except IOError:
        raise Exception(
            'Unable to open file: {0}'.format(path))

    return data


def get_cell_images(path):
    data = load_yaml(path)
    data = data['cell_images']
    samples = list(data.keys())

    cfse_images = {sample: data[sample]['cfse'] for sample in samples}
    livedead_images = {sample: data[sample]['livedead'] for sample in samples}

    return samples, cfse_images, livedead_images


def conversion_workflow(args):
    docker = docker_containers()

    converted_dir = args["out_dir"]

    cell_ids, cfse_images, livedead_images = get_cell_images(args['input_yaml'])

    converted_image_template = os.path.join(converted_dir, '{cell_id}.png')

    workflow = pypeliner.workflow.Workflow(
        ctx={'docker_image': docker['microscope_image_converter']}
    )

    workflow.setobj(
        obj=mgd.OutputChunks('cell_id'),
        value=cell_ids,
    )

    workflow.transform(
        name='convert',
        func='microscope_image_converter.tasks.convert',
        axes=('cell_id',),
        args=(
            mgd.InputFile('livedead.tif', 'cell_id', fnames=livedead_images),
            mgd.InputFile('cfse.tif', 'cell_id', fnames=cfse_images),
            mgd.OutputFile('converted.png', 'cell_id', template=converted_image_template, axes_origin=[]),
        ),
    )

    converted_meta = os.path.join(converted_dir, 'metadata.yaml')
    input_yaml_blob = os.path.join(converted_dir, 'input.yaml')
    workflow.transform(
        name='generate_meta_files_results',
        func='microscope_image_converter.tasks.generate_and_upload_metadata',
        args=(
            sys.argv[0:],
            converted_dir,
            mgd.Template('converted.png', 'cell_id', template=converted_image_template),
            mgd.OutputFile(converted_meta)
        ),
        kwargs={
            'input_yaml_data': load_yaml(args['input_yaml']),
            'input_yaml': mgd.OutputFile(input_yaml_blob),
            'metadata': {
                'cell_ids': cell_ids,
                'type': 'dlp_microscope_merged',
            }
        }
    )

    return workflow


def conversion_pipeline(args):
    pyp = pypeliner.app.Pypeline(config=args)

    workflow = conversion_workflow(args)

    pyp.run(workflow)
