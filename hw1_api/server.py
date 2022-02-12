from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

catalog = {
            "Orwell, George": ["1984", "Animal Farm"], 
            "Bradbury, Ray": ["Fahrenheit 451"], 
            "Huxley, Aldous": ["Brave New World"], 
            "Asimov, Isaac": ["The Gods Themselves", "I, Robot", "Foundation", "The Caves of Steel"], 
            "Collins, Suzanne": ["The Hunger Games", "Catching Fire", "Mockingjay"],
            "Riordan, Rick": ["Percy Jackson & The Olympians: The Lightning Thief", "Percy Jackson & The Olympians: Sea of Monsters"],
            "Corey, James SA": ["Abaddon's Gate", "Cibola Burn", "Nemesis Games", "Babylon's Ashes", "Persepolis Rising", "Tiamat's Wrath"],
            "Tolkien, J.R.R.": ["The Hobbit", "The Silmarillion"]
          }

checkouts = {
              "John Doe": 
                    {
                        "Corey, James SA": ["Leviathan Wakes", "Calibans War"]
                    },
              "Jane Joe": 
                    {
                        "Tolkien, J.R.R.": ["The Lord of The Rings"]
                    }
            }

# returns the catalog of books that are currently able to be checked out
@app.route('/library/getCatalog',methods = ['GET'])
def getCatalog():
    return jsonify({"catalog":catalog})

# returns the list of checked out books along with the name of who checked them out
@app.route('/library/getCheckouts',methods = ['GET'])
def getCheckouts():
    return jsonify({"checkouts":checkouts})

# user checks out a book
# input json in this format:
# {
#    <user name>: 
#       {
#           <author1>: [<book1>, <book2>, etc...],
#           <author2>: [<book>, etc...],
#           etc...,
#       }
# }
#
@app.route('/library/checkoutBook',methods = ['POST'])
def checkout():
    global checkouts
    global catalog 
    books_not_checked_out = {}

    new_checkouts = request.get_json()
    for (person, query) in new_checkouts:
        if person not in checkouts:
            checkouts[person] = {}
        for (author, books) in query:
            if author in catalog:
                for book in books:
                    if book in catalog[author]:
                        if author in checkouts[person]:
                            checkouts[person][author].append(book)
                        else:
                            checkouts[person][author] = [book]
                        catalog[author].remove(book)
                        if catalog[author] == []:
                            catalog.pop(author)
                    else:
                        if author not in books_not_checked_out:
                            books_not_checked_out[author] = []
                        books_not_checked_out[author].append(book)
            else:
                if author not in books_not_checked_out:
                    books_not_checked_out[author] = []
                books_not_checked_out[author].append(book)

    return ("Available books checked out.\nBooks not checked out:\n" + jsonify({books_not_checked_out}))
            

@app.route('/library/returnBook',methods = ['POST'])
def returnBook():
    return "shit"

# user inputs json in this format:
# {
#    <author1>: [<book1>, <book2>, etc...],
#    <author2>: [<book3>, <book4>, etc...],
#    etc...
# }
@app.route('/library/donateBooks',methods = ['POST'])
def donate():
    global catalog

    # gets input json data from the request
    newBooks = request.get_json()

    # loops through the input authors and books
    for (key, value) in newBooks:
        # if author exists in catalog, append input books
        if key in catalog:
            catalog[key].extend(value)
        # if the author does not exist, create new key and append the input books
        else:
            catalog[key] = value
    # returns updated catalog
    return jsonify({"catalog":catalog})


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=7999, debug = True)