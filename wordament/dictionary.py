
from py_wordament_helper.dictionary_trie import dictionary_trie
from state_manager_factory import state_manager_factory
from connexion import NoContent
import logging

logger = logging.getLogger('wordament.rest.dictionary')

def validate_dictionary_id(id):
    return len(id) <= 40

def get_names():
    logger.info("enter get_names", extra={"method": "get_names"})
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return {"names":[]}, 200  
    else:
        dictionaries = sm.get("dictionaries")
        names = list(dictionaries.keys())

        return {"names":names}, 200

def create(dictionary_id, words):
    logger.info("enter create", extra={"method": "create", "parameters": {"dictionary_id": dictionary_id, "words": len(words)}})
    if not validate_dictionary_id(dictionary_id):
        return NoContent, 400

    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        trie = dictionary_trie(words)
        sm.add("dictionaries", {dictionary_id: trie})
        return NoContent, 201  
    else:
        dictionaries = sm.get("dictionaries")
        if dictionary_id in dictionaries:
            return NoContent, 409 
        else:
            trie = dictionary_trie(words)
            sm.add("dictionaries", {dictionary_id: trie})
            return NoContent, 201  


def add_words(dictionary_id, words):
    logger.info("enter add_words", extra={"method": "add_words", "parameters": {"dictionary_id": dictionary_id, "words": len(words)}})
    if not validate_dictionary_id(dictionary_id):
        return NoContent, 400
        
    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]

        trie.insert_words(words)
        return NoContent, 201  

def get(dictionary_id):
    logger.info("enter get", extra={"method": "get", "parameters": {"dictionary_id": dictionary_id}})
    if not validate_dictionary_id(dictionary_id):
        return NoContent, 400

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
    logger.info("enter get_word", extra={"method": "get_word", "parameters": {"dictionary_id": dictionary_id, "word": word}})

    if not validate_dictionary_id(dictionary_id):
        return NoContent, 400

    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]

    document = {
        "dictionary_id": dictionary_id,
        "word": word,
        "exists": True
    }
  
    return document, 200 if trie.is_word(word) else 404

def add_word(dictionary_id, word):
    logger.info("enter add_word", extra={"method": "add_word", "parameters": {"dictionary_id": dictionary_id, "word": word}})

    if not validate_dictionary_id(dictionary_id):
        return NoContent, 400

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




