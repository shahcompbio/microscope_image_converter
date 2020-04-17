#!/bin/bash

REGISTRY=$1
ORG=$2
TAG=`git describe --tags`

docker build --build-arg app_version=$TAG -t $REGISTRY/$ORG/microscope_image_converter:$TAG -f docker/microscope_image_converter/dockerfile . --no-cache

docker push $REGISTRY/$ORG/microscope_image_converter:$TAG
