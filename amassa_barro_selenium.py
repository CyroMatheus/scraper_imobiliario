import random
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
import time, pprint, json, os, requests
 
class navegator:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--start-maximized")
        self.chrome = webdriver.Chrome(options = options)
        self.links = json.load(open(f'{os.getcwd()}/farao/links.json'))
        self.links_used = json.load(open(f'{os.getcwd()}/farao/links_used.json'))
        self.info_ads = json.load(open(f'{os.getcwd()}/farao/data_ads.json'))
    
    def get_info_by_link(self):
        for key, value in enumerate(self.links):
            if not self.links[value] in self.links_used:
                self.chrome.get(self.links[value])
                print(value)
                self.search_element('//ul/li/img')
                img_links = list()
                imgs = self.chrome.find_elements(By.XPATH, '//ul/li/img')
                list_diferences = list()
                for img_k, img_v in enumerate(imgs):
                    img_links.append(img_v.get_attribute('src'))
                if "zap" in self.links[value]:
                    m2 = self.chrome.find_element(By.XPATH, '//span[@itemprop="floorSize"]').text[:-2]
                    ad_value = self.chrome.find_element(By.XPATH,'//li[@class="price__item--main text-regular text-regular__bolder"]').text.replace(".", "").replace("R$", "").replace(" ", "")
                    rooms = self.chrome.find_element(By.XPATH, '//span[@itemprop="numberOfRooms"]').text.split(" ")
                    rooms = rooms[0]
                    if int(rooms) > 1:
                        suites = int(rooms) // 2
                    else:
                        suites = int(rooms)
                    try:
                        garage = self.chrome.find_element(By.XPATH,'//li[@class="feature__item text-regular js-parking-spaces"]/span[2]').text.split(" ")
                        garage = garage[0]
                    except:
                        garage = 0
                    bathrooms = self.chrome.find_element(By.XPATH,'//span[@itemprop="numberOfBathroomsTotal"]').text.split(" ")
                    bathrooms = bathrooms[0]
                    condominium = self.chrome.find_element(By.XPATH,'//li[@class="price__item condominium color-dark text-regular"]/span[@class="price__value"]').text
                    iptu = self.chrome.find_element(By.XPATH, '//li[@class="price__item iptu color-dark text-regular"]/span[@class="price__value"]').text
                elif "vivareal" in self.links[value]:
                    m2 = self.chrome.find_element(By.XPATH, '//li[@title="Área"]').text[:-2]
                    ad_value = self.chrome.find_element(By.XPATH,'//h3[@class="price__price-info js-price-sale"]').text.replace(".", "").replace("R$", "").replace(" ", '')
                    rooms = self.chrome.find_element(By.XPATH, '//li[@title="Quartos"]').text.split(" ")
                    rooms = rooms[0]
                    bathrooms = self.chrome.find_element(By.XPATH,'//li[@title="Banheiros"]').text
                    try:
                        bath_suit_splited = bathrooms.split("\n")
                        print(bath_suit_splited)
                        suites = bath_suit_splited[1].split(" ")
                        suites = suites[0]
                        bathrooms = bath_suit_splited[0].split(" ")
                        bathrooms = bathrooms[0]
                        garage = self.chrome.find_element(By.XPATH, '//li[@title="Vagas"]').text.split(" ")
                        garage = garage[0]
                    except:
                        suites = int(rooms)//2
                        bathrooms = int(rooms)//2
                        garage = int(rooms)//2 if int(rooms)//2 > 1 else 1
                        
                    try:
                        condominium = self.chrome.find_element(By.XPATH, '//span[@class="price__list-value condominium js-condominium missing-value"]').text
                    except:
                        condominium = 0
                        
                    try:
                        iptu = self.chrome.find_element(By.XPATH, '//span[@class="price__list-value iptu js-iptu missing-value"]').text
                    except:
                        iptu = iptu = random.randint(58, 172)

                n_path = len(os.listdir(os.getcwd() + '/farao/images_ads'))
                self.info_ads[value] = {
                    "m2": m2,
                    "value": ad_value,
                    "rooms": rooms,
                    "suites": suites,
                    "garage": garage,
                    "bathrooms": bathrooms,
                    "iptu": iptu,
                    "condominium": condominium,
                    "imgs_folder": f'{os. getcwd()}/ad_{n_path}',
                    "original_link": self.links[value],
                    "posted": False
                }
                self.save_imgs(f'{os.getcwd()}/farao/images_ads/ad_{n_path}', img_links)
                self.links_used.append(self.links[value])
                self.w_json(f"{os.getcwd()}/farao/data_ads", self.info_ads)
                self.w_json(f"{os.getcwd()}/farao/links_used", self.links_used)
                print(value, self.info_ads[value])

    def save_imgs(self, path, links):
        os.mkdir(path)
        for key_l, value_l in enumerate(links):
            response = requests.get(value_l)
            file = open(f"{path}/img_{key_l}{value_l[-4:]}", "wb")
            file.write(response.content)
            file.close()
    
    def search_element(self, element):
        while len(self.chrome.find_elements(By.XPATH, element)) == 0:
            time.sleep(0.01)
    
    def w_json(self, file, list):
        with open(f"{file}.json", "w") as arquivo:
            json.dump(list, arquivo, indent=4)

def run():
    navegador = navegator()
    navegador.get_info_by_link()

run()