import urllib.request
from bs4 import BeautifulSoup
import json, requests, os

class navegator:
    def __init__(self):
        self.links = json.load(open('links.json'))
        self.links_used = json.load(open('links_used.json'))
        self.info_ads = dict()
        self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.headers = {'User-Agent': self.user_agent}

    def open_link(self):
        tags = {
            "zapimoveis": {
                "m2": {
                    "element": "span",
                    "prop": "itemprop",
                    "xpath": "floorSize"
                },
                "value_ad": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "price__item--main text-regular text-regular__bolder"
                },
                "rooms": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "feature__item text-regular js-bedrooms"
                },
                "garage": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "feature__item text-regular js-parking-spaces"
                },
                "bathrooms": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "icon icon-color--dark icon-size--regular"
                },
                "condominium": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "price__item condominium color-dark text-regular"
                },
                "iptu": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "price__item iptu color-dark text-regular"
                },
            },
            "vivareal": {
                "m2": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "features__item features__item--area js-area"
                },
                "value_ad": {
                    "element": "h3",
                    "prop": "class",
                    "xpath": "price__price-info js-price-sale"
                },
                "rooms": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "features__item features__item--bedroom js-bedrooms"
                },
                "garage": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "features__item features__item--parking js-parking"
                },
                "bathrooms": {
                    "element": "li",
                    "prop": "class",
                    "xpath": "features__item features__item--bathroom js-bathrooms"
                },
                "condominium": {
                    "element": "span",
                    "prop": "class",
                    "xpath": "price__list-value condominium js-condominium missing-value"
                },
                "iptu": {
                    "element": "span",
                    "prop": "class",
                    "xpath": "price__list-value iptu js-iptu missing-value"
                },
            }
        }
        for key, value in enumerate(self.links):
            if not self.links[value]["__link"] in self.links_used:
                if "zapimoveis" in self.links[value]["__link"]:
                    tag = "zapimoveis"
                if "vivareal" in self.links[value]["__link"]:
                    tag = "vivareal"
                data_ad = self.get_data(self.links[value]["__link"], int(value)+1, tags[tag])
                if data_ad != False and data_ad != None:
                    self.info_ads[value] = data_ad
                    self.w_json('/home/cyro/Documentos/palacis/farao/imgs_ads/ads_0', self.info_ads)
                    self.w_json('/home/cyro/Documentos/palacis/farao/ads_0', self.info_ads)
                    # print("\n" ,self.info_ads[value])
                    print(f"{int(value)+1} - all data saved from link:{self.links[value]}")
                else:
                    print(f"{int(value)+1} - link broked:{self.links[value]}")
                self.links_used.append(self.links[value])
                self.w_json("/home/cyro/Documentos/palacis/farao/links_used", self.links_used)

    def get_data(self, link, key_folder, tags):
        ads = {
            "m2": None,
            "value_ad": None,
            "rooms": None,
            "suites": None,
            "garage": None,
            "bathrooms": None,
            "iptu": None,
            "condominium": None,
            "imgs_folder": f"/home/cyro/Documentos/palacis/farao/imgs_ads/ads_{key_folder}",
            "original_link": link,
            "posted": False
        }
        try:
            r = requests.get(f'{link}')
            if r.status_code != 404:
                request = urllib.request.Request(link, None, self.headers)  # The assembled request
                response = urllib.request.urlopen(request)
                html = response.read()
                bs4 = BeautifulSoup(html, 'html.parser')

                img_links = list()
                for img in bs4.find_all('img', attrs={'class':'carousel__image'}):
                    img_links.append(img["src"])
                self.save_imgs(ads["imgs_folder"], img_links)

                for key_ad, value_ad in enumerate(tags):
                    ads[value_ad] = self.get_text(tags[value_ad]["element"], tags[value_ad]["prop"], tags[value_ad]["xpath"], bs4)
                if int(ads["rooms"]) > 1:
                    ads["suites"] = int(ads["rooms"]) // 2
                else:
                    ads["suites"] = int(ads["rooms"])
                self.w_json(f'{ads["imgs_folder"]}/info_ad_{key_folder}', ads)
                return ads
            else:
                return False
        except Exception as e:
            # print(key_folder, e, link)
            return False

    def save_imgs(self, path, links):
        try:
            os.mkdir(path)
        except:
            pass

        for key_l, value_l in enumerate(links):
            response = requests.get(value_l)
            file = open(f"{path}/img_{key_l+1}{value_l[-4:]}", "wb")
            file.write(response.content)
            file.close()

    def get_text(self, element, prop, value_prop, bs4):
        str_treated = ""
        try:
            brutal_str = bs4.find(element, attrs={prop: value_prop}).get_text()
        except:
            brutal_str = 0

        if "suíte" in str(brutal_str):
            brutal_str = brutal_str.split("\n")
            brutal_str = brutal_str[0]

        if "ão informado" in str(brutal_str):
            str_treated = 0

        if str(brutal_str) != "0":
            for i in range(len(str(brutal_str))):
                if brutal_str[i].isdecimal():
                    str_treated += brutal_str[i]

        return str_treated

    def w_json(self, file, list):
        with open(f"{file}.json", "w") as arquivo:
            json.dump(list, arquivo, indent=4)

def run():
    navegador = navegator()
    navegador.open_link()

run()
