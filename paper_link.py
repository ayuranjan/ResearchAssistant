import json
import urllib.parse
import feedparser
import requests
import re
import boto3
import os

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    # If S3 object_name is not specified, use file_name
    if object_name is None:
        object_name = file_path

    # Create an S3 client
    s3_client = boto3.client('s3',
                             aws_access_key_id='AKIAQT2YWNM4BE2J54FQ',
                            aws_secret_access_key='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',
                            region_name='us-west-2' )
    try:
        # Upload the file to S3 bucket
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
    else:
        print("Upload successful")
        return True


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
        
    response = requests.get(pdf_link)
    # Raise an exception if the request was not successful
    response.raise_for_status()
    regular_filename = re.sub(r'[^\w\s]', '', title.replace('\n', ''))
    regular_filename = regular_filename.replace(' ', '_')
    
    # Open the local file in binary write mode
    with open(f"{regular_filename}.pdf", 'wb') as f:
        # Write the content of the response to the local file
        f.write(response.content)
        
    upload_file_to_s3(f"{regular_filename}.pdf", "researchbucketpdf")
    
    os.remove(f"{regular_filename}.pdf")
    
paper_link("Electron thermal conductivity owing to collisions between degenerate electrons")