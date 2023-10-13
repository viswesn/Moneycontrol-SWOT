import requests
from bs4 import BeautifulSoup
import csv

# This program is used to get all the stock names of the Indian market from moneycontrl.com
# using the alphapet letters.
def get_stock_names(writer, letter):
    # URL of the page containing the list of stock names
    url = "https://www.moneycontrol.com/india/stockpricequote/" + "{}".format(letter)

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table with the specified class name
        table = soup.find('table', class_='pcq_tbl MT10')

        # Check if the table was found
        if table:
            # You can now work with the 'table' variable, e.g., extract data from it
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if not cells:
                    continue
                for cell in cells:
                    link_element = cell.find('a')
                    if link_element and link_element.text:
                        link = link_element.get('href')
                        writer.writerow([link_element.text, link])
        else:
            print("Table not found with the specified class name.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


if __name__ == "__main__":
    count = 0
    with open('stocks.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_NONE)
        for letter in range(ord('A'), ord('Z') + 1):
            count += 1
            get_stock_names(writer, chr(letter))
            if count == 100:
                csv_file.flush()
                count = 0
