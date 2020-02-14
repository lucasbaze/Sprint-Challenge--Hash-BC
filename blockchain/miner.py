import hashlib
import requests
import math
import sys

from uuid import uuid4

from timeit import default_timer

import random
from threading import Timer as setTimeout


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = default_timer()

    print("Searching for next proof")
    proof = math.floor(random.random() * 1000000)

    # Hash the last proof
    last_hash = hashlib.sha256(f"last_proof".encode()).hexdigest()

    while not valid_proof(last_hash, proof):
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(default_timer() - start))    
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    new_proof = hashlib.sha256(f"{proof}".encode()).hexdigest()

    return last_hash[-6:] == new_proof[:6]



if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        def get_last_proof():
            r = requests.get(url=node + "/last_proof")
            data = r.json()
            return data.get('proof')

        last_proof = get_last_proof()

        def check_if_lost(proof):
            new_r = requests.get(url=node + "/last_proof")
            new_data = new_r.json()
            if not new_data['proof'] == proof:
                last_proof = new_data['proof']
                print('Checked')
                return

        timer = setTimeout(2, check_if_lost, args=(last_proof,))
        timer.start()

        new_proof = proof_of_work(last_proof)

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))

        