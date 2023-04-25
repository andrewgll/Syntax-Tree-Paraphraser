from flask import Flask, jsonify, request
import nltk
from nltk.tree import ParentedTree
from itertools import permutations, product
from paraphraser import *

app = Flask(__name__)

@app.route('/paraphrase', methods=['GET'])
def paraphrase():
    tree = request.args.get('tree')
    limit_string = request.args.get('limit')
    limit = int(limit_string) if limit_string is not None else -1
    if not tree:
        return jsonify({'error': 'Syntax tree parameter is required.'}), 400
    try:
        tree = nltk.tree.Tree.fromstring(tree)
        ptree = ParentedTree.convert(tree)
    except ValueError as e:
        return jsonify({'error': 'Error parsing syntax tree: {}'.format(str(e))}), 400
    
    
    paraphraser = Paraphraser(ptree,  NPPattern(),SimpleSerializator(),CartesianPermutator(), limit) 
    result = paraphraser.apply()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
