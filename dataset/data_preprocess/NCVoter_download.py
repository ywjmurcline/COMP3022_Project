import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


DOWNLOAD_FOLDER = '../download/NCVoters'

# Create download folder if it doesn't exist
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


for i in range(0,100):
    url = f"https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter{i+1}.zip"
    filename = url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    print(f"Downloading {filename}...")
    r = requests.get(url, stream=True)
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("All ZIP files downloaded.")
