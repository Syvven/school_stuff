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

    new_checkouts = request.get_json(force=True)
    for (person, query) in new_checkouts.items():
        if query == {}:
            return "No Books Checked Out"
        for (author, books) in query.items():
            if books != [] and author != "":
                if person not in checkouts:
                    checkouts[person] = {}
                if author in catalog:
                    for book in books:
                        if author in catalog and book in catalog[author]:
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
                    books_not_checked_out[author].extend(books)

    returnString = "Available books checked out.\n\nBooks not checked out due to not existing or not being in stock:\n"
    for (author2, books2) in books_not_checked_out.items():
        returnString += author2 + ": "
        for book2 in books2:
            returnString += "\"" + book2 + "\", "
        returnString = returnString[:-2]
        returnString += "\n"
    return returnString
            
# user returns a book
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
@app.route('/library/returnBook',methods = ['POST'])
def returnBook():
    global checkouts
    global catalog
    books_not_returned = {}

    new_returns = request.get_json(force=True)
    for (person, query) in new_returns.items():
        if person == {}:
            return "No Books Returned"
        if person not in checkouts:
            return "You have no books checked out.\nPlease double check the name entered or consult the checkouts list (/library/getCheckouts)."
        else:
            for (author, books) in query.items():
                if books != [] and author != "":
                    if author not in checkouts[person]:
                        if author not in books_not_returned:
                            books_not_returned[author] = []
                        books_not_returned[author].extend(books)
                    else:
                        for book in books:
                            if author in checkouts[person]:
                                if book not in checkouts[person][author]:
                                    if author not in books_not_returned:
                                        books_not_returned[author] = []
                                    books_not_returned[author].append(book)
                                else:
                                    checkouts[person][author].remove(book)
                                    if checkouts[person][author] == []:
                                        checkouts[person].pop(author)
                                    if author not in catalog:
                                        catalog[author] = []
                                    catalog[author].append(book)
                            else:
                                if author not in books_not_returned:
                                    books_not_returned[author] = []
                                books_not_returned[author].appen(book)
        if checkouts[person] == {}:
            checkouts.pop(person)
    
    returnString = "Checked out books returned.\n\nBooks not returned due to not existing or not being checked out:\n"
    for (author2, books2) in books_not_returned.items():
        returnString += author2 + ": "
        for book2 in books2:
            returnString += "\"" + book2 + "\", "
        returnString = returnString[:-2]
        returnString += "\n"
    return returnString
    

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
    newBooks = request.get_json(force=True)

    # loops through the input authors and books
    for (author, books) in newBooks.items():
        if books != [] and author != "":
            # if author exists in catalog, append input books
            if author in catalog:
                catalog[author].extend(books)
            # if the author does not exist, create new key and append the input books
            else:
                catalog[author] = books
    # returns updated catalog
    return jsonify({"catalog":catalog})


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=7999, debug = True)



