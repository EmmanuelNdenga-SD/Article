
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    
    conn = get_connection()
    cursor = conn.cursor()
    
    
    cursor.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
        DELETE FROM sqlite_sequence;
    """)
    
    
    authors = [
        Author("John Doe"),
        Author("Jane Smith"),
        Author("Bob Johnson")
    ]
    for author in authors:
        author.save()
    
    
    magazines = [
        Magazine("Tech Today", "Technology"),
        Magazine("Science Weekly", "Science"),
        Magazine("Business Insights", "Business")
    ]
    for magazine in magazines:
        magazine.save()
    
    
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