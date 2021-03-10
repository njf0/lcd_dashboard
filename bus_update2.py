import requests
import datetime
import get_json
import re
from bs4 import BeautifulSoup
from data import NEXTBUSES_WEBSITE_URL
from requests.adapters import HTTPAdapter

def get_buses():

    s = requests.Session()
    s.mount(NEXTBUSES_WEBSITE_URL, HTTPAdapter(max_retries = 1))
    
    try:
        response = s.get(NEXTBUSES_WEBSITE_URL)
        bus_soup = BeautifulSoup(response.text, 'html.parser')
        test_tag = bus_soup.find_all('p', {"class" : "Stops"}, text=True)
        bus_strings = [i.text for i in test_tag]
        times = [''.join((re.findall(r'.*(\d{2}:\d{2}|\d{1,2} mins)', i))) for i in bus_strings]
    except:
        ConnectionError()
        times = ['Unavailable'] 
    
    output = [i for i in times if i.strip()]
    
    return output

if __name__ == '__main__':
    
    a = get_buses()
    
    print(a)
