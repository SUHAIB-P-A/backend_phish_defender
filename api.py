
# 1st
from flask import Flask, request, jsonify

# 2ed
app = Flask(__name__)

# 4th
@app.route('/api',methods=['GET'])

# 5th
def returnascii():
    d={}
    inputchar = str(request.args['query'])
    answer =str(ord(inputchar))
    d['output']=answer
    return d


# 3ed
if __name__=="__main__":
    app.run()