from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection  # Added this import

def run_queries():
    # First ensure we have some test data
    from lib.db.seed import seed_database
    seed_database()
    
    print("\n=== Running Queries ===\n")
    
    # 1. Get all articles written by a specific author
    author = Author.find_by_name("John Doe")
    if not author:
        print("Author 'John Doe' not found!")
        return
        
    print("1. Articles by John Doe:")
    for article in author.articles():
        print(f"- {article.title}")
    
    # 2. Find all magazines a specific author has contributed to
    print("\n2. Magazines John Doe has contributed to:")
    for magazine in author.magazines():
        print(f"- {magazine.name} ({magazine.category})")
    
    # 3. Get all authors who have written for a specific magazine
    magazine = Magazine.find_by_name("Tech Today")
    if not magazine:
        print("Magazine 'Tech Today' not found!")
        return
        
    print("\n3. Authors who have written for Tech Today:")
    for contributor in magazine.contributors():
        print(f"- {contributor.name}")
    
    # 4. Find magazines with articles by at least 2 different authors
    print("\n4. Magazines with articles by at least 2 authors:")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.* FROM magazines m
        JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
        HAVING COUNT(DISTINCT a.author_id) >= 2
    """)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(f"- {row['name']}")
    
    # 5. Count the number of articles in each magazine
    print("\n5. Article count per magazine:")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, COUNT(a.id) as article_count
        FROM magazines m
        LEFT JOIN articles a ON m.id = a.magazine_id
        GROUP BY m.id
    """)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(f"- {row['name']}: {row['article_count']}")
    
    # 6. Find the author who has written the most articles
    print("\n6. Author with most articles:")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, COUNT(ar.id) as article_count
        FROM authors a
        LEFT JOIN articles ar ON a.id = ar.author_id
        GROUP BY a.id
        ORDER BY article_count DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"{row['name']} with {row['article_count']} articles")
    else:
        print("No authors found")

if __name__ == '__main__':
    run_queries()