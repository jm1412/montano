import subprocess
import os
from django.http import HttpResponse
from bs4 import BeautifulSoup

def scrape_mangapark(request):
    url = 'https://mangapark.com/latest'
    output_file = 'mangapark_latest.html'

    try:
        # Use wget to fetch the webpage
        subprocess.run(['wget', '-O', output_file, url], check=True)

        # Read the content from the output file
        with open(output_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract chapter links
        chapter_items = soup.select('a.link-hover.link-primary')
        chapter_list = [(item.get_text(strip=True), item['href']) for item in chapter_items]

        # Clean up the output file
        #os.remove(output_file)

        # Prepare the response
        if chapter_list:
            response_html = "<br>".join([f"{chapter}: {link}" for chapter, link in chapter_list])
            return HttpResponse(response_html)
        else:
            return HttpResponse("No chapter links found", status=404)

    except Exception as e:
        return HttpResponse(f"Error fetching page: {str(e)}", status=500)
