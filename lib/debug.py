from lib.db.seed import seed_database
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def debug():
    
    seed_database()
    
    
    print("=== Testing Author ===")
    author = Author.find_by_name("John Doe")
    if author:
        print(f"Author found: {author.name}")
        print("Articles:")
        for article in author.articles():
            print(f"- {article.title}")
    else:
        print("Author 'John Doe' not found!")

if __name__ == '__main__':
    debug()