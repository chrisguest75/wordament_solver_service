
from py_wordament_helper.wordament_helper import wordament_helper
from py_wordament_helper.dictionary_trie import dictionary_trie


def read():
    grid = 'GLNTSRAWRPHSEOPS'
    trie = dictionary_trie(["like", "shops", "shop", "wasp", "want", "hops"])

    helper = wordament_helper(grid, trie)
    words = helper.solve()
    output = {"words":[]}
    for word in list(words):
        output["words"].append(word)

    return output, 200


# def add(numbers):
#     number = numbers.get("number", None)
#     CURRENT_STORE.append(number)
#     return 201


