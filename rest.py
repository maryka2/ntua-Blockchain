import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from multiprocessing import Value

import block
import node
from blockchain import Blockchain
import wallet
# import transaction


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

app = Flask(__name__)
CORS(app)
blockchain = Blockchain()

N = 5   #Number of nodes i  the system
nodeCount = Value('i', 0)
#.......................................................................................



# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    if request is None:
        return "Error: Please supply a valid Node", 400
    data = request.json
    if data is None:
        return "Error: Please supply a valid Node", 400
    print("Add node with public_key", data["public_key"])
    with nodeCount.get_lock():
        nodeCount.value += 1
    # for node in nodes:
    #     blockchain.register_node(node)
    #
    # response = {
    #     'message': 'New nodes have been added',
    #     'total_nodes': list(blockchain.nodes),
    # }
    # return jsonify(response), 201
    return jsonify(nodeCount=nodeCount.value)

# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
