from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager


# 크롬 캐시 남길 폴더 지정
user_data_dir = "C:\\Users\\ddkkg\\Documents\\NEXT\\Crawling"

chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")

# Chrome driver 자동 업데이트 및 초기화
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 링크
driver.get('https://www.youtube.com/watch?v=rt3jzNaG3sY')

# 정렬버튼까지 스크롤
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(1)
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
time.sleep(1)

# 정렬버튼 클릭
sortbtn = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/div[2]/span/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/div/tp-yt-paper-button')
sortbtn.click()
time.sleep(1)

# 최신순 클릭
recent = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/div[2]/span/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/a[2]/tp-yt-paper-item')
recent.click()
time.sleep(1)

# 스크롤 일시정지 타임 지정
SCROLL_PAUSE_TIME = 2

# 처음 페이지 높이 가져오기
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    # 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    
    # 대기
    time.sleep(SCROLL_PAUSE_TIME)
    
    # 새로운 높이 가져오기
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    # 새로운 높이와 마지막 높이 비교
    if new_height == last_height:
        # 추가 대기 시간을 주어 댓글이 모두 로드될 수 있도록 함
        time.sleep(5)
        break
    last_height = new_height

# 추가 대기 시간 (스크롤이 끝난 후 댓글이 로드되는 시간을 기다림)
time.sleep(10)

# csv저장하기
today = datetime.now().strftime('%Y%m%d')
file_name = f'{today}simtohl.csv'

with open(file_name, mode="w", newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["최신순 번호", "핸들", "댓글 내용"])

    for i in range(2, 738):  # 고정 댓글 제외 2번 댓글부터 현재 댓글 개수까지 크롤링
        try:
            count = i-1 # 고정 댓글 제외하여 2번 댓글을 1번으로 프린트
            handle_xpath = driver.find_element(By.XPATH,f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-view-model/div[3]/div[2]/div/div[2]/h3/a/span')
            comment_xpath = driver.find_element(By.XPATH,f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-view-model/div[3]/div[2]/ytd-expander/div/yt-attributed-string/span')
            
            handle = handle_xpath.text
            comment = comment_xpath.text
            
            writer.writerow([count, handle, comment])
        
        except Exception as e:
            print(f"Error at comment {i}: {e}")
            continue
        
print(f"Comments saved to {file_name}")

driver.quit()
