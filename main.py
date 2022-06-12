# project start time 9.35 am
# break 10m
from bs4 import BeautifulSoup
import requests
import simplejson as json


# export later into csv or .env files
searchLinkWollplatz = 'https://www.wollplatz.de/{}'  # add searchItem into the q-list with .format('itemString')
searchItems = ['DMC-Natura-XL',
               'Drops-Safran',
               'Drops-Baby-Merino-Mix',
               'Hahn-Alpacca-Speciale',
               'Stylecraft-Special-double-knit'
               ]

class WebPageScraper:
    def __init__(self, itemList, searchLink):
        self.searchLink = searchLink  # add searchItem into the q-list with .format('itemString')
        self.searchItems = itemList
        self.responseList = []
        self.foundOutOfItemList = []
        self.search()

    def search(self):
        for item in self.searchItems:
            temp = requests.get(self.searchLink.format(item))
            if temp.status_code == 200:
                self.responseList.append(temp)
                self.foundOutOfItemList.append(item)

    def getFoundItems(self):
        return self.foundOutOfItemList

    #finds the String given and returns the element-info after found element
    def scrapInTable(self, tag, text):
        if tag == None or text == None: return []
        found = []
        for item in self.responseList:
            soup = BeautifulSoup(item.text, features="html.parser")
            temp = soup.findAll(tag, string=text)
            if len(temp) > 0: temp = temp[0].next_sibling
            for i in temp:
                found.append(i)
        return found

    #scraps for tag-class combination
    def scrapForClass(self, tag, wantedItem):
        if tag == None or wantedItem == None: return []
        found = []
        for item in self.responseList:
            soup = BeautifulSoup(item.text, features="html.parser")
            temp = soup.findAll(tag, wantedItem)
            if len(temp) > 0: temp = temp[0]
            for i in temp:
                found.append(i)
        return found

#[tag, class]
lieferzeitTag =['span', ['stock-green', 'stock-orange', 'stock-red']]
priceOfItemTag = ['span', 'product-price-amount']
nadelStaerkeTagString = ['td', 'Nadelstärke']
ZusammenstellungTagString = ['td', 'Zusammenstellung']

htmlOfSearchItem = []

wollplatz = WebPageScraper(searchItems, searchLinkWollplatz)

existingItemList = wollplatz.getFoundItems()
priceList = wollplatz.scrapForClass(priceOfItemTag[0], priceOfItemTag[1])
lieferbarkeit = wollplatz.scrapForClass(lieferzeitTag[0], lieferzeitTag[1])
Nadelstaerken = wollplatz.scrapInTable(nadelStaerkeTagString[0], nadelStaerkeTagString[1])
Zusammenstellung = wollplatz.scrapInTable(ZusammenstellungTagString[0], ZusammenstellungTagString[1])

FinalJSONString = '{"Wollplatz": [';

i = 0;
while i < len(existingItemList):
    obj = {
        "ItemName": existingItemList[i],
        "Price": priceList[i],
        "NeedleSize": Nadelstaerken[i],
        "Composition": Zusammenstellung[i]
    }
    FinalJSONString += json.dumps(obj, indent=4)
    if (i+1) != len(existingItemList): FinalJSONString += ','
    i += 1
FinalJSONString += ']}'

jFile = open('data.json', 'w')
jFile.write(FinalJSONString)
jFile.close();



#3 Stunden 20 minuten
