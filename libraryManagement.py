import sqlite3, os
from datetime import timedelta 
from datetime import date 

current_working_directory = os.path.dirname(__file__)
conn = sqlite3.connect("{}\\LibraryManagement.db".format(current_working_directory))
query = conn.cursor()

# Function for storing borrowing history and update book status
def update():
    borrower = input("Enter your name: ")
    phone = int(input("Enter your phone number: "))
    book = input("Enter book name: ")
    isbn = input("Enter book isbn number: ")
    borrow_date = date.today()
    submit_date = borrow_date + timedelta(days=15)

    # perform task to check the book is available or not
    query.execute("SELECT book_isbn FROM book_details")
    check_isbn = query.fetchall()
    present_isbn = False

    for i in range(len(check_isbn)):
        if(isbn in check_isbn[i][0]):
            present_isbn = True

    if(present_isbn):
        query.execute("SELECT book_borrow_status FROM book_details WHERE book_isbn = {};".format(isbn))
        data = query.fetchone()

        if data[0] == "Available":
            query.execute("INSERT INTO borrowing_history(borrowername, phone_number, borrowbook, bookisbn, borrow_date, submission_date) VALUES(?, ?, ?, ?, ?, ?)", (borrower, phone, book, isbn, str(borrow_date), str(submit_date)))
            query.execute('''UPDATE book_details SET book_borrow_status = 'Not Available' WHERE book_isbn = {};'''.format(isbn))
            print("\033[1;31mBook Borrowed Successfully\033[0m")
        else:
            query.execute('''UPDATE book_details SET book_borrow_status = 'Available' WHERE book_isbn = {};'''.format(isbn))
            print("\033[1;31mBook Submited Successfully\033[0m")
    else:
        print("\033[1;31mPlease enter the correct book name or isbn number\033[0m")

    conn.commit()

# Printing book data
def bookdata():
    print("\033[1;37;44m Book Status \033[0m")
    # fetch data from database
    query.execute("SELECT * FROM book_details")
    data = query.fetchall()

    # print table column headings
    names = [description[0] for description in query.description]
    print(f"\033[1;31m{names}\033[0m")

    # print table column data
    for row in data:
        print(row)

# Printing borrower history
def borrowHistory():
    print("\033[1;37;44m Book Borrowing History \033[0m")
    # fetch data from database
    query.execute("SELECT * FROM borrowing_history")
    data = query.fetchall()

    # print table column headings
    names = [description[0] for description in query.description]
    print(f"\033[1;31m{names}\033[0m")

    # print table column data
    for row in data:
        print(row)

# function for storing data in database
def storeData(name, author, isbn):
    query.execute("INSERT INTO book_details(book_name, book_author, book_isbn, book_borrow) VALUES(?, ?, ?, ?)", (name, author, isbn,"Available"))

# Admmin login system
def adminLogin():
    print("\033[1;37;44m Admin Portal \033[0m")
    login = False
    query.execute("SELECT * FROM admin")
    data = query.fetchall()

    user = input("Enter user name: ")
    pwd = input("Enter password: ")

    for i in range(len(data)):
        # check admin password & admin user name
        if data[i][2] == pwd and data[i][1] == user:
            login = True
            cond = True
            while(cond):
                # insert book details in database
                admin_choice = int(input("\033[1;37mPress 1 for Add book details\nPress 2 for show book availabilty\nPress 3 for show book borrow details\nPress 4 for Exit\n\033[1;32mSelection: \033[0m"))
                if(admin_choice == 1):
                    name = input("Enter book name: ")
                    author = input("enter book author name: ")
                    isbn = input("Enter book isbn: ")
                    storeData(name, author, isbn)
                elif(admin_choice == 2):
                    bookdata()
                elif(admin_choice == 3):
                    borrowHistory()
                elif(admin_choice == 4):
                    cond = False
                else:
                    print("Please choose the right option")

    if(login != True):
        print("\033[1;31mInvalid Username or Password\033[0m")

# main function
def main():
    cond = True
    while(cond):
        user_choice = int(input("\033[1;37mPress 1 for Admin login\nPress 2 for see book availability\nPress 3 to brrow or submit a book\nPress 4 to for Exit\n\033[1;32mSelection: \033[0m"))
        if(user_choice == 1):
            adminLogin()
        elif(user_choice == 2):
            bookdata()
        elif(user_choice == 3):
            update()
        elif(user_choice == 4):
            cond = False
        else:
            print("Please choose the right option")

print("\033[1;37;44m Developed by Koushik Debnath \033[0m")
main()

conn.commit()
conn.close()