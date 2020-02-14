#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    ht = HashTable(length)
    route = [None] * length

    # Put each ticket in the hash table by the source
    for item in tickets: 
        hash_table_insert(ht, item.source, item.destination)

    # get the first source of None
    nextDestination = hash_table_retrieve(ht, 'NONE')
    route[0] = nextDestination
    hash_table_remove(ht, 'NONE')

    # Iterate through the rest
    for x in range(1, length - 1):
        route[x] = hash_table_retrieve(ht, nextDestination)
        nextDestination = hash_table_retrieve(ht, nextDestination)

    return [x for x in route if x is not None]

