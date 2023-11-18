from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging 
import pandas as pd

logging.basicConfig(level=logging.INFO, 
                              format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


class Designer_bot : 
    def __init__(self): 
        self.driver = webdriver.Chrome()
    
    def open_website(self): 
        self.driver.get('https://www.dexigner.com/')
        self.driver.maximize_window()

        # directory page
        directory_button = WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.dexigner.com/directory/']")))
        directory_button.click()

        # web design section
        web_design_button = WebDriverWait(self.driver,3).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='/directory/cat/Web-Design']")))
        web_design_button.click()

        #designers page 
        designers = WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,"//a[@href='/directory/cat/Web-Design/Designers']")))
        designers.click()
    
    def extract_data(self): 
        self.names = []
        self.websites = []
        self.phones = []
        self.descriptions = []
        self.full_address = []

        # Pagination
        pagination = self.driver.find_element(by="xpath", value = "//nav[@id='navdiv']")
        pages = pagination.find_elements(by="xpath", value=".//li")

        # last page
        last_page = int(pages[-2].text)

        current_page = 1

        while current_page <= last_page: 
            # locate each personne
            items = WebDriverWait(self.driver,3).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='listing']")))

            for i in range(len(items)):
                item = items[i]

                name = item.find_element(by='xpath', value=".//h3")
                self.names.append(name.text)
                button = name.find_element(by="xpath", value=".//a")
                button.click()

                try: 
                    website = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,"//p[@class='detailnew']/a"))).text
                except: 
                    website = 'N/A'
                    logger.info(f"No website for the designer {i+1}!!!!!!!!!!")
                
                try:
                    description = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,"//p[contains(@class,'detailnew detaildesc')]"))).text
                except: 
                    description = 'N/A'
                    logger.info(f"No profile description for the designer {i+1}!!!!!!!!!")

                try: 
                    phone = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, "//p[@id='telephone']/a/span"))).text
                except: 
                    phone = 'N/A'
                    logger.info(f"No phone number for the designer {i+1}!!!!!!!!!")

                try: 
                    address = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, "//p[@id='location']"))).get_attribute("textContent")
                except: 
                    address = 'N/A'
                    logger.info(f"No address for the designer {i+1}!!!!!!!!")

                # append to list
                self.websites.append(website)
                self.descriptions.append(description)
                self.phones.append(phone)
                self.full_address.append(address)

                #come back to the main page 
                self.driver.back()

                #relocate
                items = WebDriverWait(self.driver,3).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='listing']")))

            # next page
            current_page += 1

            # Go to the next page if possible
            try: 
                next_page = self.driver.find_element(by="xpath", value="//a[@class='prevnext nextlink']")
                next_page.click()
                logger.info(f"Page {current_page}!!!!!!!!!")
            except:
                logger.warning(f"Last page!!!!!!!!!!!!!!") 
                pass

    def save_to_csv(self):       
        df = pd.DataFrame({'Name':self.names, 'Description':self.descriptions,
                    'Phone':self.phones, 'Website':self.websites, 'Adress':self.full_address})

        df.to_csv('designers.csv')

        self.driver.close()

bot = Designer_bot()
bot.open_website()
bot.extract_data()
bot.save_to_csv()

