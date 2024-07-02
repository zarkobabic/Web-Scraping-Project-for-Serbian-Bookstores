from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pszWebScrapperAndCrawler.items import BookItem
import re

class pszBigzSpider(CrawlSpider):
    name = "pszBigzSpider"
    allowed_domains = ['bigzknjizara.rs']
    start_urls = ["https://bigzknjizara.rs/"]
    stop_condition = 0
    

    rules = (
        Rule(LinkExtractor(allow=("kategorija",), deny=("kategorija/skolski-pribor", "kategorija/poklon-program"))),
        Rule(LinkExtractor(allow=("pocetna",)), callback="parse_book_page")
    )

    def find_year(self, text):
        pattern = r"Godina izdanja: (\d{4})\."
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
        
    def find_number_of_pages(self, text):
        pattern = r"Broj strana: (\d+)"
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
        else:
            return None
        
    def find_binding_type(self, text):
        pattern = r"Povez: (.+)"
        match = re.search(pattern, text)
        if match:
            if(match.group(1).lower().rstrip() == "meki"): #standardizujemo sa lagunom
                return "mek"
            elif(match.group(1).lower().rstrip() == "tvrdi"): #standardizujemo sa lagunom
                return "tvrd"
            else:
                return match.group(1).lower().rstrip()
        else:
            return None

    def find_format_height(self, text):
        pattern = r"Format: (\d+(?:\.\d+)?) x (\d+(?:\.\d+)?)"
        match = re.search(pattern, text)
        if match:
            height = float(match.group(2))
            return height
        else:
            return None
        
    def find_format_width(self, text):
        pattern = r"Format: (\d+(?:\.\d+)?) x (\d+(?:\.\d+)?)"
        match = re.search(pattern, text)
        if match:
            width = float(match.group(1))
            return width
        else:
            return None

    def transform_price(self, price_str):
        #menja tacku posle hiljada ni sa cim
        price_str = price_str.replace('.', '')
        #menja zarez u tacku kako bi se formirao dobar decimalni broj za bazu
        price_str = price_str.replace(',', '.')
        price_float = float(price_str)
        return price_float
    

    def check_is_name(self, string_to_check):
        pattern = r"^[A-Z][a-z]*(?: [A-Z][a-z]*)*$"
        match = re.match(pattern, string_to_check)
        return bool(match)

    def parse_authors(self, authors_string):
        authors_array = authors_string.split(", ")
        authors_array_final = []
        for item in authors_array:
            item_temp = item.rstrip().lstrip()
            temp = item_temp.split() #Ako ima vise od par razmaka u splitovanom tekstu po zarezu, i ne pocinje svaka rec velikim slovom za ime, onda je neki tekst o autorima a ne autori, nekonzistentno je na sajtu
            if self.check_is_name(item_temp) and len(temp) <= 5:
                authors_array_final.append(item_temp)

        return authors_array_final
                


    # naziv knjige, autori, zanr/kategorija, izdavac, godina izdanja, broj strana, tip poveza, format, opis, cena. 
    def parse_book_page(self, response):

        book_item = BookItem()

        description_all_separate_elements_in_array = response.css(".woocommerce-Tabs-panel--description *::text").getall()
        book_item["description"] = ' '.join(element.replace('\r', "").replace('\n',"").replace('\r\n', "").rstrip().lstrip() for element in description_all_separate_elements_in_array if element.strip()).replace("  "," ").replace(" .", ".").replace('„ ',"„") if description_all_separate_elements_in_array else None
        book_item["title"] = response.css(".entry-title::text").get().rstrip().replace('\n\t', '') if response.css(".entry-title::text").get() else None #rstrip() uklanja sve razmake sa kraja stringa
        #woocommerce-Tabs-panel--ux_custom_tab
        book_item["authors"] = self.parse_authors(response.css(".woocommerce-Tabs-panel--ux_custom_tab::text").get().replace("\n" , "").replace("\t", "")) if response.css(".woocommerce-Tabs-panel--ux_custom_tab::text").get() else []
        book_item["genres"] = response.css(".posted_in a::text").getall()
        book_item["publisher"] = response.css(".tagged_as a::text").get().lower() if response.css(".tagged_as a::text").get() else None
        
        info_string = ' '.join(response.css(".woocommerce-Tabs-panel--description *::text").getall())

        book_item["year"] = self.find_year(info_string)
        book_item["number_of_pages"] = self.find_number_of_pages(info_string)
        book_item["cover_binding"] = self.find_binding_type(info_string)
        book_item["format_height"] = self.find_format_height(info_string)
        book_item["format_width"] = self.find_format_width(info_string)
        book_item["price"] = self.transform_price(response.css(".product-page-price bdi::text").getall()[0]) if response.css(".product-page-price bdi::text").getall() else None

        if book_item["publisher"] != "laguna": #ne zelimo da dodajemo lagunine knjige, vec postoje u bazi za lagunu 
            self.stop_condition += 1
            if self.stop_condition > 20000:
                self.crawler.engine.close_spider(self, 'Item count exceeded 20000')
                return
            yield book_item

        