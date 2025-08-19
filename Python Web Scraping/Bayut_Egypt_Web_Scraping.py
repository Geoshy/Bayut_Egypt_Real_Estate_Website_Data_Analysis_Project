import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

page_link = f'https://www.bayut.eg/en/cairo/apartments-for-sale/?completion_status=ready'
second_page_link = 'https://www.bayut.eg/en/cairo/apartments-for-sale/page-2/?completion_status=ready'

links = []

for index in range(515):
    links.append(f"https://www.bayut.eg/en/cairo/apartments-for-sale/page-{index + 2}/?completion_status=ready")

def bayut_egypt(link, link_2=[]):
    try:
        selenium_service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=selenium_service)

        browser.get(link)
        time.sleep(5)

        currency_list = []
        price_list = []
        real_estate_type_list = []
        bedrooms_number_list = []
        bathrooms_number_list = []
        area_list = []
        location_list = []
        down_payment_list = []
        description = []

        apartments = browser.find_elements('class name', 'a37d52f0')
        for apartment in apartments:
            html_code = apartment.get_attribute('outerHTML')
            page_soup = BeautifulSoup(html_code, 'html.parser')
            currency_list.append(page_soup.find('span', {'class', '_06f65f02'}).text)
            price_list.append(page_soup.find('span', {'class' : 'dc381b54'}).text)
            real_estate_type_list.append(page_soup.find('div', {'class' : '_948d9e0a d05e0d48'}).span.span.text) 

            rooms_number = page_soup.find_all('span', {'class' : '_1822ec30 f34d293d'})
            bedrooms_number_list.append(rooms_number[1].text)
            bathrooms_number_list.append(rooms_number[2].text)

            area_list.append(page_soup.find('h4', {'class' : 'cfac7e1b _85ddb82f'}).text)
            location_list.append(page_soup.find('h3', {'class' : '_4402bd70'}).text)

            try:
                down_payment_list.append(page_soup.find('span', {'class' : '_41163454'}).text)
            except:
                down_payment_list.append('None')

            try:
                description.append(page_soup.find('h2', {'class' : 'f0f13906'}).text)
            except:
                description.append('None')

        selenium_service_2 = Service(ChromeDriverManager().install())
        browser_2 = webdriver.Chrome(service=selenium_service_2)
        for link in link_2:                                                   
            browser_2.get(link)
            time.sleep(1)

            apartments_2 = browser_2.find_elements('class name', 'a37d52f0')
            for apartment_2 in apartments_2:
                html_code_2 = apartment_2.get_attribute('outerHTML')
                page_soup_2 = BeautifulSoup(html_code_2, 'html.parser')
                currency_list.append(page_soup_2.find('span', {'class', '_06f65f02'}).text)
                price_list.append(page_soup_2.find('span', {'class' : 'dc381b54'}).text)
                real_estate_type_list.append(page_soup_2.find('div', {'class' : '_948d9e0a d05e0d48'}).span.span.text) 

                rooms_number_2 = page_soup_2.find_all('span', {'class' : '_1822ec30 f34d293d'})
                bedrooms_number_list.append(rooms_number_2[1].text)
                bathrooms_number_list.append(rooms_number_2[2].text)

                area_list.append(page_soup_2.find('h4', {'class' : 'cfac7e1b _85ddb82f'}).text)
                location_list.append(page_soup_2.find('h3', {'class' : '_4402bd70'}).text)

                try:
                    down_payment_list.append(page_soup_2.find('span', {'class' : '_41163454'}).text)
                except:
                    down_payment_list.append('None')

                try:
                    description.append(page_soup_2.find('h2', {'class' : 'f0f13906'}).text)
                except:
                    description.append('None')


        df_dictionary = {
            "Real_Estate_Type" : real_estate_type_list,
            "Location" : location_list,
            "Price" : price_list,
            "Down_Payment" : down_payment_list,
            "Currency" : currency_list,
            "Bedrooms_Number" : bedrooms_number_list,
            "Bathrooms_Number" : bathrooms_number_list,
            "Area" : area_list,
            "Description" : description
        }

        df = pd.DataFrame(df_dictionary)

        return(df.to_csv('bayut_egypt.csv', index=False))
    
    except Exception as error:
        print(f'Error With -bayut_egypt- Function: {error}')




