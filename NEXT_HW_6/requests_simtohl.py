import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 유튜브 영상 링크
url = 'https://www.youtube.com/watch?v=rt3jzNaG3sY'

# requests를 사용하여 페이지 가져오기
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 사용자가 직접 스크롤을 마치기 전까지 기다리기
input("스크롤을 마치셨으면 아무 키나 눌러주세요...")

# 댓글 요소 찾기
comments = soup.find_all('yt-formatted-string', class_='style-scope ytd-comment-renderer')

# csv 저장
today = datetime.now().strftime('%Y%m%d')
file_name = f'{today}simtohl.csv'

with open(file_name, mode="w", newline='', encoding='UTF-8') as file:
    writer = csv.writer(file)
    writer.writerow(["핸들", "댓글 내용"])

    for comment in comments:
        try:
            handle = comment.find('a', class_='yt-simple-endpoint style-scope yt-formatted-string').text
            comment_text = comment.find('span', class_='style-scope yt-formatted-string').text
            
            writer.writerow([handle, comment_text])
        
        except Exception as e:
            print(f"Error: {e}")
            continue
        
print(f"Comments saved to {file_name}")
