#!/usr/bin/env bash

export SERVER_URL=http://localhost:8080/api   
pushd ./simple_client
pipenv run ./main.py --load-only
popd

xdg-open http://localhost:8080/
xdg-open http://localhost:8080/api/ui/