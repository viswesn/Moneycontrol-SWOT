import requests
from bs4 import BeautifulSoup
import csv
import os
import json

pattern = r'\((\d+)\)'
ids = ['swot_ls', 'swot_lw', 'swot_lo', 'swot_lt']
labels = ["Strengths", "Weaknesses", "Opportunities", "Threats"]


def make_swot(stockname=None, url=None, sector=None, strengths=0, weaknesses=0, opportunities=0, threats=0, mc_essentials=-1):
    swot = [stockname, url, sector, strengths, weaknesses, opportunities, threats, mc_essentials]
    return swot


def get_mc_essentials(soup):
    div_element = soup.find('div', class_='bx_mceti mc_essenclick')
    if not div_element:
        return "-1"
    elements = div_element.find_all('div', class_=lambda x: x and 'esbx' in x)
    if not elements:
        return "-1%"
    for element in elements:
        mc_value = element.text or "-1% Fail"
    return mc_value.split('%')[0]


def get_sowt_values(soup):
    swot_array = [-1, -1, -1, -1]
    div_element = soup.find('div', class_='swot_feature')
    # Check if the element was found
    if not div_element:
        return
    # Do something with the <div> element, e.g., print its content
    # Find all the <li> elements within the <div> element
    li_elements = div_element.find_all('li', class_='swotliClass')
    # Loop through the <li> elements

    for li_element in li_elements:
        # Extract the ID attribute value
        swot_element = li_element.find('strong')
        # Check if the <strong> element was found
        if not swot_element:
            return
        swot_element_value = swot_element.text
        parts = swot_element_value.split('(')
        if len(parts) != 2:
            return
        category = parts[0].strip()
        value = parts[1].strip(')').strip()
        # Check if the category is valid
        if category not in labels:
            return
        index = labels.index(category)
        try:
            swot_array[index] = int(value)
        except ValueError:
            return
    return swot_array


def get_stock_details(soup):
    div_element = soup.find('div', class_='inid_name', id='stockName')
    if not div_element:
        return None, None
    stock = div_element.find('h1').text.strip()
    sector = div_element.find('strong').text.strip() or "NA"
    return stock, sector


def get_sowt_details(url):
    mc_essentials = -1
    # Send an HTTP GET request to the URL
    stock = url.split('/')[-1]
    filename = "stock/{}.html".format(stock.rstrip('\n'))
    if not os.path.isfile(filename):
        response = requests.get(url)
        if response.status_code != 200:
            return
        with open(filename, "wb") as file:
            file.write(response.content)
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content of the page
    soup = BeautifulSoup(html_content, 'html.parser')

    stock_name, sector = get_stock_details(soup)
    if not stock_name:
        return

    if sector and sector == "ETF":
        return

    swot_array = get_sowt_values(soup)
    if not swot_array:
        return

    # Check if all elements in the list are 0
    all_zeros = all(element == 0 for element in swot_array)
    if not all_zeros:
        mc_essentials = get_mc_essentials(soup)
        return make_swot(stock_name, url.rstrip("\n"), sector, swot_array[0], swot_array[1], swot_array[2], swot_array[3], mc_essentials)
    return


if __name__ == "__main__":
    count = 0
    index = 0
    with open("swot_details.csv", mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        with open('stocks.csv', 'r') as companies:
            for company in companies:
                if company:
                    name, link = company.split(',')
                    count += 1
                    index += 1
                    print(index, ":", name)
                    data = get_sowt_details(link)
                    if data:
                        writer.writerow(data)
                if count == 100:
                    csv_file.flush()
                    count = 0
