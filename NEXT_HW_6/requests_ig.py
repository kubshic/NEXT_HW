from bs4 import BeautifulSoup as bs
from openpyxl import Workbook
from datetime import datetime
import requests

url='https://tickets.interpark.com/contents/genre/concert'

try:
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code ==200:
        html_text = response.text
        
        soup = bs(response.text, 'html.parser')
        # print(soup)
        
        title = soup.find_all(class_='TicketItem_goodsName__Ju76j')
        title = list(map(lambda x: x.text.strip(), title))
        print(title)
        
        place = soup.select('.TicketItem_placeName__ls_9C')
        place = list (map(lambda x: x.text, place))
        print(place)
        
        date = soup.select('.TicketItem_playDate__5ePr2')
        date = list (map(lambda x: x.text, date))
        print(date)
        
        wb = Workbook()
        ws = wb.active
        
        ws.append(["순위", "제목", "장소", "날짜"])
        
        for i, (title, place, date) in enumerate(zip(title, place, date), start=1):
            ws.append([i, title, place, date])
        
        today = datetime.now().strftime('%Y%m%d')
        
        filename = f'hot_concerts_{today}.xlsx'
        wb.save(filename)
        print(f"엑셀 파일 저장 완료: {filename}")
    
    else:
        print(f"Error: HTTP 요청 실패. 상태 코드: {response.status_code}")
    
except requests.exceptions.RequestException as e:
    print(f"Error: 요청 중 오류 발생. 오류 메세지: {e}")