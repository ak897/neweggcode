from bs4 import BeautifulSoup
import requests, re
import csv

class Scraper:

    def __init__(self):
        self.pageUrl = 'https://www.newegg.com/p/pl?N=100897483%201065556566&PageSize=96&page='
        self.itemUrl = 'https://www.newegg.com/velztorm-mini-pilum-mt/p/3D5-000W-0U2Y0?Item='
        self.pageNumber = 6;
        self.pageItems = 0;



    def listItems(self):
        for page in range(self.pageNumber):
            response = requests.get(self.pageUrl + str(page+1))
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('div', {"class": "item-cell"})
            self.pageItems = len(results)
            if (page == 6):
                self.pageItems = 20;
            for item in range(self.pageItems):
                self._productDetails(results[item])


    def _productDetails(self,item):
        # item = re.sub(r'\s+', ' ', results[j].get_text(" "))
        # itemID = re.search('Item #: (.*) Return Policy:', item)
        itemID = item.find('div', {"class": "item-container"}).get("id")
        print(itemID)
        itemResponse = requests.get(self.itemUrl + itemID)
        itemSoup = BeautifulSoup(itemResponse.content, 'html.parser')
        self._CSV(
            self._extract_title(itemSoup),
            self._extract_description(itemSoup),
            self._extract_price(itemSoup),
            self._extract_rating(itemSoup),
            self._extract_seller(itemSoup),
            self._extract_img(itemSoup))


    def _notNone(self,property):
        if property:
            return property
        else:
            return 'N/A'

    def _extract_title(self, itemSoup):
        title = itemSoup.find('h1', {"class": "product-title"}).get_text()
        return self._notNone(title)


    def _extract_description(self, itemSoup):
        description = itemSoup.find('div', {"class": "product-bullets"}).get_text()
        return self._notNone(description)

    def _extract_price(self, itemSoup):
        price = itemSoup.find('div', {"class": "product-price"}).get_text()
        return self._notNone(price)

    def _extract_rating(self, itemSoup):
        rating = itemSoup.find('div', {"class": "product-rating"})
        try:
            ratingTitle = rating.find('i',{"class": "rating"})['title']
        except:
            ratingTitle = "N/A";
        return self._notNone(ratingTitle)

    def _extract_seller(self, itemSoup):
        seller = itemSoup.find('div', {"class": "product-seller"})
        sellerTitle = seller.find('a',{"class": "popover-question"})['title']
        return self._notNone(sellerTitle)

    def _extract_img(self, itemSoup):
        image = itemSoup.find('div', {"class": "swiper-zoom-container"})
        imageLink = image.find('img').get('src')
        return self._notNone(imageLink)

    def _CSV(self,PT,PD,PFP,PR,SN,MIU):
        with open('newegg.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            fieldnames = ["Product Title","Product Description","Product Final Pricing","Product Rating","Seller Name", "Main Image URL"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            if(PT == "N/A" and PD=="N/A" and PFP=="N/A" and PR =="N/A" and SN=="N/A" and MIU =="N/A"):
                self.pageNumber = 0;
                self.pageItems = 0;

            writer.writerow({
                'Product Title': PT,
                'Product Description': PD,
                'Product Final Pricing': PFP,
                'Product Rating': PR,
                'Seller Name': SN,
                'Main Image URL': MIU,
            })



if __name__ == '__main__':
    list = Scraper()
    list.listItems()
