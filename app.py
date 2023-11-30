import requests
from datetime import datetime, timedelta
from configparser import ConfigParser

# Load configuration file
config = ConfigParser()
config.read('config.ini')

# Replace 'YOUR_API_KEY' with your News API key
api_key = config.get('NEWSAPI', 'api_key')

# Keywords for Bitcoin and Ethereum Mastodon search
keywords_bitcoin = ["Bitcoin", "BTC"]
keywords_ethereum = ["Ethereum", "ETH"]

# Calculate the date for yesterday
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')

# API endpoint and parameters
url = 'https://newsapi.org/v2/everything'
api_url = "http://localhost:5000/store-text"

try:

    # Function to process subreddit posts
    def search_newsapi(keywords):
        entries_to_store = []

        params = {
            'q': " OR ".join(keywords),
            'from': yesterday_str,
            'to': yesterday_str,
            'sortBy': 'popularity',
            'pageSize': 40,
            'apiKey': api_key,
        }

        # Send a GET request to the News API
        response = requests.get(url, params=params)
        data = response.json()

        # Check if the request was successful
        if response.status_code == 200:
            articles = data.get('articles', [])

            # Display the articles in the terminal
            for i, article in enumerate(articles, start=1):
                article_time = datetime.fromisoformat(article['publishedAt'])

                print(f"{i}. Author: {article['author']}")
                print(f"Title: {article['title']}")
                print(f"Text: {article['description']}")
                print(f"Date: {article_time.isoformat()}\n")
                
                entry = {
                    'user': article['author'],
                    'title': article['title'],
                    'text': article['description'],
                    'date': article_time.isoformat()
                }
                entries_to_store.append(entry)
        return entries_to_store
    
    # Function to send data to API
    def send_to_api(entries, source, keyword):
        if entries:
            data_to_send = {
                'source': source,
                'keyword': keyword,
                'entries': entries
            }
            response = requests.post(api_url, json=data_to_send)
            print(f"Status Code for {keyword}: {response.status_code}")
            print(f"Response for {keyword}: {response.json()}")
        else:
            print(f"No new relevant comments found for {keyword} in the previous day.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

# Process Bitcoin and Ethereum subreddits
btc_entries = search_newsapi(keywords_bitcoin)
send_to_api(btc_entries, 'NewsApi', 'Bitcoin')

eth_entries = search_newsapi(keywords_ethereum)
send_to_api(eth_entries, 'NewsApi', 'Ethereum')