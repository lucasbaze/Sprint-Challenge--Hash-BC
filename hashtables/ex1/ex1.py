#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for x in range(0, len(weights)):
        hash_table_insert(ht, weights[x], x)

    for x in range(0, len(weights)):
        complement = limit - weights[x]
        if hash_table_retrieve(ht, complement) is not None:
            if complement >= weights[x]:
                return (hash_table_retrieve(ht, complement), x)
            else: 
                return (x, hash_table_retrieve(ht, complement))

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
