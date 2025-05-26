import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture
def setup_db():
    # Initialize database schema
    conn = get_connection()
    cursor = conn.cursor()
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    
    # Create test data
    author = Author("Test Author")
    author.save()
    
    magazine = Magazine("Test Magazine", "Test Category")
    magazine.save()
    
    article = Article("Test Article", author.id, magazine.id)
    article.save()
    
    yield
    
    # Clean up
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_author_save(setup_db):
    author = Author("New Author")
    author.save()
    assert author.id is not None

def test_author_find_by_id(setup_db):
    author = Author.find_by_name("Test Author")
    found = Author.find_by_id(author.id)
    assert found.name == "Test Author"

def test_author_articles(setup_db):
    author = Author.find_by_name("Test Author")
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_db):
    author = Author.find_by_name("Test Author")
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Test Magazine"