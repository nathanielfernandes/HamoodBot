from bs4 import BeautifulSoup as BS
import requests

def covid_info(country):
    url = "https://www.worldometers.info/coronavirus/"
    if country == ():
        url = url
    else:
        url = "https://www.worldometers.info/coronavirus/country/" + str(country) + "/"

    data = requests.get(url)
    soup = BS(data.text, 'html.parser')
    total = soup.find("div", class_ = "maincounter-number").text
    total = total[1 : len(total) - 2]
    other = soup.find_all("span", class_ = "number-table")
    recovered = other[2].text
    deaths = other[3].text
    deaths = deaths[1:]
    info = {'Total Cases':total, 'Recovered Cases':recovered, 'Total Deaths':deaths}

    return info

