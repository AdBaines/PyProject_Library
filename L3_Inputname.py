class Author: #Author template
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.books = []  # List to store the books written by the author

    def __repr__(self):
        return f'{self.name}-{self.age}' # Returns the authors Name and Age

    def display_books(self):
        if self.books:
            print(f"Books by {self.name}:") # This will print the books aslong as self.books is not empty
            for book in self.books:
                print(f"- {book.title} ({book.year})")
        else:
            print(f"No books found for {self.name}")


class Book: # Book template
    def __init__(self, title, year, authors=None):
        self.title = title
        self.year = year
        if authors is None:
            self.authors = []  # List to store the authors of the book
        else:
            self.authors = authors

    @property # The @property decorator allows accessing the authors attribute as if it were a regular attribute, rather than a method.
    def authors(self):
        return self._authors # This line defines a property called authors

    @authors.setter
    def authors(self, new_authors):
        for a in new_authors:
            if not isinstance(a, Author):
                raise TypeError
            else:
                a.books.append(self)  # Add the book to the author's list of books
        self._authors = new_authors

    def __repr__(self):
        return f'{self.title}-{self.year}'


class Library: # Library template
    def __init__(self):
        self.books = []  # List to store all the books in the library

    def add_book(self, title, year, authors):
        new_book = Book(title, year, authors)
        self.books.append(new_book)  # Add the book to the library
        self.save_book(new_book)  # Save the book to the file

    def save_book(self, book):
        with open("library.txt", "a") as file:
            file.write(f"{book.title},{book.year},{','.join([author.name for author in book.authors])}\n")
            # Write the book details to the library file in a comma-separated format

    def load_books(self):
        try:
            with open("library.txt", "r") as file:
                for line in file:
                    book_info = line.strip().split(',')
                    title = book_info[0]
                    year = int(book_info[1])
                    author_names = book_info[2:]
                    authors = [Author(name, None) for name in author_names]
                    new_book = Book(title, year, authors)
                    self.books.append(new_book)
                    # Load books from the library file and add them to the library
        except FileNotFoundError:
            print("Library file not found. Starting with an empty library.")


def add_book_to_library(library):
    title = input("Enter the title of the book: ")
    year = int(input("Enter the year of publication: "))

    # Collect author information
    authors = []
    author_names = input("Enter the name(s) of the author(s) (separated by commas): ").split(',')
    for name in author_names:
        author = Author(name.strip(), None)
        authors.append(author)

    # Add the book to the library
    library.add_book(title, year, authors)
    print("Book added successfully!")


def display_library(library):
    for book in library.books:
        print(f"{book.title} ({book.year})")
        print("Authors:")
        for author in book.authors:
            print(f"- {author.name}")
        print()

def check(book_title):
    with open('library.txt') as f:
        datafile = f.readlines()
    found = False
    for line in datafile:
        book_info = line.strip().split(',')
        if book_info[0] == book_title:
            found = True
            print(f"Book found: {book_info[0]} ({book_info[1]})")
            authors = book_info[2:]
            if authors:
                print("Authors:")
                for author_name in authors:
                    print(f"- {author_name}")
            else:
                print("No authors listed for this book.")
            break

    if not found:
        print(f"Book with title '{book_title}' not found in the library.")


def main():
    library = Library()
    library.load_books()  # Load existing books from the library file, if available

    while True:
        print("Library Menu:")
        print("1. Add a book")
        print("2. Display library")
        print("3. Individual Search for books")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_book_to_library(library)
        elif choice == "2":
            display_library(library)
        elif choice == "3":
            book_title = input("Enter the title of the book to search: ")
            check(book_title)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
