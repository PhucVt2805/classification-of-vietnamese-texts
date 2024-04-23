import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class Collect_Data:
    def __init__(self) -> None:
        self.topic_dictionary = {'the-gioi':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                             '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'kinh-te':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                           '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'doi-song':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                            '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'suc-khoe':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                            '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'gioi-tre':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > div > h3 > a',
                                            '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'giao-duc':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                            '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'van-hoa':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                           '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'giai-tri':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                            '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'xe':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                      '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > a'],
                                'du-lich':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                           '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div.list__viewmore.list__center > a'],
                                'the-thao':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > div > h3 > a',
                                            '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div.list__viewmore.list__center > a'],
                                'cong-nghe-game':['#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div > div > h3 > a',
                                                  '#content > div.list__stream > div > div > div.list__stream-main.list__main_check.list__stream-checkhot > div > div > div.list__viewmore.list__center > a']
                                }

        self.name = ['Thế giới',
                    'Kinh tế',
                    'Đời sống',
                    'Sức khỏe',
                    'Giới trẻ',
                    'Giáo dục',
                    'Văn hóa',
                    'Giải trí',
                    'Xe',
                    'Du lịch',
                    'Thể thao',
                    'Công nghệ - Game']
        
        self.result = {'Tiêu đề': None, 'Danh mục':None}

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Tải thêm nội dung của trang web
    def load_more_content(self, time_load:int, value:list):
        for _ in range(8):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
        show_more_button = self.driver.find_element(By.CSS_SELECTOR, value[1])
        show_more_button.click()
        for _ in range(time_load):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    
    # Hàm viết kết quả ra file csv
    def write(self):
        df = pd.DataFrame(self.result)
        df.to_csv('Data/Data.csv')

    # Hàm lấy dữ liệu từ trang web
    def Get_Data(self):
        data = []
        categorys = []
        for i, (key, value) in enumerate(self.topic_dictionary.items()):
            self.driver.get('https://thanhnien.vn/'+key+'.htm')
            self.load_more_content(600, value)
            topics = self.driver.find_elements(By.CSS_SELECTOR, value[0])
            data += [text.text for text in topics]
            categorys += [self.name[i]]*len(topics)
            self.result['Tiêu đề'] = data
            self.result['Danh mục'] = categorys
            self.write()
            print('Đã viết ra file danh mục: '+self.name[i])

if __name__=='__main__':
    Data = Collect_Data()
    Data.Get_Data()
