from bs4 import BeautifulSoup
import requests
import simplejson as json

# export later into external file
searchLinkWollplatz = 'https://www.wollplatz.de/{}'
searchItems = ['DMC-Natura-XL',
               'Drops-Safran',
               'Drops-Baby-Merino-Mix',
               'Hahn-Alpacca-Speciale',
               'Stylecraft-Special-double-knit'
               ]

class WebPageScraper:
    def __init__(self, itemList, searchLink): #searchlink needs '{}' in position of the search-word
        self.searchLink = searchLink
        self.searchItems = itemList
        self.responseList = []
        self.foundOutOfItemList = []
        self.search()

    #searches website for pages and saves those with an status_code = 200 to the responseList
    def search(self):
        for item in self.searchItems:
            temp = requests.get(self.searchLink.format(item))
            if temp.status_code == 200:
                self.responseList.append(temp)
                self.foundOutOfItemList.append(item)

    #returns list of "search-words" to which a page was found
    def getFoundItems(self):
        return self.foundOutOfItemList

    #finds the String given and returns the element-info after found element
    def scrapeInTable(self, tag= None, text= None):
        if tag == None or text == None: return []
        found = []
        for item in self.responseList:
            soup = BeautifulSoup(item.text, features="html.parser")
            temp = soup.findAll(tag, string=text)
            if len(temp) > 0: temp = temp[0].next_sibling
            for i in temp:
                found.append(i)
        return found

    #scrapes for tag-class combination
    def scrapeForClass(self, tag= None, wantedItem= None):
        if tag == None or wantedItem == None: return []
        found = []
        for item in self.responseList:
            soup = BeautifulSoup(item.text, features="html.parser")
            temp = soup.findAll(tag, wantedItem)
            if len(temp) > 0: temp = temp[0]
            for i in temp:
                found.append(i)
        return found


#Test code:

#[tag, class]
lieferzeitTag =['span', ['stock-green', 'stock-orange', 'stock-red']]
priceOfItemTag = ['span', 'product-price-amount']

#[tag, text]
nadelStaerkeTagString = ['td', 'Nadelstärke']
ZusammenstellungTagString = ['td', 'Zusammenstellung']



#create Object of scrape
wollplatz = WebPageScraper(searchItems, searchLinkWollplatz)


existingItemList = wollplatz.getFoundItems()

#saving params of found items into lists
priceList = wollplatz.scrapeForClass(priceOfItemTag[0], priceOfItemTag[1])
lieferbarkeit = wollplatz.scrapeForClass(lieferzeitTag[0], lieferzeitTag[1])
Nadelstaerken = wollplatz.scrapeInTable(nadelStaerkeTagString[0], nadelStaerkeTagString[1])
Zusammenstellung = wollplatz.scrapeInTable(ZusammenstellungTagString[0], ZusammenstellungTagString[1])

#building the json string:
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

#writing jsonString into File, overwrite if there is content in the file, creates file if it is not found.
jFile = open('data.json', 'w')
jFile.write(FinalJSONString)
jFile.close();