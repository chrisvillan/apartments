#https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from fake_useragent import UserAgent


import requests
from bs4 import BeautifulSoup
import json
import time
import sys 



def open_website_with_selenium(url):
    # print(url)

    #Set up Chrome options
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument(f'user-agent={user_agent}') 

    # chrome_options.add_argument('window-size=1920,1080')  # Set a larger window size

    # chrome_options.binary_location = 'C:/DRIVERS/Chrome/chrome.exe'
    
    driver = webdriver.Chrome(options=chrome_options)
    # driver.set_window_size(800, 600)
    try:
        driver.get(url)
        # Wait for the page to be completely loaded
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'header')))

        #Show Unavailable Floor Plans
        try:
            wait = WebDriverWait(driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-showUnavailableFloorPlansButton')))
            button.click()
            # print('Show Unavailable Floor Plans [Button] has been clicked')
        except Exception as e:
            # print(f"Show Unavailable Floor Plans [Button] error")
            pass
        #Show Floor Plan Details
        try:
            # Wait for the buttons to be present (adjust as needed)
            wait = WebDriverWait(driver, 10)
            buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'actionLinks')))
             # Click each button individually
            for button in buttons:
                button.click()
                # print('Show Floor Plan Details [Button] has been clicked')
        except Exception as e:
            # print(f"Show Floor Plan Details [Button] error")
            pass
        # Grab the HTML content
        html_content = driver.page_source

        # print(html_content)
        # print('HTML content obtained successfully.')
    
    except Exception as e:
        # print(f'Error: {str(e)}')
        pass
    finally:
        driver.quit()

    return html_content

def writeToFile(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f'File sucessfully save: {file_path}')

def remove_dict_duplicates(array_of_dicts):
    # Convert each dictionary to a JSON-formatted string
    json_strings = [json.dumps(d, sort_keys=False) for d in array_of_dicts]

    # Use set to remove duplicates
    unique_json_strings = set(json_strings)

    # Convert back to dictionaries
    unique_dicts = [json.loads(json_str) for json_str in unique_json_strings]

    return unique_dicts

def remove_array_duplicates(input_array):
    if not input_array:
        return []  # Return an empty list for an empty input array

    unique_items = list(set(input_array))
    return unique_items

def get_html_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

def sanitize_filename(filename):
    illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    sanitized_filename = ''.join(char for char in filename if char not in illegal_chars)
    return sanitized_filename

def get_json_apartments_com(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    script_tag = soup.find('script', {'type': 'application/ld+json'})

    # Extract the contents if the script tag is found
    if script_tag:
        json_ld_content = script_tag.string
        return json_ld_content
    else:
        print('No script tag with type="application/ld+json" found.')
        return None

def get_posts_apartments_com(json_content):
    post_links = []
    for post in json_content:
        post_links.append(post['url'])
    return post_links

#soup.find('h1',class_:='propertyName',id='propertyName')
def get_address(soup):
    address_container = soup.find('div',class_:='propertyAddressContainer')
    delivery_address = address_container.find('span', class_:='delivery-address')
    add_line_tag = delivery_address.find('span')
    city_tag = delivery_address.find_next_sibling()
    statezip_container = city_tag.find_next_sibling()
    state_tag = statezip_container.find('span')
    zip_tag = state_tag.find_next_sibling()

    address_line = add_line_tag.get_text(strip=True)
    city = city_tag.get_text(strip=True)
    state = state_tag.get_text(strip=True)
    zipcode = zip_tag.get_text(strip=True)
    address = f'{address_line}, {city}, {state} {zipcode}'

    my_dict = {
        'address': address,
        'address_line': address_line,
        'city': city,
        'state': state,
        'zipcode': zipcode
    }

    return my_dict

#soup.find_all('div', class_:='priceGridModelWrapper js-unitContainer mortar-wrapper')
def get_unit_details(units):
    unit_dicts = []
    for unit in units:
        unit_name = unit.find('span', class_:='modelName').get_text()
        rent_price = unit.find('span', class_:='rentLabel').get_text()
        details_tag = unit.find('h4', class_:='detailsLabel')
        room_tag = details_tag.find('span', class_:='detailsTextWrapper')
        
        span_tag = room_tag.find('span')
        room_type = span_tag.get_text(strip=True)
        
        span_tag = span_tag.find_next_sibling()
        bath = span_tag.get_text(strip=True)

        span_tag = span_tag.find_next_sibling()
        room_size = span_tag.get_text(strip=True)

        details_tag = details_tag.find('span', class_:='detailsTextWrapper leaseDepositLabel')
        span_tag = details_tag.find('span')

        lease = span_tag.get_text(strip=True)

        
        if details_tag.find('span', class_:='availabilityInfo'):
            availability = details_tag.find('span', class_:='availabilityInfo').get_text(strip=True)
        else:
            availability = ''


        amenity_highlight = []
        amenity_kitchen = []
        amenity_floor = []
        amenity_other = []
        if unit.find('ul', class_:='allAmenities'):
            amenities_container = unit.find('ul', class_:='allAmenities')
            li_tags = amenities_container.find_all('li', recursive=False)

            for li_tag in li_tags:
                amenity_temp = []
                span_tag = li_tag.find('span')
                amenity_tags = li_tag.find_all('span',class_:='amenity')
                for amenity_tag in amenity_tags:
                    amenity_temp.append(amenity_tag.get_text(strip=True))
                    
                if span_tag.get_text(strip=True) == 'Highlights':
                    amenity_highlight = amenity_temp
                elif span_tag.get_text(strip=True) == 'Kitchen Features & Appliances':
                    amenity_kitchen = amenity_temp
                elif span_tag.get_text(strip=True) == 'Floor Plan Details':
                    amenity_floor = amenity_temp
                else:
                    amenity_other = amenity_other + amenity_temp
        
        
        my_dict = {
            'name': unit_name,
            'type': room_type,
            'bath': bath,
            'size': room_size,
            'lease': lease,
            'availability': availability,
            'amenities':{
                'highlight': amenity_highlight,
                'kitchen': amenity_kitchen,
                'floor': amenity_floor,
                'other': remove_array_duplicates(amenity_other)
            }

        }
        unit_dicts.append(my_dict)

    return unit_dicts

def set_page_range(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pageRange_tag = soup.find('span', class_:='pageRange')
    page_str = ''
    page_max = 1
    if pageRange_tag:
        page_str = pageRange_tag.get_text(strip=True)
        if page_str != '':
            words = page_str.split(' ')
            page_max = int(words[-1])

    return page_max


url = "https://www.apartments.com/orange-county-ca/under-2000/?bb=5qojn2g6kNuizm_zb"

html_content = open_website_with_selenium(url)
page_max = set_page_range(html_content)
# page_max  = 3
units = []
for page in range(1,page_max +1):
    
    if page == 1:
        url = "https://www.apartments.com/orange-county-ca/under-2000/?bb=5qojn2g6kNuizm_zb"
    else:
        url = f'https://www.apartments.com/orange-county-ca/under-2000/{page}/?bb=5qojn2g6kNuizm_zb'
    
    html_content = open_website_with_selenium(url)
    json_content = get_json_apartments_com(html_content)
    data_dict = json.loads(json_content)
    about_content = data_dict.get('about', [])
    # file_path = 'test.json'
    # writeToFile(html_content, file_path)

    #Get post urls
    post_urls = get_posts_apartments_com(about_content)

    #Get post data
    count = 1
    for url in post_urls:
        print(f'Page: {page} / {page_max} | Post: {count} / {len(post_urls)+1}')
        # url = "https://www.apartments.com/carlyle-courtyard-anaheim-ca/rmhy2h3/"
        html_content = open_website_with_selenium(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title').get_text(strip=True)
        filepath = './urls/' + sanitize_filename(title) + '.html'
        writeToFile(html_content, filepath)

        # unit_dicts = get_unit_details(soup.find_all('div', class_:='priceGridModelWrapper js-unitContainer mortar-wrapper'))
        # unit_dicts = remove_dict_duplicates(unit_dicts)

        # my_dict = {
        #     'title': title,
        #     'url': url,
        #     'units': unit_dicts,
        # }

        # units.append(my_dict)
        # count += 1

# content = json.dumps(units, indent=4, sort_keys=False)
# writeToFile(content, './test/unit_details.json')


    # soup = BeautifulSoup(html_content, 'html.parser')
    # address_dict = get_address(soup.find('h1',class_:='propertyName',id='propertyName'))
