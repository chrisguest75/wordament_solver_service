# README.md
This is a simple Restful service that integrates the Wordament Solver.  

# TODO
* Metrics for endpoints from health endpoint
* Logging
* It relies on a singleton which stops tests from working properly
* Does it make sense to pass wordlist as array rather than {[]}
* Run tests in cloudbuild
* Deploy to endpoints and kubernetes

# Usage
To host you can use the docker-compose file. 

```
docker-compose up --build
```

Browse to http://localhost:8000/api/ui

# Debugging and Unittests
You can use VSCode to load and execute the tests. Use 'pipenv install --dev'


# Testing 
You can use curl commands.  Or there is a file in the wordament [./wordament/quick_endpoint_tests.sh](./wordament/quick_endpoint_tests.sh)
```
curl http://localhost:8000/api/health
curl http://localhost:8000/api/wordament

curl -X POST http://localhost:8000/api/dictionary/test -d '[]' --header "content-type:application/json"

curl -X GET http://localhost:8000/api/dictionary/test --header "content-type:application/json"

```

