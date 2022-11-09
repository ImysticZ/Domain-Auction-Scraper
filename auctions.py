from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import os

date = []
suburbs = []
address = []
urls = []
beds = []
prices = []
property = []
agent = []
region = []
status = []
states = ['SYDNEY', 'MELBOURNE', 'BRISBANE', 'ADELAIDE', 'CANBERRA']

if os.path.isdir("auctions"):
    os.chdir("auctions")
else:
    os.mkdir("auctions")
    os.chdir("auctions")

t = datetime.now()

for x in states:
    url = 'https://www.domain.com.au/auction-results/' + x.lower() + '/'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    for url in soup.find_all("a", {"class": "css-1b9txmm"}):  # used to get the urls of houses
        urls.append(url.get('href'))

    for houses in soup.find_all('article', {'class': 'css-3xqrp1'}):
        house_in_subs = len(houses.find_all('div', {'class': 'css-hjun8m'}))  # number of houses in a suburb

        for house in range(0, house_in_subs):  # loops through the suburbs for the amount of houses
            date.append(t.strftime('%d/%m/%Y'))

            addy = houses.find_all('a', {'class': 'css-1b9txmm'})  # address
            address.append(addy[house].get_text())  # appends each each address through a loop

            subs = houses.find('h3')  # suburb
            suburbs.append(subs.get_text())  # appends to suburbs for the amount of houses in each suburb

            try:  # some listings have no beds
                bed = houses.find_all('span', {'class': 'css-1g2pbs1'})[house]  # amount of beds
                beds.append(bed.get_text())
            except:
                beds.append(None)

            try:
                agen = houses.find_all('a', {'class': 'css-1ctpznc'})  # agent
                agent.append(agen[house].get_text())
            except:
                agen = houses.find_all('li', {'class': 'css-1wxwou3'})  # agent
                agent.append(agen[house].get_text())


            try:  # some listings have no price
                price = houses.find_all('span', {'class': 'css-m75dnw'})[house]  # price of house
                prices.append(price.get_text())
            except:
                prices.append(None)

            region.append(x)  # state

            try:  # some listings have no status
                state = houses.find_all('li', {'class': 'css-43wvni'})[house]  # status of the house
                stateNew = state.find_all('span')[0]
                status.append(stateNew.get_text())
            except:
                status.append(None)

            try:  # some listings have no type
                type = houses.find_all('li', {'class': 'css-dpwygs'})[house]  # type of house
                typeNew = type.find_all('span')[0]
                property.append(typeNew.get_text())
            except:
                property.append(None)

filename = t.strftime("%d%m%Y")

data = {'Date' : date, 'Region': region, 'Suburb': suburbs, 'Address': address, 'Agent': agent, 'Status': status, 'Prices': prices,
        'Beds': beds, 'Property': property, 'URL': urls}

df = pd.DataFrame(data)
df.to_csv(filename + ".csv", index=False)
