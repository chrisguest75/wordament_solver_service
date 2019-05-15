
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
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]

        trie.insert_words(words)
        return NoContent, 201  

def get(dictionary_id):
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]

        document = {
            "id": dictionary_id,
            "num_of_words": trie.number_of_words(),
            "longest_word_length": trie.longest_word_length()
        }

        return document, 200

def get_word(dictionary_id, word):
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]
         
    return NoContent, 200 if trie.is_word(word) else 404

def add_word(dictionary_id, word):
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]
        if trie.is_word(word):
            return NoContent, 409
        else:
            trie.insert_words([word])  
    
    return NoContent, 201

def loaded():
    return {'msg': 'ok'}, 200




