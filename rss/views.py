import subprocess
import os
import time
from django.http import HttpResponse
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, tostring

def scrape_mangapark(request, num_pages=2):
    base_url = 'https://mangapark.com/latest'
    output_file = 'mangapark_latest.html'
    cache_duration = 30 * 60  # 30 minutes in seconds

    # Check if the output file exists and is not older than 30 minutes
    if os.path.exists(output_file) and (time.time() - os.path.getmtime(output_file)) < cache_duration:
        with open(output_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
    else:
        try:
            # Use wget to fetch the webpage
            with open(output_file, 'w', encoding='utf-8') as file:
                for page in range(1, num_pages + 1):
                    url = f"{base_url}?page={page}"
                    subprocess.run(['wget', '-O', file.name, url], check=True)

            # Read the content from the output file
            with open(output_file, 'r', encoding='utf-8') as file:
                html_content = file.read()

        except Exception as e:
            return HttpResponse(f"Error fetching page: {str(e)}", status=500)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    manga_dict = {}

    # Extract manga titles and chapter links
    manga_items = soup.select('.pl-3')  # Select the parent container

    for item in manga_items:
        manga_title = item.find('h3').get_text(strip=True)
        chapters = item.select('a.link-hover.link-primary')  # Select chapter links within the same parent

        # Create a list of chapter links for this manga
        chapter_list = [(chapter.get_text(strip=True), chapter['href']) for chapter in chapters]

        if chapter_list:
            manga_dict[manga_title] = manga_dict.get(manga_title, []) + chapter_list

    # Generate XML structure
    root = Element('manga_updates')

    for manga, chapters in manga_dict.items():
        manga_element = SubElement(root, 'manga', title=manga)
        for chapter_title, chapter_link in chapters:
            chapter_element = SubElement(manga_element, 'chapter')
            chapter_element.set('title', chapter_title)
            chapter_element.set('link', f"https://mangapark.com{chapter_link}")

    # Convert the XML structure to a string
    xml_string = tostring(root, encoding='utf-8', method='xml').decode('utf-8')

    return HttpResponse(xml_string, content_type='application/xml')
