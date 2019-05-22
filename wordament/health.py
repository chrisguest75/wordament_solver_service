from state_manager_factory import state_manager_factory
from connexion import NoContent
import logging

logger = logging.getLogger('wordament.rest.health')

def health():
    logger.info("enter health", extra={"method": "health"})

    sm = state_manager_factory.create()
    if not sm.exists("dictionaries"):
        return NoContent, 200  
    else:
        dictionaries = sm.get("dictionaries")
        names = dictionaries.keys()
        output = {"dictionaries":{}}
        for name in list(names):
            trie = dictionaries[name]
            document = {
                "id": name,
                "num_of_words": trie.number_of_words(),
                "longest_word_length": trie.longest_word_length()
            }

            output["dictionaries"][name] = document

        return output, 200
