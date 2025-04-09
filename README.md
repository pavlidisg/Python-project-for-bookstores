# Python-project-for-bookstores
Anaconda Spyder (Python) IDE recommended in order to run this project
This is a Python project for simple bookstores digital system (consumers, admins, etc..) focusing on data managment and using .csv files as database tables.

The .csv files: books.csv, admins.csv, users.csv
These contain records without lists and dictionaries, as required by the dataframes in the program. The corresponding relationships are stored in:

categories.csv
orders.csv
favorites.csv
bookstores_admins.csv
bookstores_books.csv
ratings.csv

The .csv files: books2.csv, admins2.csv, user.csv are the complete dataframes.

The program contains a Tkinter interface, but some inputs and prints happen in the console.
Functions:
create_dfs(): Creates all required dataframes from the appropriate .csv files.

Then following functions that create .csv files from the dataframes:

Admin Functions:
admin_ui(): Called from login() if the user is an admin. Creates the admin Tkinter interface.

graphs(): Displays graphical charts. Triggered via a button in the admin_frame, created inside admin_ui().

add_book(): Lets an admin add a book. If the book already exists, nothing happens and a message is shown. If it doesn't exist dataframes are updated.
If any of the bookstores the admin tries to add the book to isn't present in the bookstores_admins_df, it's added so the admin has access.

books_admins(): Creates buttons with book titles. On the right, it shows:
Total cost of all available books per publisher/author/overall.
Each button shows a frame with that book’s details.
Admins can edit book details only if they have access to all bookstores where the book is available. They can change copy counts for bookstores they have access to.
For each book, show_rating_comments() is created and triggered by a button. It shows user ratings/comments, which admins can edit.

del_users(): Displays users by username, with a button beside each for deletion. Only the user record from user_df/users_df is deleted — associated records (orders, favorites, etc.) are not removed.

User Functions:
user_ui(): Called from login() if user is a normal user, or from register() upon sign-up. It creates the Tkinter interface for users.

apa(): Calculates how many copies of a book a user can buy based on their balance.

books():
Starts with delete_frame_widgets() to refresh the widgets.
Shows books with title, buttons to add/remove from orders/favorites, book info, and how many copies they can afford (based on balance and availability).
Defines functions to add/remove books from orders/favorites, for each book by its ID.

orders(): Triggered by a button in user_frame. Shows books in user's orders with details and a button to add comments and ratings. Includes a button to remove books from the order, similar to books().

favorites(): Similar to orders().

acc_details(): Creates a frame where users can update their account details.

recommendations():
Shows book suggestions.
Finds the most frequent category in user's favorites.
Lists all books in that category not already in orders/favorites.
Randomly selects some of the remaining books (possibly zero).
Displays them with buttons to add to favorites/orders.

Notes:
Input validation is only implemented for the password during registration.
Admins can’t add books to a bookstore unless it’s a new book.
If an admin sets copies to 0, the book is not removed from the bookstore.
comments on code are in greek.

*This project was developed as part of a course at the university
