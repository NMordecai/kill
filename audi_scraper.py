import requests
from bs4 import BeautifulSoup

def scrape_bodleian_navigation(url):
    
    try:
        # 1. Fetch the HTML content
        # Adding a User-Agent header to mimic a real browser can help avoid some blocks.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Define the target navigation texts for Bodleian Libraries
        target_texts = ["Libraries", "collections and resources", "services"]
        extracted_data = {}

        # 4. Locate elements containing the target data
        # For the Bodleian website, these main navigation links are likely within
        # specific navigation areas. We'll search for all <a> tags and filter them
        # by their text content.
        
        all_links = soup.find_all('a')
        
        for link in all_links:
            link_text = link.get_text(strip=True).lower() # Get text and convert to lowercase for case-insensitive matching
            
            # Check for exact matches of the target texts
            if link_text == "libraries":
                extracted_data["Libraries"] = link.get('href', 'No href found')
            elif link_text == "collections and resources":
                extracted_data["collections and resources"] = link.get('href', 'No href found')
            elif link_text == "services":
                extracted_data["services"] = link.get('href', 'No href found')
                
        return extracted_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Updated URL for Bodleian Libraries
    bodleian_url = "https://www.bodleian.ox.ac.uk/home"
    print(f"Attempting to scrape navigation data from: {bodleian_url}")
    data = scrape_bodleian_navigation(bodleian_url)

    if data:
        print("\nExtracted Navigation Data:")
        for key, value in data.items():
            print(f"- {key}: {value}")
    else:
        print("\nFailed to extract data.")

