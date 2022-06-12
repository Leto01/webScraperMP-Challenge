from unittest import TestCase
from main import WebPageScraper

searchItems = ['DMC-Natura-XL',
               'Drops-Safran',
               'Drops-Baby-Merino-Mix',
               'Hahn-Alpacca-Speciale',
               'Stylecraft-Special-double-knit'
               ]
link = 'https://www.wollplatz.de/{}'

class TestWebPageScraper(TestCase):
    def setUp(self):
        self.webPageScraper = WebPageScraper(searchItems, link)

class TestInit(TestWebPageScraper):
    def test_init(self):
        self.assertEqual(self.webPageScraper.getFoundItems(), ['DMC-Natura-XL',
               'Drops-Safran',
               'Drops-Baby-Merino-Mix'])

    def test_no_params_in_scrapeInTable(self):
        self.assertEqual(self.webPageScraper.scrapeInTable(), [])

    def test_no_params_in_scrapeForClass(self):
        self.assertEqual(self.webPageScraper.scrapeForClass(), [])

    def test_empty_item_list(self):
        self.webPageScraper = WebPageScraper([], link)
        self.assertEqual(self.webPageScraper.getFoundItems(), [])

    def test_empty_link_string(self):
        #fails
        self.webPageScraper = WebPageScraper(searchItems, '')
        self.assertEqual(self.webPageScraper.search(), None)
