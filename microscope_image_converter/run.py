import argparse
import pypeliner
from microscope_image_converter.conversion import conversion_pipeline

from microscope_image_converter import __version__


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    pypeliner.app.add_arguments(parser)

    parser.add_argument('--version', action='version',
                        version='{version}'.format(version=__version__))

    parser.add_argument("--input_yaml",
                        required=True,
                        help='''yaml file with fastq files, output bams and cell metadata''')

    parser.add_argument("--out_dir",
                        required=True,
                        help='''Path to output directory.''')

    args = vars(parser.parse_args())

    return args


def main():
    args = parse_args()

    conversion_pipeline(args)


if __name__ == "__main__":
    main()
