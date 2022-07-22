import random
import json
import re
import os
from PIL import Image
import pytesseract
import requests


pytesseract_loaded = False

with open('companycrawler/json/functions-config.json', 'r') as f:
    jsonData = json.load(f)
    if jsonData['pytesseract-path']:
        pytesseract.pytesseract.tesseract_cmd = jsonData['pytesseract-path']
        pytesseract_loaded = True
    headers = jsonData['user-agent-header']

def img_to_text(path):
    img = Image.open(path)
    if pytesseract_loaded:
        return pytesseract.image_to_string(img, lang='eng')
    return ""

def gen_path(ext=''):
    path = str(random.random())[2:] + ext
    
    while path in os.listdir():
        path = str(random.random())[2:] + ext
        
    return path

def download_url(url, save_path):
    try:
        r = requests.get(url, verify=False, headers=headers)
        
        with open(save_path, 'wb') as g:
            g.write(r.content)
        return True
    except Exception as e:
        print(e)
        return False

def find_ext(path):
    lower = path.lower()
    if path:
        for ext in ['.png', '.jpg', '.jpeg']:
            if lower.endswith(ext):
                return ext
            elif ext in lower:
                for idx in [x.end() for x in re.finditer(ext, lower)]:
                    if idx < len(lower) and not lower[idx].isalnum():
                        return ext
    return ''

def is_pdf(url):
    if url.endswith('.pdf'):
        return True
    elif '.pdf' in url:
        for idx in [x.end() for x in re.finditer('.pdf', url)]:
            if idx < len(url) and not url[idx].isalnum():
                return True
    return False

# Deletes trailing '/' and '#'
def url_rstrip(s):
    return s.rstrip('#').rstrip('/')

def print_header(header):
    print('+-' + len(header)*'-' + '-+')
    print('|', header, '|')
    print('+-' + len(header)*'-' + '-+')
