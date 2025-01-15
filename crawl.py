import requests
from bs4 import BeautifulSoup
import os

def veriCekYaz(url, title, file_path):
    print("Veriler Çekiliyor. Lütfen bekleyin.")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        if title == "MIDDLE EAST":
            content_divs = soup.find_all('section', class_='layout__wrapper layout-no-rail__wrapper')
        else:
            content_divs = soup.find_all('div', class_='article__content')
        if not content_divs:
            content = soup.body.get_text(separator='\n', strip=True) if soup.body else "No content found"
        else:
            content = "\n\n".join([div.get_text(separator='\n', strip=True) for div in content_divs])
        if content.strip():
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"\n\n### {title}\n\n")
                file.write(content)
        else:
            print(f"No significant content found on {url}")
    else:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")

def main():
    anaHaberSitesi = "https://edition.cnn.com/world/middle-east"
    kayitDosyasi = "data.txt"
    if os.path.exists(kayitDosyasi):
        os.remove(kayitDosyasi)

    veriCekYaz(anaHaberSitesi, "MIDDLE EAST", kayitDosyasi)

    response = requests.get(anaHaberSitesi)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if 'middleeast' in href: 
                if href.startswith("https://edition.cnn.com"):
                    links.append(href)
                elif href.startswith("/"):
                    links.append(f"https://edition.cnn.com{href}")

        links = list(set(links))

        for link in links:
            page_response = requests.get(link)
            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.content, 'html.parser')
                title = page_soup.find('title').get_text(strip=True) if page_soup.find('title') else "No Title"
                veriCekYaz(link, title, kayitDosyasi)
            else:
                print(f"Bu sayfaya erisilemedi: {link}")
    else:
        print(f"Ana sayfaya erisilemedi: {response.status_code}")

main()
