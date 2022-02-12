from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

catalog = {
            "Orwell, George": ["1984", "Animal Farm"], 
            "Bradbury, Ray": ["Fahrenheit 451"], 
            "Huxley, Aldous": ["Brave New World"], 
            "Asimov, Isaac": ["The Gods Themselves", "I, Robot", "Foundation", "The Caves of Steel"], 
            "Collins, Suzanne": ["The Hunger Games", "Catching Fire", "Mockingjay"],
            "Riordan, Rick": ["Percy Jackson & The Olympians: The Lightning Thief", "Percy Jackson & The Olympians: Sea of Monsters"]
          }

checkouts = []  

@app.route('/library/getCatalog',methods = ['GET'])
def getCatalog():
    return jsonify({"catalog":catalog});

@app.route('/library/getCheckouts',methods = ['GET'])
def getCheckouts():
    return jsonify({"checkouts":checkouts});

@app.route('/library/checkoutBook',methods = ['POST'])
def checkout():
    return "piss"

# @app.route('/library/returnBook',methods = ['POST'])
# def returnBook():
#     global balance
#     transaction = request.get_json()
#     transaction["type"] = "withdraw"
#     transaction["time"] = datetime.now()
#     balance = balance - transaction["amount"]
#     transactions.append(transaction)
#     return jsonify({"balance":balance});

# @app.route('/library/donateBook',methods = ['POST'])
# def donate():
    

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=7999, debug = True)