# README.md
This is a simple Restful service that integrates the Wordament Solver.  

The words alpha has been sourced from [words_alpha.txt](https://github.com/dwyl/english-words/blob/master/words_alpha.txt)

# TODO
* Run tests in cloudbuild
* Fix data input validation
* Add comments to the code
* Think about how to persist state maybe in redis and mysql.
* Performance analysis - correlationids, open tracing.  
* Metrics for endpoints from health endpoint
* Does it make sense to pass wordlist as array rather than {[]}
* Deploy to endpoints and kubernetes

# Usage
To host you can use the docker-compose file. 

```
docker-compose up --build
```

Browse to http://localhost:8000/api/ui

# Debugging and Unittests
You can use VSCode to load and execute the tests. Use 'pipenv install --dev'

# Code Coverage
```
pytest --cov=. --cov-report html:coverage
open ./coverage/index.html 
```

# Testing 
You can use curl commands.  Or there is a file in the wordament [./wordament/quick_endpoint_tests.sh](./wordament/quick_endpoint_tests.sh)
```
curl http://localhost:8000/api/health
curl http://localhost:8000/api/wordament

curl -X POST http://localhost:8000/api/dictionary/test -d '[]' --header "content-type:application/json"

curl -X GET http://localhost:8000/api/dictionary/test --header "content-type:application/json"

```

# Test CloudBuild
```
gcloud builds submit --project open-source-01 --substitutions=COMMIT_SHA=test,BRANCH_NAME=master,REPO_NAME=wordament_solver_service
```

# Development using skaffold
I'm currently using this on Docker for Mac.

* Enable kubernetes on Docker for Mac. 
* Switch to the docker-for-desktop kubectl context 
* Ensure skaffold v0.30.0 is installed. 

NOTE: The "imagePullPolicy: Never" means we use the local image registry. 

```
cd ./wordament
skaffold dev --profile=testlocaldockerk8s --no-prune
```

# Debugging using skaffold and VSCode
If you want to live debug the service from VSCode you can run Skaffold with port-forwarding.

```
cd ./wordament
skaffold dev --profile=testlocaldockerk8s --no-prune --port-forward
```

You'll need to change the manifests in ./k8s to ensure the DEBUGGER is enabled.  
If you'd like to wait for the debugger to attach then also set WAIT to True. 

```
    env:
      - name: DEBUGGER
        value: "True"
      - name: WAIT
        value: "False"
```

Your .vscode config should look something like this. 
```
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "localhost",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        },
```