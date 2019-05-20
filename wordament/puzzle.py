
from py_wordament_helper.wordament_helper import wordament_helper
from py_wordament_helper.dictionary_trie import dictionary_trie
from state_manager_factory import state_manager_factory
from connexion import NoContent
import logging

logger = logging.getLogger('wordament.rest.puzzle')

def validate_dictionary_id(id):
    return len(id) <= 40

def validate_grid(grid):
    return len(grid) == 16

def solve(grid, dictionary_id):
    logger.info("enter solve", extra={"method": "solve", "parameters": {"dictionary_id": dictionary_id, "grid": grid}})

    if not validate_dictionary_id(dictionary_id):
        return NoContent, 400

    if not validate_grid(grid):
        return NoContent, 400

    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 404  
    else:
        dictionaries = sm.get("dictionaries")
        trie = dictionaries[dictionary_id]

        helper = wordament_helper(grid, trie)
        words = helper.solve()
        output = {"words":[]}
        for word in list(words):
            output["words"].append(word)

        return output, 200
