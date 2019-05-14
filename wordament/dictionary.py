
from py_wordament_helper.dictionary_trie import dictionary_trie
from state_manager import state_manager_factory
from connexion import NoContent

def create(dictionary_id, words):
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        trie = dictionary_trie(words)
        sm.add("dictionaries", {dictionary_id: trie})
        return NoContent, 201  
    else:
        return NoContent, 409 

def add_words(dictionary_id, words):
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        d = sm.get("dictionaries")
        trie = d[dictionary_id]

        trie.insert_words(words)
        return NoContent, 201  

def get(dictionary_id):
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        d = sm.get("dictionaries")
        t = d[dictionary_id]

        document = {
            "num_of_words": t.number_of_words(),
            "longest_word_length": t.longest_word_length()
        }

        return document, 200

def loaded():
    return {'msg': 'ok'}, 200




