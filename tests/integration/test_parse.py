from app.services.parser import GoogleShoppingParser

def test_local_parsing():
    print("Testing parser with local debug_google.html...")
    
    with open("../../debug_google.html", "r") as f:
        html = f.read()
    
    parser = GoogleShoppingParser()
    results = parser.parse(html)
    
    print(f"Found {len(results)} results:")
    for i, res in enumerate(results[:10], 1):
        print(f"{i}. {res.get('title', 'N/A')} - {res.get('price_range', 'N/A')}")
        print(f"   Link: {res.get('product_link', 'N/A')}")
        
    if not results:
        print("Still no results found. Selectors might still be incorrect.")
    else:
        print("Parsing successful!")

if __name__ == "__main__":
    test_local_parsing()
