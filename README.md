# README.md
This is a simple service that integrates the Wordament Solver.  

```
curl http://localhost:8000/api/health
curl http://localhost:8000/api/wordament
```


```
curl -X POST http://localhost:8000/api/dictionary/test -d '[]' --header "content-type:application/json"

 curl -X GET http://localhost:8000/api/dictionary/test --header "content-type:application/json"

```