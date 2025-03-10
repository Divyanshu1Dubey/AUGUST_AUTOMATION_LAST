pip install sumy
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt')

# URL of the webpage you want to scrape
URL = 'https://news.mit.edu/2021/top-research-2021-1222'

# Send an HTTP request to the URL with headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(URL, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the body content
    body_content = soup.body.get_text()

    # Summarize the content
    parser = PlaintextParser.from_string(body_content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5)  # Summarize to 5 sentences

    # Print the summary
    for sentence in summary:
        print(sentence)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")