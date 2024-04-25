
# 1st
from flask import Flask, request, jsonify, make_response
from get_result import get_resultfunc

# 2ed
app = Flask(__name__)


# 4th
@app.route('/api', methods=['GET'])
# 5th
def getphishornot():
    d = {}
    d.clear()
    resString = request.args['query']
    answer = get_resultfunc(resString)
    d['output'] = answer
    return d


# 3ed
if __name__ == "__main__":
    app.run(debug=True)
