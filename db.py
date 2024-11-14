import duckdb

def get_duckdb():
    return duckdb.connect('./database.db')

def query_db(query: str):
    duckdb.sql(query).show()

def create_books_table():
    duckdb.execute(
        """CREATE OR REPLACE TABLE books (
            id int primary key NOT NULL,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(50),
            year INT,
            category VARCHAR(20)
            )
        """
    )

# get_duckdb()
create_books_table()
query_db("SELECT * FROM books")