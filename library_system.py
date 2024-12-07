import os
import json

# File to store books
BOOKS_FILE = "books.json"
USERS_FILE = "users.json"


# Load or initialize data
def load_data(filename, default):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return default


# Save data
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# Initialize books and users data
books = load_data(BOOKS_FILE, [])
users = load_data(USERS_FILE, {})


# Add a new book
def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter book author: ").strip()
    copies = int(input("Enter number of copies: "))
    book_id = str(len(books) + 1)
    books.append({"id": book_id, "title": title, "author": author, "copies": copies})
    save_data(BOOKS_FILE, books)
    print(f"Book '{title}' by {author} added successfully.\n")


# Display all books
def view_books():
    if not books:
        print("No books in the library.\n")
        return
    print("\n--- Library Books ---")
    for book in books:
        print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Copies: {book['copies']}")
    print()


# Borrow a book
def borrow_book():
    user_id = input("Enter your User ID: ").strip()
    book_id = input("Enter the Book ID to borrow: ").strip()

    for book in books:
        if book["id"] == book_id:
            if book["copies"] > 0:
                book["copies"] -= 1
                users.setdefault(user_id, []).append(book_id)
                save_data(BOOKS_FILE, books)
                save_data(USERS_FILE, users)
                print(f"You have borrowed '{book['title']}'.\n")
                return
            else:
                print("Sorry, this book is out of stock.\n")
                return
    print("Invalid Book ID. Please try again.\n")


# Return a book
def return_book():
    user_id = input("Enter your User ID: ").strip()
    if user_id not in users or not users[user_id]:
        print("You have no borrowed books.\n")
        return

    print("Your borrowed books:")
    for book_id in users[user_id]:
        book = next((b for b in books if b["id"] == book_id), None)
        if book:
            print(f"ID: {book['id']}, Title: {book['title']}")

    book_id = input("Enter the Book ID to return: ").strip()
    if book_id in users[user_id]:
        book = next((b for b in books if b["id"] == book_id), None)
        if book:
            book["copies"] += 1
            users[user_id].remove(book_id)
            save_data(BOOKS_FILE, books)
            save_data(USERS_FILE, users)
            print(f"You have returned '{book['title']}'.\n")
            return
    print("Invalid Book ID or not borrowed by you.\n")


# Main menu
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            print("Exiting Library System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main_menu()
