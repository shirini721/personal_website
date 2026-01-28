#!/usr/bin/env python3
"""
Script to fetch publications from Google Scholar profile and generate JSON data
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

def fetch_google_scholar_publications(scholar_id, max_pages=5):
    """
    Fetch publications from Google Scholar profile
    
    Args:
        scholar_id (str): Google Scholar user ID
        max_pages (int): Maximum number of pages to fetch
    
    Returns:
        dict: Dictionary containing publications and statistics
    """
    base_url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
    publications = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        for page in range(max_pages):
            if page == 0:
                url = base_url
            else:
                url = f"{base_url}&cstart={page * 20}"
            
            print(f"Fetching page {page + 1}...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find publication entries
            pub_entries = soup.find_all('tr', class_='gsc_a_tr')
            
            if not pub_entries:
                print(f"No more publications found on page {page + 1}")
                break
            
            for entry in pub_entries:
                pub_data = parse_publication_entry(entry)
                if pub_data:
                    publications.append(pub_data)
            
            # Add delay to be respectful to Google Scholar
            time.sleep(2)
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
    # Extract statistics
    stats = extract_statistics(soup)
    
    return {
        'publications': publications,
        'statistics': stats,
        'total_publications': len(publications)
    }

def parse_publication_entry(entry):
    """
    Parse a single publication entry from Google Scholar
    
    Args:
        entry: BeautifulSoup element containing publication data
    
    Returns:
        dict: Parsed publication data
    """
    try:
        # Title and link
        title_elem = entry.find('a', class_='gsc_a_at')
        if not title_elem:
            return None
        
        title = title_elem.get_text().strip()
        link = title_elem.get('href', '')
        
        # Authors
        authors_elem = entry.find('div', class_='gs_gray')
        authors = authors_elem.get_text().strip() if authors_elem else ""
        
        # Venue and year
        venue_year_elem = entry.find('div', class_='gs_gray').find_next_sibling('div', class_='gs_gray')
        venue_year = venue_year_elem.get_text().strip() if venue_year_elem else ""
        
        # Citations
        citations_elem = entry.find('a', class_='gsc_a_c')
        citations = 0
        if citations_elem:
            citations_text = citations_elem.get_text().strip()
            citations = int(citations_text) if citations_text.isdigit() else 0
        
        # Year extraction
        year_match = re.search(r'\b(19|20)\d{2}\b', venue_year)
        year = year_match.group() if year_match else ""
        
        # Venue (remove year from venue_year)
        venue = re.sub(r'\b(19|20)\d{2}\b', '', venue_year).strip()
        venue = re.sub(r'^,\s*', '', venue)  # Remove leading comma
        
        return {
            'title': title,
            'authors': authors,
            'venue': venue,
            'year': year,
            'citations': citations,
            'link': link
        }
    
    except Exception as e:
        print(f"Error parsing publication entry: {e}")
        return None

def extract_statistics(soup):
    """
    Extract statistics from Google Scholar profile
    
    Args:
        soup: BeautifulSoup object of the profile page
    
    Returns:
        dict: Statistics data
    """
    stats = {
        'total_citations': 0,
        'h_index': 0,
        'i10_index': 0
    }
    
    try:
        # Find statistics table
        stats_table = soup.find('table', {'id': 'gsc_rsb_st'})
        if stats_table:
            rows = stats_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    label = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    if 'Citations' in label:
                        stats['total_citations'] = int(value.replace(',', ''))
                    elif 'h-index' in label:
                        stats['h_index'] = int(value)
                    elif 'i10-index' in label:
                        stats['i10_index'] = int(value)
    
    except Exception as e:
        print(f"Error extracting statistics: {e}")
    
    return stats

def save_publications_json(data, filename='publications.json'):
    """
    Save publications data to JSON file
    
    Args:
        data (dict): Publications data
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Publications data saved to {filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def main():
    """Main function"""
    scholar_id = 'yvZVcDQAAAAJ'  # Your Google Scholar ID
    
    print(f"Fetching publications for Google Scholar ID: {scholar_id}")
    print("This may take a few minutes...")
    
    data = fetch_google_scholar_publications(scholar_id)
    
    if data:
        save_publications_json(data)
        print(f"\nSuccessfully fetched {data['total_publications']} publications")
        print(f"Statistics:")
        print(f"  Total Citations: {data['statistics']['total_citations']}")
        print(f"  H-Index: {data['statistics']['h_index']}")
        print(f"  i10-Index: {data['statistics']['i10_index']}")
    else:
        print("Failed to fetch publications")

if __name__ == "__main__":
    main()
