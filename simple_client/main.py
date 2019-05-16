#!/usr/bin/env python3
import io 
import requests

if __name__ == "__main__":
    base_url = "http://localhost:8000/api"

    with(io.open("./test_data/words_alpha.txt")) as f:
        lines = [line.rstrip() for line in f]

    total_word_count = len(lines)
    word_count = total_word_count

    word_load = False
    response = requests.get(f"{base_url}/dictionary/full")
    if response.status_code != 200:
        response = requests.post(f"{base_url}/dictionary/full", data='[]', headers={'content-type': 'application/json'})
        word_load = True
    else:
        if response.json()["num_of_words"] != total_word_count:
            word_load = True

    if word_load:
        for index in range(0, total_word_count, 1000):
            take = 1000
            if (total_word_count - index) < take:
                take = (total_word_count - index)

            wordlist = lines[index:index + take]
            words = "["
            for word in wordlist[:-1]:
                words += f'"{word}",'
            words += '"' + wordlist[-1] + '"]'

            response = requests.put(f"{base_url}/dictionary/full", data=words, headers={'content-type': 'application/json'})

        response = requests.get(f"{base_url}/dictionary/full")
        print("loaded words: " + response.json()["num_of_words"])


    grid = input("Enter grid:")
    #grid = 'GLNTSRAWRPHSEOPS'
    response = requests.get(f"{base_url}/puzzle/solve/{grid}?dictionary_id=full")
    discovered_words = response.json()
    words = list(discovered_words["words"])
    words.sort(key=len, reverse=True)

    for word in words: 
        print(word) 

