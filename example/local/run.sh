docker pull scdnaprod.azurecr.io/singlecellpipeline/microscope_image_converter:v0.0.1 && docker run -v $PWD:$PWD -w $PWD --env set-docker-credentials.env scdnaprod.azurecr.io/singlecellpipeline/microscope_image_converter:v0.0.1 microscope_image_converter --input_yaml inputs.yaml --out_dir out --loglevel DEBUG --tmpdir tmp --pipelinedir pipeline --submit local 
