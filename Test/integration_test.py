import sqlite3
from path_fix import resource_path
from Backend.BooksTable import BooksTable

#Tests covering how multiple functions work together
class Test_Reviews():

  #Review functions from BooksTable are tested here since add & edit review
  #need fetch review to know if they worked correctly

  #Test covering add_review(book_id, review_score, review_text), &
  #fetch_review_info(id_filter=None,limit=None)
  def test_add_review(self):
    books = BooksTable()
    book_id = 52
    books.add_review(book_id, 8, "Good book")
    #the first parameter is book_id, so using it means only 1 book is returned
    rows = books.fetch_review_info(book_id, 10)
    assert rows == [{"book_id": 52, "score": 8, "text": "Good book"}]

  #Test covering edit_review(book_id, review_score, review_text), &
  #fetch_review_info(id_filter=None,limit=None)
  def test_edit_review(self):
    #Have this part here since pytest doesn't like classes with init function
    # Initialize connection to the database file
    self.db_path = resource_path('Backend/Books_Database/BooksDatabase.db')
    self.conn = sqlite3.connect(self.db_path,check_same_thread=False)
    self.conn.row_factory = sqlite3.Row  # This allows column access by name

    books = BooksTable()
    book_id = 52
    books.edit_review(book_id, 10, "Amazing book")
    #the first parameter is book_id, so using it means only 1 book is returned
    rows = books.fetch_review_info(book_id, 10)
    assert rows == [{"book_id": 52, "score": 10, "text": "Amazing book"}]

    with self.conn:
      cursor = self.conn.cursor()
      query = "DELETE FROM REVIEWS WHERE book_id = ?"
      param = [book_id]
      cursor.execute(query, param)