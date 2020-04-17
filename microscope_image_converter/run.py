import sys

from microscope_image_converter.conversion import conversion_pipeline
from microscope_image_converter.clean_sentinels import clean_sentinels
from microscope_image_converter.cmdline import parse_args
from microscope_image_converter.docker_run import run_with_docker
from microscope_image_converter.generate_config import generate_config


def main():
    args = parse_args()

    if args["which"] == "generate_config":
        generate_config(args)
        return

    if args["which"] == "clean_sentinels":
        clean_sentinels(args)
        return

    if args["run_with_docker"]:
        run_with_docker(args, sys.argv)
        return

    if args["which"] == "convert":
        conversion_pipeline(args)


if __name__ == "__main__":
    main()
