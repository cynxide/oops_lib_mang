import datetime
import os
import pickle
import random
import re
import statistics
import sys


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Available: {self.available}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.available:
                    book.available = False
                    return book
                else:
                    raise Exception("Book is already borrowed")
        raise Exception("Book not found")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.available:
                    book.available = True
                    return book
                else:
                    raise Exception("Book was not borrowed")
        raise Exception("Book not found")

    def view_books(self):
        if not self.books:
            print("No books in the library.")
            return
        sorted_books = sorted(self.books, key=lambda book: book.title)
        for book in sorted_books:
            print(book)


def get_available_books(library):
    return [book.title for book in library.books if book.available]


def get_books_by_author(library, author_name):
    return {book.isbn: book.title for book in library.books if book.author == author_name}


def save_library(library, filename):
    try:
        with open(filename, 'wb') as file:
            pickle.dump(library.books, file)
    except Exception as e:
        print(f"Error, file couldn't be saved: {e}")


def load_library(filename):
    try:
        with open(filename, 'rb') as file:
            books = pickle.load(file)
            library = Library()
            library.books = books
            return library
    except Exception as e:
        print(f"Error, file couldn't be loaded: {e}")
        return Library()


def file_exists(filename):
    return os.path.isfile(filename)


def print_python_version():
    print(f"Python version: {sys.version}")


def validate_isbn(isbn):
    pattern = re.compile(r'\d{3}-\d{10}')
    return bool(pattern.match(isbn))


def calculate_late_fee(days_late):
    return 1 * days_late


def generate_random_isbn():
    return f"{random.randint(100, 999)}-{random.randint(1000000000, 9999999999)}"


def calculate_average_borrowed_books(borrowed_books):
    return statistics.mean(borrowed_books) if borrowed_books else 0


def calculate_due_date(borrow_date, borrow_period_days):
    borrow_date = datetime.datetime.strptime(borrow_date, '%Y-%m-%d')
    due_date = borrow_date + datetime.timedelta(days=borrow_period_days)
    return due_date.strftime('%Y-%m-%d')


def main():
    filename = 'library_data.pkl'
    library = load_library(filename)

    while True:
        print('''Library Management System
        1. Add Book
        2. Borrow Book
        3. Return Book
        4. View Books
        5. Save Library
        6. Load Library
        7. Exit''')

        choice = input("Enter choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter ISBN : ")
            if not validate_isbn(isbn):
                print("Invalid ISBN format. Please use the format 'XXX-XXXXXXXXXX'.")
                continue
            library.add_book(Book(title, author, isbn))
            print(f"Book '{title}' added successfully.")

        elif choice == '2':
            isbn = input("Enter the ISBN of the book to borrow: ")
            try:
                borrowed_book = library.borrow_book(isbn)
                print(f"Book borrowed: {borrowed_book}")
            except Exception as e:
                print(e)

        elif choice == '3':
            isbn = input("Enter the ISBN of the book to return: ")
            try:
                returned_book = library.return_book(isbn)
                print(f"Book returned: {returned_book}")
            except Exception as e:
                print(e)

        elif choice == '4':
            print("Books in the library:")
            library.view_books()

        elif choice == '5':
            save_library(library, filename)
            print("Library data saved successfully.")

        elif choice == '6':
            library = load_library(filename)
            print("Library data loaded successfully.")

        elif choice == '7':
            save_library(library, filename)
            print("Library data saved.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
