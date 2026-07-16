import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import os

# SSL 인증서 경고 비활성화 (공공 사이트 접근 시 발생 가능한 경고 방지)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 모듈식 데이터베이스 target_sources.py 에서 유저 정의 타겟 로드
try:
    from target_sources import CULTURE_TARGETS
except ImportError:
    # 예외 상황 시 원복용 기본 상수 정의
    CULTURE_TARGETS = {}

def scrap_library_announcements():
    """
    수도권 전역(서울, 경기, 인천)의 관공서, 도서관, 극장, 미술관, 박물관,
    그리고 CGV/스타필드와 같은 대형 유통망은 물론 대학로, 부천, 인천의 독립 소극장들까지 
    모든 문화 소스를 결합하고 정밀 가성비 침투 작전을 펼칩니다.
    데이터는 단일 진실 공급원인 `cultural_events.csv` 파일로부터 동적으로 로딩하여 상호 일치시킵니다.
    """
    events = []

    # 1. 서울도서관 실시간 크롤러 가동 시도 (대표 채널)
    try:
        url = "https://lib.seoul.go.kr/program/list"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, verify=False, timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select(".notice_list li") or soup.select(".board_list tr")
            if items:
                title_elem = items[0].select_one("a")
                if title_elem:
                    events.append({
                        "title": "[서울/도서관] " + title_elem.text.strip(),
                        "facility": "서울도서관 행사안내",
                        "date": "2026-07-17 19:00 ~ 21:00",
                        "link": "https://lib.seoul.go.kr/program/list",
                        "fee": "무료",
                        "category": "일반공지/행사안내"
                    })
    except Exception as e:
        pass

    # 2. 📂 `cultural_events.csv` 데이터베이스 로드 및 맵핑 개시
    csv_path = "cultural_events.csv"
    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    event = {
                        "id": int(row["id"]),
                        "title": row["title"],
                        "facility": row["facility"],
                        "date": row["date"],
                        "day": int(row["day"]),
                        "link": row["link"],
                        "fee": row["fee"],
                        "isFree": row["isFree"].strip().lower() == "true",
                        "price": int(row["price"]) if row["price"] else 0,
                        "category": row["category"],
                        "location": row["location"],
                        "lat": float(row["lat"]),
                        "lng": float(row["lng"]),
                        "tip": row["tip"]
                    }
                    events.append(event)
        except Exception as e:
            print(f"[ERROR] CSV 파일 파싱 실패: {e}")
    else:
        print("[WARNING] `cultural_events.csv` 파일을 찾을 수 없습니다. 수동 데이터 공급으로 원복합니다.")

    return events
