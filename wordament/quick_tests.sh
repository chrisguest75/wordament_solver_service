
curl -X POST "http://localhost:8000/api/dictionary/test" -d '["one", "two", "three"]' --header "content-type:application/json" -v

curl -X GET "http://localhost:8000/api/dictionary/test" "content-type:application/json" -v

curl -X PUT "http://localhost:8000/api/dictionary/test" -d '["wrwr", "wrwrw", "qweewe"]' --header "content-type:application/json" -v

curl -X GET "http://localhost:8000/api/dictionary/test" "content-type:application/json" -v

read -p "Enter your input here: " NUMBER
curl -X PUT "http://localhost:8000/api/dictionary/test" -d '[\"$NUMBER\"]' --header "content-type:application/json" -v

curl -X GET "http://localhost:8000/api/dictionary/test" "content-type:application/json" -v
