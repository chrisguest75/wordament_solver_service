#!/usr/bin/env python3
import io 
import requests
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Redis dataload example')
    parser.add_argument('--url', default="0.0.0.0:8080/api", dest='url', type=str, help='')
    parser.add_argument('--words', default="./test_data/words_alpha.txt", dest='words', type=str, help='')

    parser.add_argument('--load-only', dest='loadonly', action='store_true')

    args = parser.parse_args()
        
    base_url = args.url 
    if 'SERVER_URL' in os.environ:
        base_url = os.environ['SERVER_URL']
    words_file = args.words         
    if 'WORDS_FILE' in os.environ:
        words_file = os.environ['WORDS_FILE']

    with(io.open(words_file)) as f:
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
        print("loaded words: " + str(response.json()["num_of_words"]))

    ############################################################
    # load
    ############################################################
    if args.loadonly == False:        
        grid = input("Enter grid:")
        #grid = 'GLNTSRAWRPHSEOPS'
        response = requests.get(f"{base_url}/puzzle/solve/{grid}?dictionary_id=full")
        discovered_words = response.json()
        words = list(discovered_words["words"])
        words.sort(key=len, reverse=True)

        for word in words: 
            print(word) 

