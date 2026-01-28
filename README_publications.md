# Publications System for Personal Website

This system allows you to automatically fetch and display your Google Scholar publications on your personal website.

## Files Created

- `publications.html` - The main publications page
- `fetch_publications.py` - Python script to fetch publications from Google Scholar
- `requirements.txt` - Python dependencies
- `publications.json` - Generated file containing publication data (created after running the script)

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fetch Publications from Google Scholar

Run the Python script to fetch your publications:

```bash
python fetch_publications.py
```

This will:
- Scrape your Google Scholar profile
- Extract publication details (title, authors, venue, year, citations)
- Generate a `publications.json` file with all the data
- Display statistics (total citations, h-index, etc.)

### 3. View the Publications Page

Open `publications.html` in your web browser to see your publications displayed in a clean, organized format.

## Features

- **Automatic Data Fetching**: Fetches all publications from your Google Scholar profile
- **Statistics Display**: Shows total papers, citations, and h-index
- **Clean Design**: Publications are displayed in an organized, readable format
- **Fallback System**: If the JSON file doesn't exist, shows manually curated publications
- **Responsive Design**: Works on desktop and mobile devices
- **Clickable Links**: Publication titles link to their Google Scholar pages

## Customization

### Adding More Publications Manually

If you want to add publications that aren't on Google Scholar, you can edit the `manual-publications` section in `publications.html`.

### Styling

The publications are styled with CSS classes:
- `.publication-item` - Individual publication container
- `.publication-title` - Publication title
- `.publication-authors` - Author list
- `.publication-venue` - Venue/journal name
- `.publication-year` - Publication year
- `.publication-citations` - Citation count

### Updating Data

To refresh your publications data, simply run the Python script again:

```bash
python fetch_publications.py
```

## Troubleshooting

### If the Python script fails:
- Make sure you have a stable internet connection
- Check that your Google Scholar profile is public
- The script includes delays to be respectful to Google Scholar's servers

### If publications don't display:
- Check that `publications.json` was created successfully
- Open the browser's developer console to see any JavaScript errors
- The page will fall back to manual publications if the JSON file is missing

## Notes

- The script respects Google Scholar's rate limits with built-in delays
- Some publications might not parse perfectly due to varying formats
- The system is designed to be robust with fallback mechanisms
- All data is stored locally in JSON format for fast loading
