# Python program to obtain Weather data using WebScraping and Beautiful Soup from Weather.com

# Import necessary modules
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to create page and soup
def getPage(url):
    # Create page object
    page = requests.get(url)

    # Create soup with page data
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

# Function to scrape data from website
def getData(soup):
    # Obtain location of weather data
    loc = soup.find(class_='_-_-node_modules--wxu-components-src-molecule-Card-Card--cardHeading--3et4e').get_text()

    # Find location of daily weather data
    forecastWrapper = soup.find(id='WxuDailyWeatherCard-main-bb1a17e7-dc20-421a-b1b8-c117308c6626')

    # Find data
    daysList = forecastWrapper.find_all('li')

    # Lists for Date, temperatur and humidity
    dayName = []
    dayTemp = []
    dayHumidity = []

    # Obtain data from website
    for day in daysList:
        dayName.append(day.find(class_='_-_-node_modules--wxu-components-src-atom-Ellipsis-Ellipsis--ellipsis--lfjoB').get_text())
        dayTemp.append(day.find(class_='_-_-node_modules--wxu-components-src-molecule-WeatherTable-Column-Column--tempLo--19O32').get_text())
        dayHumidity.append(day.find(class_='_-_-node_modules--wxu-components-src-molecule-WeatherTable-Column-Column--precip--2H5Iw').get_text())

    return loc, dayName, dayTemp, dayHumidity

def organizeData(dayName, dayTemp, dayHumidity):
    # Organize scraped data
    weather_data = pd.DataFrame(
        {
            'Date': dayName,
            'Temperature': dayTemp,
            'Humidity Level': dayHumidity
        }
        )
    
    return weather_data

# Function to run program
def run(url):
    soup = getPage(url)

    loc, dayName, dayTemp, dayHumidity = getData(soup)

    weather_data = organizeData(dayName, dayTemp, dayHumidity)

    print(loc)
    print(weather_data)

# Loop to run program multiple times
again = True
while again is True:
    print('')
    url = input('URL of Location: ')

    print('')
    run(url)

    print('')
    next = input('Again? y/n: ')
    if next.lower() == 'n':
        again = False
