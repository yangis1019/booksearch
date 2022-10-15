import sqlite3

# Create a database connection
conn = sqlite3.connect('books.db')

# Create a cursor
c = conn.cursor()

# Create a table
c.execute("""CREATE TABLE bookdata (
        title text,
        booknumber text,
        barcode text,
        bookshelf integer
        )""")
# Commit changes
conn.commit()

# Close connection
conn.close()