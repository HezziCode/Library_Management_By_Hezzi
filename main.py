import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: #E0E0E0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition-duration: 0.4s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .book-card {
        background-color: #2D2D2D;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
    }
    .header {
        color: #4CAF50;
        font-weight: bold;
    }
    .subheader {
        color: #9E9E9E;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Database Connection and Initialization
def init_db():
    """Initialize the SQLite database with the books table if it doesn't exist"""
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    
    # Create books table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        year INTEGER NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def connect_db():
    """Function to establish a connection to the SQLite database"""
    return sqlite3.connect("library.db")

# Book Management Functions
def add_book(title, author, genre, year, quantity):
    """
    Function to add a new book to the database
    
    Parameters:
    - title (str): Title of the book
    - author (str): Author of the book
    - genre (str): Genre of the book
    - year (int): Publication year
    - quantity (int): Number of copies available
    """
    if not title or not author or not genre:
        st.warning("Please fill in all required fields.")
        return
        
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Insert the book into the database
        cursor.execute(
            "INSERT INTO books (title, author, genre, year, quantity) VALUES (?, ?, ?, ?, ?)",
            (title, author, genre, year, quantity)
        )
        conn.commit()
        st.success("✅ Book added successfully!")
    except sqlite3.Error as err:
        st.error(f"Error adding book: {err}")
    finally:
        conn.close()

def get_books(search_query="", search_by="all"):
    """
    Function to get books from the database with optional search filtering
    
    Parameters:
    - search_query (str): The term to search for
    - search_by (str): The field to search in (title, author, genre, all)
    
    Returns:
    - list: List of books matching the search criteria
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        if search_query:
            if search_by == "title":
                cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_query + '%',))
            elif search_by == "author":
                cursor.execute("SELECT * FROM books WHERE author LIKE ?", ('%' + search_query + '%',))
            elif search_by == "genre":
                cursor.execute("SELECT * FROM books WHERE genre LIKE ?", ('%' + search_query + '%',))
            else:  # search all fields
                cursor.execute(
                    "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?",
                    ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')
                )
        else:
            cursor.execute("SELECT * FROM books ORDER BY title")
        
        books = cursor.fetchall()
        return books
    except sqlite3.Error as err:
        st.error(f"Error retrieving books: {err}")
        return []
    finally:
        conn.close()

def remove_book(book_id):
    """
    Function to remove a book from the database
    
    Parameters:
    - book_id (int): ID of the book to remove
    """
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Delete the book from the database
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            st.success(f"❌ Book with ID {book_id} removed successfully!")
        else:
            st.warning(f"⚠️ No book found with ID {book_id}.")
    except sqlite3.Error as err:
        st.error(f"Error removing book: {err}")
    finally:
        conn.close()

def update_book_quantity(book_id, new_quantity):
    """
    Function to update the quantity of a book
    
    Parameters:
    - book_id (int): ID of the book to update
    - new_quantity (int): New quantity value
    """
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Update the book quantity
        cursor.execute("UPDATE books SET quantity = ? WHERE book_id = ?", (new_quantity, book_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            st.success(f"✅ Quantity updated for book ID {book_id}!")
        else:
            st.warning(f"⚠️ No book found with ID {book_id}.")
    except sqlite3.Error as err:
        st.error(f"Error updating book quantity: {err}")
    finally:
        conn.close()

# UI Display Functions
def display_book_card(book):
    """
    Function to display a book in a card format
    
    Parameters:
    - book (tuple): Book data (id, title, author, genre, year, quantity)
    """
    book_id, title, author, genre, year, quantity = book
    
    st.markdown(f"""
    <div class="book-card">
        <h3 class="header">{title}</h3>
        <p class="subheader">by {author}</p>
        <p><strong>Genre:</strong> {genre} | <strong>Year:</strong> {year} | <strong>Available:</strong> {quantity}</p>
        <p><strong>ID:</strong> {book_id}</p>
    </div>
    """, unsafe_allow_html=True)

# Main Application
def main():
    """Main function to display menu and perform actions"""
    # Initialize the database
    init_db()
    
    # Sidebar with logo and menu
    with st.sidebar:
        st.title("📚 Library System")
        st.markdown("---")
        
        menu = [
            "Home", 
            "Add a Book", 
            "Remove a Book", 
            "Update Quantity", 
            "Search Books"
        ]
        choice = st.selectbox("📌 Navigation", menu)
        
        st.markdown("---")
        st.markdown("### About")
        st.info("Library Management System v2.0")
        st.markdown(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Main content based on menu choice
    if choice == "Home":
        st.title("📚 Library Management System")
        st.subheader("Welcome to your digital library!")
        
        # Get all books
        books = get_books()
        
        if not books:
            st.info("📝 No books in the library yet. Add some books to get started!")
        else:
            st.subheader(f"All Books ({len(books)})")
            
            # Display books in a grid layout
            cols = st.columns(3)
            for i, book in enumerate(books):
                with cols[i % 3]:
                    display_book_card(book)

    elif choice == "Add a Book":
        st.title("📖 Add a New Book")
        
        # Create a form for adding books
        with st.form("add_book_form"):
            title = st.text_input("📌 Book Title*")
            author = st.text_input("✍️ Author Name*")
            
            col1, col2 = st.columns(2)
            with col1:
                genre = st.selectbox("🏷️ Genre*", [
                    "Fiction", "Non-Fiction", "Science Fiction", "Fantasy", 
                    "Mystery", "Thriller", "Romance", "Biography", 
                    "History", "Science", "Technology", "Self-Help", "Other"
                ])
            with col2:
                year = st.number_input("📆 Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=2020)
            
            quantity = st.number_input("📦 Quantity", min_value=1, step=1, value=1)
            
            submit_button = st.form_submit_button("➕ Add Book")
            
            if submit_button:
                add_book(title, author, genre, year, quantity)

    elif choice == "Remove a Book":
        st.title("❌ Remove a Book")
        
        # Get all books for reference
        books = get_books()
        
        if not books:
            st.info("📝 No books in the library to remove.")
        else:
            # Display books in a table for reference
            st.subheader("Current Books")
            book_df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Quantity"])
            st.dataframe(book_df, use_container_width=True)
            
            # Create a dropdown for book selection
            book_options = {f"{book[1]} by {book[2]} (ID: {book[0]})": book[0] for book in books}
            selected_book = st.selectbox("📌 Select Book to Remove", list(book_options.keys()))
            
            if st.button("❌ Remove Book"):
                remove_book(book_options[selected_book])

    elif choice == "Update Quantity":
        st.title("📦 Update Book Quantity")
        
        # Get all books for reference
        books = get_books()
        
        if not books:
            st.info("📝 No books in the library to update.")
        else:
            # Display books in a table for reference
            st.subheader("Current Books")
            book_df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Quantity"])
            st.dataframe(book_df, use_container_width=True)
            
            # Create a dropdown for book selection
            book_options = {f"{book[1]} by {book[2]} (ID: {book[0]})": book[0] for book in books}
            selected_book = st.selectbox("📌 Select Book to Update", list(book_options.keys()))
            
            # Get current quantity for the selected book
            selected_book_id = book_options[selected_book]
            current_quantity = next((book[5] for book in books if book[0] == selected_book_id), 0)
            
            new_quantity = st.number_input("📦 New Quantity", min_value=0, step=1, value=current_quantity)
            
            if st.button("✅ Update Quantity"):
                update_book_quantity(selected_book_id, new_quantity)

    elif choice == "Search Books":
        st.title("🔍 Search Books")
        
        # Search form
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Enter search term")
        with col2:
            search_by = st.selectbox("Search by", ["all", "title", "author", "genre"])
        
        if st.button("🔍 Search"):
            if search_term:
                results = get_books(search_term, search_by)
                
                if results:
                    st.subheader(f"Search Results ({len(results)})")
                    for book in results:
                        display_book_card(book)
                else:
                    st.info(f"📝 No books found matching '{search_term}' in {search_by}.")
            else:
                st.warning("⚠️ Please enter a search term.")

# Run the main function to start the program
if __name__ == "__main__":
    main()