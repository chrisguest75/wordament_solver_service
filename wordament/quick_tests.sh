#!/usr/bin/env bash -x

#export VERBOSE=-v
curl -X POST "http://localhost:8000/api/dictionary/test" -d '["one", "two", "three"]' --header "content-type:application/json" ${VERBOSE}

curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}

curl -X PUT "http://localhost:8000/api/dictionary/test" -d '["wrwr", "wrwrw", "qweewe"]' --header "content-type:application/json" ${VERBOSE}

curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}

read -p "Enter word to add to dictionary: " NUMBER
echo "Add $NUMBER"
quoted="\"$NUMBER\""

curl -X PUT "http://localhost:8000/api/dictionary/test" -d "[$quoted]" --header "content-type:application/json" ${VERBOSE}

curl -X GET "http://localhost:8000/api/dictionary/test" --header "content-type:application/json" ${VERBOSE}
