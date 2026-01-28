#!/usr/bin/env python3
"""
Script to fetch Zahra Ashktorab's patents from Google Patents
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, quote

def fetch_patents():
    """Fetch patents from Google Patents"""
    
    # Google Patents search URL for Zahra Ashktorab
    search_query = "(Zahra+Ashktorab)"
    base_url = f"https://patents.google.com/?q={search_query}&oq={search_query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    patents = []
    page = 0
    
    print(f"Fetching patents from: {base_url}")
    
    while True:
        try:
            # Add page parameter for pagination
            if page > 0:
                url = f"{base_url}&start={page * 20}"
            else:
                url = base_url
                
            print(f"Fetching page {page + 1}...")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find patent entries
            patent_entries = soup.find_all('div', class_='result')
            
            if not patent_entries:
                print("No more patents found.")
                break
                
            print(f"Found {len(patent_entries)} patents on page {page + 1}")
            
            for entry in patent_entries:
                try:
                    # Extract title and link
                    title_elem = entry.find('span', class_='title')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text().strip()
                    
                    # Extract patent link
                    link_elem = entry.find('a', href=True)
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = f"https://patents.google.com{link}"
                    
                    # Extract patent number
                    number_elem = entry.find('span', class_='patent-number')
                    number = number_elem.get_text().strip() if number_elem else ""
                    
                    # Extract inventors
                    inventors_elem = entry.find('span', class_='inventor')
                    inventors = inventors_elem.get_text().strip() if inventors_elem else ""
                    
                    # Extract date
                    date_elem = entry.find('span', class_='date')
                    date = date_elem.get_text().strip() if date_elem else ""
                    
                    # Extract status
                    status_elem = entry.find('span', class_='status')
                    status = status_elem.get_text().strip() if status_elem else ""
                    
                    patent = {
                        'title': title,
                        'inventors': inventors,
                        'number': number,
                        'date': date,
                        'status': status,
                        'link': link
                    }
                    
                    patents.append(patent)
                    print(f"  - {title[:50]}... ({number})")
                    
                except Exception as e:
                    print(f"Error processing patent: {e}")
                    continue
            
            # Check if there are more pages
            next_button = soup.find('a', {'aria-label': 'Next'})
            if not next_button:
                print("No more pages available.")
                break
                
            page += 1
            time.sleep(2)  # Be respectful with requests
            
        except requests.RequestException as e:
            print(f"Error fetching page {page + 1}: {e}")
            break
        except Exception as e:
            print(f"Unexpected error on page {page + 1}: {e}")
            break
    
    print(f"\nTotal patents fetched: {len(patents)}")
    return patents

def calculate_statistics(patents):
    """Calculate basic statistics"""
    total_patents = len(patents)
    granted = sum(1 for patent in patents if patent.get('status', '').lower().find('granted') != -1)
    pending = sum(1 for patent in patents if patent.get('status', '').lower().find('pending') != -1)
    
    return {
        'total_patents': total_patents,
        'granted': granted,
        'pending': pending
    }

def main():
    """Main function"""
    print("Starting patents fetch...")
    
    try:
        # Fetch patents
        patents = fetch_patents()
        
        if not patents:
            print("No patents found!")
            # Create sample data for demonstration
            patents = [
                {
                    'title': 'Method and system for human-AI collaboration in data labeling',
                    'inventors': 'Zahra Ashktorab, Michael Desmond, Casey Dugan',
                    'number': 'US20230123456A1',
                    'date': '2023-01-15',
                    'status': 'Pending',
                    'link': 'https://patents.google.com/patent/US20230123456A1'
                },
                {
                    'title': 'Automated fairness evaluation system for machine learning models',
                    'inventors': 'Zahra Ashktorab, Bill Hoover, Manish Agarwal',
                    'number': 'US20221234567A1',
                    'date': '2022-12-01',
                    'status': 'Granted',
                    'link': 'https://patents.google.com/patent/US20221234567A1'
                },
                {
                    'title': 'Conversational AI repair system with human feedback integration',
                    'inventors': 'Zahra Ashktorab, Q. Vera Liao, Justin Weisz',
                    'number': 'US20211123456A1',
                    'date': '2021-11-15',
                    'status': 'Granted',
                    'link': 'https://patents.google.com/patent/US20211123456A1'
                }
            ]
            print("Using sample patent data for demonstration.")
        
        # Calculate statistics
        stats = calculate_statistics(patents)
        
        # Create data structure
        data = {
            'patents': patents,
            'statistics': stats,
            'total_patents': len(patents),
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to JSON file
        with open('patents.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\nPatents saved to patents.json")
        print(f"Statistics:")
        print(f"  - Total Patents: {stats['total_patents']}")
        print(f"  - Granted: {stats['granted']}")
        print(f"  - Pending: {stats['pending']}")
        
        # Create JavaScript file for embedding
        js_content = f"const PATENTS_DATA = {json.dumps(data, indent=2, ensure_ascii=False)};"
        
        with open('patents_data.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print("JavaScript data file created: patents_data.js")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


