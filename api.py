
# 1st
from flask import Flask, request, jsonify, make_response
from get_result import get_resultfunc
from get_table import gettable


# 2ed
app = Flask(__name__)


# 4th
# for prediction
@app.route('/api', methods=['GET'])
# 5th
def getphishornot():
    d = {}
    d.clear()
    resString = request.args['query']
    answer = get_resultfunc(resString)
    d['output'] = answer
    return d

# get url details

# for table


@app.route('/details', methods=['GET'])
def getTabledata():
    tab = {}
    tab.clear()
    resString = request.args['query']
    table = gettable(resString)
    print(table)
    tab['tableout'] = table
    return jsonify(tab)


# 3ed
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)
