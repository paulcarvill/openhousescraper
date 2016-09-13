#!/usr/bin/python

import urllib2
import xlwt
from bs4 import BeautifulSoup

class House(object):
  def __init__(self, url, name="", address="", description=""):
    self.url=url
    self.name=name
    self.address=address
    self.description=description

# make a list to hold all the house page urls
housePages = []

# loop through the site's pagination and get all the individual house page links
for page in range(1,17):
  response = urllib2.urlopen("http://listings.openhouselondon.org.uk/?sf_paged=%d" % (page))
  page_source = response.read()
  soup = BeautifulSoup(page_source, "html.parser")
  
  # get house page link from the div>a element
  divs = soup.find_all("div", class_="result-container col-1-3")
  for div in divs:
    link = div.find('a')
    housePages.append(House(link['href']))

# get details from each house page
for house in housePages:
  response = urllib2.urlopen(house.url)
  page_source = response.read()
  soup = BeautifulSoup(page_source, "html.parser")

  # get address
  address = soup.find("div", class_="et_pb_text et_pb_module address-module")
  addressText = address.find('p').getText()
  house.address = addressText

  # get name
  name = soup.find("div", class_="et_pb_text et_pb_module listing-title")
  nameText = name.find('h1').getText()
  house.name = nameText

  #get opening hours
  hours = soup.find("div", class_="et_pb_text et_pb_module opening-module")
  hoursText = hours.find('p').getText()
  house.hours = hoursText

  # get description
  description = soup.find("div", class_="et_pb_text et_pb_module listing-description")
  descriptionText = description.find('h5').getText()
  house.description = descriptionText

# create a spreadsheet file
book = xlwt.Workbook()
sheet1 = book.add_sheet("Open Houses")

cols = ["name", "description", "hours", "url", "address"]

# write each house detail to a new spreadsheet row
for index, house in enumerate(housePages):
  row = sheet1.row(index)
  row.write(0, house.name)
  row.write(1, house.description)
  row.write(2, house.hours)
  row.write(3, house.url)
  row.write(4, house.address)
  
book.save("open-house.xls")
