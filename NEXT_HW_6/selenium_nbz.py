from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv

# 크롬 웹드라이버 경로 지정
chromedriver_path = "C:\\Users\\ddkkg\\Documents\\NEXT\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

# 크롬 캐시 남길 폴더 지정
user_data_dir = "C:\\Users\\ddkkg\\Documents\\NEXT\\Crawling"

chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
service = Service(executable_path=chromedriver_path)

# ChromeDriver에 사용자 데이터 디렉토리와 함께 옵션 전달
driver = webdriver.Chrome(service=service, options=chrome_options)

# 넘버즈인 웹페이지 접속하기
driver.get('https://numbuzin.com/')

# 스크롤 두 번 내리기
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(1)
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(1)

# 넘버즈인 1번토너 클릭
chartbtn = driver.find_element(By.XPATH, '//*[@id="Map"]/area[4]')
chartbtn.click()
time.sleep(1)

# 스크롤 한 번 내리기
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(1)

# 상품후기 클릭
chartbtn = driver.find_element(By.XPATH, '//*[@id="detail"]/div[1]/ul/li[2]/a')
chartbtn.click()
time.sleep(1)

# csv저장하기
# today = datetime.now().strftime('%Y%m%d')

# file = open(f'{today}nbz.csv', mode="w", newline='')
# writer = csv.writer(file)
# writer.writerow(["리뷰 내용"])

# 10번까지 리뷰 가져오기
for i in range(1, 11):
    # 리뷰 텍스트 가져오기
    review_element = driver.find_element(By.XPATH,
                                         f'/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/div[2]/div[1]/div/div[{i}]/div[1]/div/div[1]')
    review_text = review_element.text

    # '..더보기' 버튼 클릭
    more_button = review_element.find_elements(By.XPATH, './/a/strong[contains(text(), "더보기")]')
    if more_button:
        more_button[0].click()
        time.sleep(2)
        review_element = driver.find_element(By.XPATH,
                                         f'/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/div[2]/div[1]/div/div[{i}]/div[1]/div/div[2]')
        review_text = review_element.text

    print(review_text)
    print()

    # CSV 파일에 리뷰 텍스트 기록
    # writer.writerow([review_text])

# 나머지 페이지들에 대한 반복
for page in range(2, 7):  # 2번째 페이지부터 6번째 페이지까지
    try:
        chartbtn = driver.find_element(By.XPATH, f'//*[@id="delivery"]/div[2]/div[1]/div/div[11]/ul/li[{page}]/a')
        chartbtn.click()
        


        # 페이지 로드될 때까지 잠시 대기
        time.sleep(3)  # 페이지 로드 속도 및 대기 시간을 조정해야 할 수 있습니다.

        # 10번까지 리뷰 가져오기
        for i in range(1, 11):
            # 리뷰 텍스트 가져오기
            review_element = driver.find_element(By.XPATH,
                                                 f'/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/div[2]/div[1]/div/div[{i}]/div[1]/div/div[1]')
            review_text = review_element.text

            # '..더보기' 버튼 클릭
            more_button = review_element.find_elements(By.XPATH, './/a/strong[contains(text(), "더보기")]')
            if more_button:
                more_button[0].click()
                time.sleep(2)
                review_element = driver.find_element(By.XPATH,
                                         f'/html/body/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/div[2]/div[1]/div/div[{i}]/div[1]/div/div[2]')
                review_text = review_element.text

            print(review_text)
            print()

            # CSV 파일에 리뷰 텍스트 기록
            # writer.writerow([review_text])
            
    except:
        print("다음 페이지 버튼을 찾을 수 없습니다.")
        break

# file.close()
