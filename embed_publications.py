#!/usr/bin/env python3
"""
Script to embed publications data directly into the HTML file
"""

import json

def embed_publications():
    """Read publications.json and create JavaScript data to embed in HTML"""
    
    try:
        with open('publications.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create JavaScript data structure
        js_data = f"""
        const PUBLICATIONS_DATA = {json.dumps(data, indent=2)};
        """
        
        # Write to a JavaScript file
        with open('publications_data.js', 'w', encoding='utf-8') as f:
            f.write(js_data)
        
        print("Publications data embedded successfully!")
        print(f"Total publications: {data['total_publications']}")
        print(f"Total citations: {data['statistics']['total_citations']}")
        print(f"H-index: {data['statistics']['h_index']}")
        
        return True
        
    except Exception as e:
        print(f"Error embedding publications: {e}")
        return False

if __name__ == "__main__":
    embed_publications()
