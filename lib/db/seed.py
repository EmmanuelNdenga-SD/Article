# Add this import at the top of the file
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    # Clear existing data and reset auto-increment
    conn = get_connection()
    cursor = conn.cursor()
    
    # Reset database tables
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
        DELETE FROM sqlite_sequence;
    """)
    
    # Create test authors
    authors = [
        Author("John Doe"),
        Author("Jane Smith"),
        Author("Bob Johnson")
    ]
    for author in authors:
        author.save()
    
    # Create test magazines
    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Science Weekly", "Science"),
        Magazine("Business Insights", "Business")
    ]
    for magazine in magazines:
        magazine.save()
    
    # Create test articles
    articles = [
        Article("The Future of AI", authors[0].id, magazines[0].id),
        Article("Quantum Computing", authors[1].id, magazines[1].id),
        Article("Market Trends", authors[2].id, magazines[2].id)
    ]
    for article in articles:
        article.save()
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")