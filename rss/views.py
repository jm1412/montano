import json
import os
from django.http import HttpResponse, JsonResponse
from xml.etree.ElementTree import Element, SubElement, tostring
import requests

# Path to JSON file on GitHub
JSON_FILE_URL = 'https://jm1412.github.io/mangapark_latest.json'

def fetch_json():
    response = requests.get(JSON_FILE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_xml_from_json(data):
    root = Element('rss', version="2.0")
    channel = SubElement(root, 'channel')

    title_channel = SubElement(channel, 'title')
    title_channel.text = "MangaPark Latest Releases"
    
    link_channel = SubElement(channel, 'link')
    link_channel.text = "https://mangapark.com/"
    
    description_channel = SubElement(channel, 'description')
    description_channel.text = "Latest manga release information."

    for entry in data:
        item_element = SubElement(channel, 'item')
        
        chapter_title_element = SubElement(item_element, 'title')
        chapter_title_element.text = f"{entry['manga']} - {entry['chapter']}"
        
        chapter_link_element = SubElement(item_element, 'link')
        chapter_link_element.text = entry['link']

    return tostring(root, encoding='utf-8', method='xml').decode('utf-8')

def mangapark_rss(request, filter=None):
    data = fetch_json()
    if not data:
        return JsonResponse({"error": "Unable to fetch data."}, status=500)

    if filter:
        filter = filter.lower()
        filtered_data = [entry for entry in data if filter in entry['manga'].lower()]
        if not filtered_data:
            return JsonResponse({"error": f"No entries found for filter: {filter}"}, status=404)
    else:
        filtered_data = data

    xml_string = generate_xml_from_json(filtered_data)
    return HttpResponse(xml_string, content_type='application/xml')
