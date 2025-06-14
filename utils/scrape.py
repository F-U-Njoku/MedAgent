import os
import requests
import pandas as pd
from typing import List, Dict
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_medlineplus_drug(url: str) -> Dict:
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    name = soup.find("h1").text.strip()

    sections = soup.find_all("div", class_="section")

    def extract_section(title_substring):
        for section in sections:
            h2 = section.find("h2")
            if h2 and title_substring.lower() in h2.text.lower():
                return section.get_text(separator=" ", strip=True)
        return "Not found"

    return {
        "drug_name": name,
        "url": url,
        "uses": extract_section("Why is this medication prescribed?"),
        "side_effects": extract_section("What side effects"),
        "precautions": extract_section("What special precautions")
    }

def scrape_multiple_drugs(drug_urls: List[str], output_path: str = "data/medlineplus_drugs.csv"):
    os.makedirs("data", exist_ok=True)
    records = []
    for url in drug_urls:
        try:
            print(f"Scraping {url}...")
            record = scrape_medlineplus_drug(url)
            records.append(record)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
    
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False, sep=";")
    print(f"Saved scraped data to {output_path}")

if __name__ == "__main__":
    urls = [
        "https://medlineplus.gov/druginfo/meds/a696005.html",  # Metformin
        "https://medlineplus.gov/druginfo/meds/a682159.html",  # Ibuprofen
        "https://medlineplus.gov/druginfo/meds/a611014.html",  # Ceftaroline
        "https://medlineplus.gov/druginfo/meds/a611003.html",  # Liraglutide
        "https://medlineplus.gov/druginfo/meds/a699002.html",  # Diclofenac and Misoprostol 
        "https://medlineplus.gov/druginfo/meds/a604002.html",  # DAlfuzosin 
        "https://medlineplus.gov/druginfo/meds/a682145.html",  # Albuterol
        "https://medlineplus.gov/druginfo/meds/a693050.html",  # Omeprazole
        "https://medlineplus.gov/druginfo/meds/a682461.html",  # Levothyroxine
        "https://medlineplus.gov/druginfo/meds/a682277.html",  # Warfarin
        "https://medlineplus.gov/druginfo/meds/a685001.html",  # Amoxicillin
        "https://medlineplus.gov/druginfo/meds/a600045.html", # Atorvastatin
        ]
    scrape_multiple_drugs(urls)