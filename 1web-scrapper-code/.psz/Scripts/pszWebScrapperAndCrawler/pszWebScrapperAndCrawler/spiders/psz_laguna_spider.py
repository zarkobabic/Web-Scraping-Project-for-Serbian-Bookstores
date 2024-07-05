from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pszWebScrapperAndCrawler.items import BookItem

class pszLagunaSpider(CrawlSpider):
    name = "pszLagunaSpider"
    allowed_domains = ['laguna.rs']
    start_urls = ["https://laguna.rs/s_laguna_knjige_spisak_naslova.html"]
    stop_condition = 0

    rules = (
        Rule(LinkExtractor(allow=(r'.*zanr.*',))),
        Rule(LinkExtractor(allow=(r'.*knjiga.*',)), callback="parse_book_page")
    )

    # naziv knjige, autori, zanr/kategorija, izdavac, godina izdanja, broj strana, tip poveza, format, opis, cena. 
    def parse_book_page(self, response):

        book_item = BookItem()

        description_all_separate_elements_in_array = response.css("#oknjizitab *::text").getall()
        book_item["description"] = ' '.join(element.replace('\r', "").replace('\n',"").replace('\r\n', "").rstrip().lstrip() for element in description_all_separate_elements_in_array if element.strip()).replace("  "," ").replace(" .", ".").replace('„ ',"„") if description_all_separate_elements_in_array else None
        book_item["title"] = response.css("#sadrzaj div h1.naslov::text").get().rstrip() if response.css("#sadrzaj div h1.naslov::text").get() else None #rstrip() uklanja sve razmake sa kraja stringa
        book_item["authors"] = response.css("#sadrzaj > div:nth-child(1) h2 a::text").getall()
        book_item["genres"] = response.css(".podatak h3 a::text").getall()
        book_item["publisher"] = "laguna"
        book_item["year"] = response.css("#podaci-korica > div:nth-child(5)::text").get().split()[-1].strip('.') if response.css("#podaci-korica > div:nth-child(5)::text").get() else None
        book_item["number_of_pages"] = response.css("#podaci-korica > div:nth-child(2)::text").get()
        book_item["cover_binding"] = response.css("#podaci-korica > div:nth-child(4)::text").get().lower() if response.css("#podaci-korica > div:nth-child(4)::text").get() else None
        book_item["format_width"] = response.css("#podaci-korica > div:nth-child(1)::text").get().split('x')[0] if response.css("#podaci-korica > div:nth-child(1)::text").get() else None
        book_item["format_height"] = response.css("#podaci-korica > div:nth-child(1)::text").get().split('x')[1].split()[0] if response.css("#podaci-korica > div:nth-child(1)::text").get() else None
        book_item["price"] = response.css(".cena p::text").get().split()[0] if response.css(".cena p::text").get() else None

        #ukoliko knjiga jos nije izasla u prodaju godina ce biti isbn zapravo jer se tako pomera css na stranici za jedan, pa te iteme necemo obradjivati jer nam ne znace u istrazivanju - nemaju cenu
        if(len(book_item["year"]) <= 4):
            self.stop_condition += 1
            if self.stop_condition > 20000:
                self.crawler.engine.close_spider(self, 'Item count exceeded 20000')
                return
            yield book_item

        