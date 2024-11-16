from db import *
from classes import *

x = Book(title="blah blah", author="me", category="moving")

validate_new_entry("./data/books.csv", x.book_id, x.title)

insert_to_local_table(x, "books")

y = x.add_to_reading_list()

# validate_new_entry("./data/reading_list.csv", x.book_id, x.title)

y.finish()

# validate_new_entry("./data/finished.csv", x.book_id, x.title)