from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pszWebScrapperAndCrawler.items import BookItem
import re
class pszMakartSpider(CrawlSpider):
    name = "pszMakartSpider"
    allowed_domains = ['makart.rs']
    start_urls = ["https://www.makart.rs/knjige"]
    stop_condition = 0

    rules = (
        Rule(LinkExtractor(allow=("knjige/zanrovi",))),
        Rule(LinkExtractor(allow=(r'.*knjige/knjiga.*',), deny=("knjige/zanrovi","knjige/autori")), callback="parse_book_page")
    )


    def find_publisher(self, info_array):
        for index, info in enumerate(info_array):
            if info == 'Izdavač:':
                if index + 1 < len(info_array):
                    return info_array[index + 1].lower().rstrip()
                else:
                    return None
        return None

    def find_year(self, info_array):
        for index, info in enumerate(info_array):
            if info == 'Godina izdanja:':
                if index + 1 < len(info_array):
                    return info_array[index + 1]
                else:
                    return None
        return None

    def find_binding_type(self, info_array):
        for index, info in enumerate(info_array):
            if info == 'Povez:':
                if index + 1 < len(info_array):
                    if info_array[index + 1].lower().rstrip() == "broširani povez":
                        return "broš"
                    elif info_array[index + 1].lower().rstrip() == "tvrd povez":
                        return "tvrd"
                    else:
                        return info_array[index + 1].lower().rstrip()
                else:
                    return None
        return None
    
    def find_format(self, info_array):
        for index, info in enumerate(info_array):
            if info == 'Format:':
                if index + 1 < len(info_array):
                    return info_array[index + 1]
                else:
                    return None
        return None

    def find_number_of_pages(self, info_array):
        for index, info in enumerate(info_array):
            if info == 'Broj strana:':
                if index + 1 < len(info_array):
                    return info_array[index + 1]
                else:
                    return None
        return None
    
    def transform_price(self, price_str):
        #menja tacku posle hiljada ni sa cim
        price_str = price_str.replace('.', '')
        #menja zarez u tacku kako bi se formirao dobar decimalni broj za bazu
        price_str = price_str.replace(',', '.')
        price_float = float(price_str)
        return price_float

    # naziv knjige, autori, zanr/kategorija, izdavac, godina izdanja, broj strana, tip poveza, format, opis, cena. 
    def parse_book_page(self, response):

        book_item = BookItem()

        book_item["title"] = response.css(".tg-booktitle h1::text").get().rstrip() if response.css(".tg-booktitle h1::text").get() else None #rstrip() uklanja sve razmake sa kraja stringa
        book_item["authors"] = response.css(".tg-productcontent span.tg-bookwriter a::text").getall()
        book_item["genres"] = response.css(".tg-bookscategories a::text").getall()
        info_array = response.css(".tg-sidebar .tg-productinfo *::text").getall()
        
        book_item["publisher"] = self.find_publisher(info_array)
        book_item["year"] = self.find_year(info_array)
        book_item["number_of_pages"] = self.find_number_of_pages(info_array)
        book_item["cover_binding"] = self.find_binding_type(info_array)

        info_format = self.find_format(info_array).split()[0] if self.find_format(info_array) else None

        if(info_format):
            pattern = r"(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)"
            match = re.search(pattern, info_format)
            if match: #ukoliko ima dva broja zadovoljice ovo
                book_item["format_width"] = float(match.group(1))
                book_item["format_height"] = float(match.group(2))
            else: #ako ima samo jedan broj onda je kvadratna
                pattern_two = r"(\d+(?:\.\d+)?)cm"
                match_two = re.search(pattern_two, info_format)
                if match_two:
                    book_item["format_width"] = float(match.group(1))
                    book_item["format_height"] = float(match.group(1))
                else:
                    book_item["format_width"] = float(info_format)
                    book_item["format_height"] = float(info_format)
        else:
            book_item["format_width"] = None
            book_item["format_height"] = None

        book_item["price"] = self.transform_price(response.css(".tg-productcontent .tg-bookprice ins::text").get().split()[0]) if response.css(".tg-productcontent .tg-bookprice ins::text").get() else None
        
        description_all_separate_elements_in_array = response.css(".tg-description *::text").getall()
        book_item["description"] = ' '.join(element.replace('\r', "").replace('\n',"").replace('\r\n', "").rstrip().lstrip() for element in description_all_separate_elements_in_array if element.strip()).replace("  "," ").replace(" .", ".").replace('„ ',"„") if description_all_separate_elements_in_array else None

        if book_item["publisher"] != "laguna": #ne zelimo da dodajemo lagunine knjige, vec postoje u bazi za lagunu 
            self.stop_condition += 1
            if self.stop_condition >= 20000:
                self.crawler.engine.close_spider(self, 'Item count exceeded 20000')
                return
            yield book_item