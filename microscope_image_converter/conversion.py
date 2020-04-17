import os
import re

import pypeliner.managed as mgd
from microscope_image_converter.utils import inpututils

import pypeliner
import sys


def conversion_workflow(args):
    config = inpututils.load_config(args)
    config = config['convert']

    converted_dir = args["out_dir"]

    red_images, cyan_images, cell_ids = inpututils.get_cell_images(args['input_yaml'])

    converted_image_template = os.path.join(converted_dir, '{cell_id}.png')

    converted_meta = os.path.join(converted_dir, 'metadata.yaml')

    input_yaml_blob = os.path.join(converted_dir, 'input.yaml')

    workflow = pypeliner.workflow.Workflow(
        ctx={'docker_image': config['docker']['microscope_image_converter']}
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
            mgd.InputFile('red.tif', 'cell_id', fnames=red_images),
            mgd.InputFile('cyan.tif', 'cell_id', fnames=cyan_images),
            mgd.OutputFile('converted.png', 'cell_id', template=converted_image_template, axes_origin=[]),
        ),
    )

    workflow.transform(
        name='generate_meta_files_results',
        func='microscope_image_converter.utils.helpers.generate_and_upload_metadata',
        args=(
            sys.argv[0:],
            converted_dir,
            mgd.Template('converted.png', 'cell_id', template=converted_image_template),
            mgd.OutputFile(converted_meta)
        ),
        kwargs={
            'input_yaml_data': inpututils.load_yaml(args['input_yaml']),
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
