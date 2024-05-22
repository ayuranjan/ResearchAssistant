import json
import urllib.parse
import feedparser

def paper_link(title):
    # TODO implement
    # title = event.get('title')
    
    query = urllib.parse.urlencode({
            "search_query": f"ti:{title}",
            "start": 0,
            "max_results": 1
        })

    # URL of the arXiv Atom feed
    base_url = "http://export.arxiv.org/api/query?"
    feed_url = base_url + query

    # Parse the feed
    feed = feedparser.parse(feed_url)
    
    if not feed.entries:
        pdf_link = "No entries found for the given title. (-1"

    # Iterate over each entry in the feed and extract information
    for entry in feed.entries:
        # Extract basic information
        # print(entry)
        entry_id = entry.id
        updated = entry.updated
        published = entry.published
        title = entry.title
        summary = entry.summary
        
        # Extract authors
        authors = [author.name for author in entry.authors]
        
        # Extract DOI (Digital Object Identifier)
        doi = entry.get('arxiv_doi', 'N/A')
        
        # Extract links (for PDF, HTML, etc.)
        pdf_link = None
        for link in entry.links:
            if 'title' in link and link.title == 'pdf':
                pdf_link = link.href

        # Print extracted information
        print(f"ID: {entry_id}")
        print(f"Updated: {updated}")
        print(f"Published: {published}")
        print(f"Title: {title}")
        print(f"Summary: {summary}")
        print(f"Authors: {', '.join(authors)}")
        print(f"DOI: {doi}")
        print(f"PDF Link: {pdf_link}")
        print("\n" + "="*80 + "\n")
        
    return {
        'statusCode': 200,
        'body': pdf_link
    }
    
paper_link("Electron thermal conductivity owing to collisions between degenerate electrons")