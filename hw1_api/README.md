# Library (Using Python Flask)

## Description

My Library API makes use of Python Flask in order to implement a simple library.
There are no actual books stored, it is just a simulation of a library, however, 
other useful functions could be implemented such as a library card, or links to pdfs
of books being checked out when checking out books.
As it is now, the user can:
- View the catalog of available books
- Add new books to the catalog
- Checkout books existing in the catalog
- View who has what books checked out
- Return books the user has checked out

## Pre-Requisites

- [Python](https://www.python.org/)

- Flask

>Install Flask with 
>
>```
>pip install --no-cache-dir -r requirements.txt
>```

#### or

 - Docker

#### or 

- SSH/CSE Labs Machine Access

## Running The Library

### Running via Command Line

Run the `server.py` file in the command line by typing

```
python server.py
```

Then use Postman, CURL, or another program to call the available functions

### Running via Docker

Build the image using

```
 docker build -t syven/hw1_api .
```

Then run the image using

```
 docker run -p 127.0.0.1:7999:7999 -it syven/hw1_api
```

### Running via Singularity on CSE Labs Machines

SSH into a CSE labs machine with the correct port using

```
% ssh -L 7999:127.0.0.1:7999 <x500>@<machine>.cselabs.umn.edu
```

Pull the docker image using

```
% singularity pull docker://syven/hw1_api
```

Then run the image using

```
% singularity run docker://syven/hw1_api
```

---

*Side Note: singularity takes up a lot of space on the Labs Machines. You are almost guaranteed to 
go over your quota (~1.5 GB)
In order to minimize the impact, once you are done running the docker image, input into the command line.*

```
% rm -rf *.sif
```

*followed by*

```
% singularity cache clean
```

*to return your space usage to what it was before pulling and running the docker image.
This will make your life much easier and will avoid unnecessary errors when sshing.*

## Available Functions

- GET → http://127.0.0.1:7999/library/getCatalog
    - returns the catalog of available authors and their books
    - authors ordered by last name
- GET → http://127.0.0.1:7999/library/getCheckouts
    - returns a list of who has checked out books and which books they have checked out
- POST → http://127.0.0.1:7999/library/checkoutBook
    - allows the user to check out books
    - input should be as such, each element being a string:

>```
>// these comments should not be included in the input
>// each entry should be a string
>// author name is ordered such: "lastname, firstname middleinitial"
>// eg. J.R.R. Tolkien should be entered as "Tolkien, J.R.R."
>// each book must have an author (no empty string)
>// each author must have at least 1 book "no empty list"
>// each person must have at least 1 author and 1 book (no empty dictionary)
>// user does not need to have already checked out a book
>// any book that does not exist will not be checked out
>// each string must be exactly the same as the author/book/person shown in the catalog/checkouts
>// if you wish to know how which books are available, consult /library/getCatalog or /library/getCheckouts
>// if you wish to checkout for two people, you may do so, however, it wouldnt make logical sense
>{
>     <user-name1>: 
>        {
>             <author1>: [<book1>, <book2>, etc...], 
>             <author2>: [<book3>, <book4>, etc...], 
>             etc...
>        },
>     <user-name2>: 
>        { 
>             etc...
>        }
>}
>```

- POST → http://127.0.0.1:7999/library/returnBook
    - allows user to return books they have checked out
    - inputs should be as such, each element being a string:

>```
>// these comments should not be included in the input
>// each entry should be a string
>// author name is ordered such: "lastname, firstname middleinitial"
>// eg. J.R.R. Tolkien should be entered as "Tolkien, J.R.R."
>// each book must have an author (no empty string)
>// each author must have at least 1 book "no empty list"
>// each person must have at least 1 author and 1 book (no empty dictionary)
>// user needs to have already checked out a book
>// any book that does not exist or was not checked out will not be returned
>// each string must be exactly the same as the author/book/person shown in the person's checkouts
>// if you wish to know how which books you checked out, consult /library/getCheckouts
>// if you wish to return for two people, you may do so, however, it wouldnt make logical sense
>{
>     <user-name1>: 
>        {
>             <author1>: [<book1>, <book2>, etc...], 
>             <author2>: [<book3>, <book4>, etc...], 
>             etc...
>        },
>     <user-name2>: 
>        { 
>             etc...
>        }
>}
>```

- POST → http://127.0.0.1:7999/library/donateBooks
    - allows the user to donate, or add, new books and authors to the catalog
    - returns catalog with new books added
    - input should be as follows, each element a string:

>```
>// these comments should not be included in the input
>// each entry should be formatted as a string
>// author name is ordered such: "lastname, firstname middleinitial"
>// eg. J.R.R. Tolkien should be entered as "Tolkien, J.R.R."
>// each book must have an author (no empty string)
>// each author must have at least 1 book "no empty list"
>// you may donate books that are already in the catalog -- cant have enough books
>// be sure to double check spelling of book/author name -- will be inserted in the catalog even with spelling errors
>{
>        <author1>: [<book1>, <book2>, etc...], 
>        <author2>: [<book3>, <book4>, etc...], 
>        etc...
>}
>```

## Bugs / Suggestions

*If you run into any bugs or issues while using the API, or want to suggest any features, feel free to comment at [the github repository](https://github.com/Syvven/school_stuff)
or [email me](hend0800@umn.edu) directly.* 

*I hope that you enjoy this little library simulation!*


