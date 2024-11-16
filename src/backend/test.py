from db import *
from classes import *

x = Book(title="blah blah", author="me", category="moving")

y = ToRead(x.title, x.author, x.category, 'no one')
