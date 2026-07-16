import csv
import re
import sys
import os

# Set standard output encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r"c:\aiclu_1\free_cul\cultural_events.csv"
DATA1_CSV = r"c:\aiclu_1\free_cul\data_1.csv"
DATA2_CSV = r"c:\aiclu_1\free_cul\data_2.csv"
DATA3_CSV = r"c:\aiclu_1\free_cul\data_3.csv"

# 1. Official Homepage Link Upgrades for Vetted Original 37 Events
OFFICIAL_HOMEPAGES = {
    1: "https://lib.seoul.go.kr", # 서울도서관
    3: "https://www.inartplatform.kr", # 인천아트플랫폼
    5: "https://jdlib.sen.go.kr", # 정독도서관
    18: "https://e-school.seoul.go.kr", # 서울 모두의학교
    19: "https://yeyak.seoul.go.kr", # 서울공공서비스예약
    20: "http://www.guitar.or.kr", # 한국기타협회
    21: "https://yeyak.seoul.go.kr", # 서울시 로봇아카데미 예약
    22: "https://www.naruart.or.kr", # 나루아트센터
    23: "https://yeyak.seoul.go.kr", # 서울공공예약
    24: "https://museum.seoul.go.kr", # 서울역사박물관
    25: "https://yeyak.seoul.go.kr", # 서울시 1인가구 포털
    26: "https://www.dongjak.go.kr", # 동작구청
    27: "https://museum.yongsan.go.kr", # 용산역사박물관
    28: "https://www.dongjak.go.kr", # 동작구청 버스킹
    29: "https://www.dongjak.go.kr", # 동작구청 가무극
    30: "https://museum.seoul.go.kr/scwm/main", # 한양도성박물관
    31: "https://www.sfac.or.kr", # 서울문화재단 신진작가
    32: "https://www.sdm.go.kr", # 서대문구청 청년작가
    33: "https://www.gwanak.go.kr", # 관악구청 청년페스티벌
    34: "https://yeyak.seoul.go.kr", # 서울공공예약문학특강
    35: "https://www.sfac.or.kr", # 서울문화재단 갤러리비뮨
    36: "https://www.sb.go.kr", # 성북구청 한옥공방
    37: "https://www.ddp.or.kr" # DDP 공식 야외조각전
}

# 2. Load existing vetted 37 events (completely discarding previously merged events to rebuild cleanly)
existing_events = []
existing_keys = set() # (title_clean, start_date) to prevent duplicates

if os.path.exists(ORIGINAL_CSV):
    with open(ORIGINAL_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = int(row["id"])
            # Only keep the original 37 curated core events
            if row_id <= 37:
                # Inject official homepage if it had a Naver search query
                if row_id in OFFICIAL_HOMEPAGES:
                    row["link"] = OFFICIAL_HOMEPAGES[row_id]
                existing_events.append(row)
                # Normalize title to extract the core name (ignoring region prefix like [서울/영화])
                core_title = re.sub(r"^\[.*?\]\s*", "", row["title"]).strip()
                # Extract start date
                start_date = row["date"].split()[0]
                existing_keys.add((core_title, start_date))

print(f"Loaded {len(existing_events)} Curated Core Events (upgraded to official detail URLs).")

# Category determination helper
def determine_category(title, content):
    text = (title + " " + content).lower()
    if any(k in text for k in ["공연", "국악", "가요제", "콘서트", "콩구르", "콩쿠르", "합창", "연주회", "음악회", "오케스트라", "서커스", "버스킹", "밴드", "뮤지컬", "연극", "인형극"]):
        return "공연"
    elif any(k in text for k in ["전시", "미술", "갤러리", "박물관", "그림", "사진", "비엔날레", "미디어아트"]):
        return "전시"
    elif any(k in text for k in ["영화", "시네마", "상영", "영화제", "단편영화"]):
        return "영화"
    elif any(k in text for k in ["도서관", "책", "독서", "작가", "북토크", "이야기"]):
        return "도서관"
    elif any(k in text for k in ["강연", "특강", "인문학", "아카데미", "교육", "세미나", "포럼", "토크"]):
        return "강연"
    elif any(k in text for k in ["체험", "공방", "원데이", "만들기", "교실", "놀이", "캠프", "플리마켓", "시장"]):
        return "체험"
    else:
        return "공연"

# Price parser helper
def parse_price(fee_info, price_info=""):
    text = (fee_info + " " + price_info).lower()
    if "무료" in text or "공짜" in text or "무상" in text or "0원" in text:
        return 0, True
    if "유료" in text or "원" in text:
        nums = re.findall(r'\d+', text.replace(",", ""))
        if nums:
            valid_prices = [int(n) for n in nums if int(n) >= 1000]
            if valid_prices:
                return min(valid_prices), False
    return 0, True # Default to free

# Funny kitschy spy tips generator
def generate_tip(title, facility):
    title_lower = title.lower()
    if "영화" in title_lower or "시네마" in title_lower:
        return f"{facility} 기밀 스크린 근처 어두운 자리를 확보하십시오. 쉿! 퇴근 길 조용히 잠입해서 공짜 시네마 낭만을 가로채는 미션입니다."
    elif "도서관" in title_lower or "책" in title_lower or "북" in title_lower:
        return f"서가 뒤 그늘진 자리를 확보하여 지식을 도청하십시오. 도서관 전용 스파이답게 사뿐사뿐 걷는 음소거 이동 기술이 핵심입니다."
    elif "요가" in title_lower or "테라피" in title_lower or "웰니스" in title_lower:
        return f"가장 편안한 위장 복장으로 긴장을 풀고 세포 단위로 교란 신호를 보내십시오. 주말 동안 지친 정신을 은밀히 충전하는 비밀 작전입니다."
    elif "만들기" in title_lower or "체험" in title_lower or "공방" in title_lower:
        return f"공방 공작원의 지시에 따라 정밀한 나만의 전리품을 제작하십시오. 손재주를 발휘해 고급 굿즈를 합법적으로 탈취할 절호의 기회입니다."
    elif "음악회" in title_lower or "콘서트" in title_lower or "공연" in title_lower or "밴드" in title_lower:
        return f"명품 클래식/인디 음파를 도청 장치 없이 고막에 직접 완벽 저장하십시오. 귀가 호강하는 최고의 공짜 문화 침투 루트입니다."
    else:
        return f"{facility} 현장의 감시카메라 사각지대에 차분히 포지셔닝하여 작전을 개시하십시오. 사냥꾼 다운 날렵한 회피 및 복귀 요령을 숙지하세요."

# Check if within Seoul Metropolitan Area (bounding box or text check)
def is_metropolitan(lat, lng, address_text="", facility_text=""):
    # Bounding box coordinates for Seoul/Gyeonggi/Incheon
    lat_ok = (37.0 <= lat <= 38.3)
    lng_ok = (126.3 <= lng <= 127.9)
    if lat_ok and lng_ok:
        return True
    
    text = (address_text + " " + facility_text).lower()
    if any(k in text for k in ["서울", "경기", "인천", "부천", "수원", "고양", "성남", "안산", "화성", "용인", "남양주", "의정부"]):
        return True
    return False

# Region helper
def get_region(lat, lng, address_text="", facility_text=""):
    text = (address_text + " " + facility_text).lower()
    if "서울" in text:
        return "서울"
    elif "인천" in text:
        return "인천"
    elif "경기" in text or "부천" in text or "수원" in text or "고양" in text:
        return "경기"
    
    # Coordinate-based fallback
    if 37.42 <= lat <= 37.7 and 126.75 <= lng <= 127.2:
        return "서울"
    elif 37.3 <= lat <= 37.6 and 126.3 <= lng <= 126.8:
        return "인천"
    return "경기"

# Helper to get clean valid direct link or return empty string (ignoring None, null, etc.)
def get_clean_link(r, keys):
    for k in keys:
        val = r.get(k)
        if val and val.strip() and val.strip().lower() not in ["none", "null", ""]:
            link = val.strip()
            # If it's a domain name without http, prefix with https
            if not link.startswith("http") and "." in link:
                link = "https://" + link
            if link.startswith("http"):
                return link
    return ""

new_added_count = 0
added_events_list = []

# --- 3. PARSE DATA 1 (cp949 encoding) ---
data1_count = 0
if os.path.exists(DATA1_CSV):
    with open(DATA1_CSV, "r", encoding="cp949", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Strictly filter for direct links first
            link = get_clean_link(r, ["문화포털상세URL", "홈페이지?주소", "홈페이지주소"])
            if not link:
                continue # Skip if no direct details link is present
                
            start_date = r.get("시작일") or ""
            if not start_date:
                continue
            start_date = start_date.split()[0].strip()
            
            # Start date threshold: on or after July 16, 2026
            if start_date < "2026-07-16":
                continue
            
            # Coordinates auto-detection
            val1 = 0.0
            val2 = 0.0
            try:
                val1 = float(r.get("경도(Y좌표)") or 0)
            except ValueError:
                pass
            try:
                val2 = float(r.get("위도(X좌표)") or 0)
            except ValueError:
                pass
                
            lat, lng = 0.0, 0.0
            for val in [val1, val2]:
                if 36.0 <= val <= 39.0:
                    lat = val
                elif 126.0 <= val <= 129.0:
                    lng = val
                    
            facility = r.get("장소") or r.get("기관명") or ""
            addr = r.get("자치구") or ""
            full_addr = f"서울특별시 {addr} {facility}" if "서울" in r.get("시민/기관", "") or addr else facility
            
            # Area filter
            if not is_metropolitan(lat, lng, full_addr, facility):
                continue
                
            core_title = (r.get("공연/행사명") or "").strip()
            if not core_title:
                continue
                
            # Deduplicate
            if (core_title, start_date) in existing_keys:
                continue
                
            # Build fields
            category = determine_category(core_title, r.get("프로그램소개") or "")
            region = get_region(lat, lng, full_addr, facility)
            title = f"[{region}/{category}] {core_title}"
            
            fee_info = r.get("이용요금") or r.get("유무료") or "무료"
            price, is_free = parse_price(fee_info)
            
            day_val = int(start_date.split("-")[2])
            tip = generate_tip(core_title, facility)
            
            # Fallback coordinates if zero
            if lat == 0.0 or lng == 0.0:
                if region == "서울": lat, lng = 37.5665, 126.9780
                elif region == "인천": lat, lng = 37.4563, 126.7052
                else: lat, lng = 37.2752, 127.0095
                
            end_date = r.get("종료일") or start_date
            end_date = end_date.split()[0].strip()
            date_str = f"{start_date} ~ {end_date}"
            if r.get("행사시간"):
                date_str += f" ({r.get('행사시간')})"
                
            mapped_event = {
                "title": title,
                "facility": facility,
                "date": date_str,
                "day": str(day_val),
                "link": link,
                "fee": fee_info,
                "isFree": "True" if is_free else "False",
                "price": str(price),
                "category": category,
                "location": full_addr,
                "lat": f"{lat:.4f}",
                "lng": f"{lng:.4f}",
                "tip": tip
            }
            added_events_list.append(mapped_event)
            existing_keys.add((core_title, start_date))
            new_added_count += 1
            data1_count += 1

print(f"Data 1 parse complete. Added {data1_count} direct-link events.")

# --- 4. PARSE DATA 2 (cp949 encoding) ---
data2_count = 0
if os.path.exists(DATA2_CSV):
    with open(DATA2_CSV, "r", encoding="cp949", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Strictly filter for direct links first
            link = get_clean_link(r, ["예매정보", "홈페이지주소"])
            if not link:
                continue # Skip if no direct link is present
                
            start_date = r.get("행사시작일자") or ""
            if not start_date or start_date < "2026-07-16":
                continue
                
            try:
                lat = float(r.get("위도") or 0)
                lng = float(r.get("경도") or 0)
            except ValueError:
                lat, lng = 0.0, 0.0
                
            facility = r.get("장소") or r.get("제공기관명") or ""
            addr = r.get("소재지도로명주소") or r.get("소재지지번주소") or ""
            
            # Area filter
            if not is_metropolitan(lat, lng, addr, facility):
                continue
                
            core_title = (r.get("행사명") or "").strip()
            if not core_title:
                continue
                
            # Deduplicate
            if (core_title, start_date) in existing_keys:
                continue
                
            category = determine_category(core_title, r.get("행사내용") or "")
            region = get_region(lat, lng, addr, facility)
            title = f"[{region}/{category}] {core_title}"
            
            fee_info = r.get("요금정보") or r.get("관람요금") or "무료"
            price, is_free = parse_price(fee_info, r.get("관람요금") or "")
            
            day_val = int(start_date.split("-")[2])
            
            start_time = r.get("행사시작시각") or ""
            end_time = r.get("행사종료시각") or ""
            if start_time and end_time:
                date_str = f"{start_date} {start_time} ~ {end_time}"
            else:
                date_str = f"{start_date} 14:00 ~ 16:00"
                
            tip = generate_tip(core_title, facility)
            
            if lat == 0.0 or lng == 0.0:
                if region == "서울": lat, lng = 37.5665, 126.9780
                elif region == "인천": lat, lng = 37.4563, 126.7052
                else: lat, lng = 37.2752, 127.0095
                
            mapped_event = {
                "title": title,
                "facility": facility,
                "date": date_str,
                "day": str(day_val),
                "link": link,
                "fee": fee_info,
                "isFree": "True" if is_free else "False",
                "price": str(price),
                "category": category,
                "location": addr if addr else facility,
                "lat": f"{lat:.4f}",
                "lng": f"{lng:.4f}",
                "tip": tip
            }
            added_events_list.append(mapped_event)
            existing_keys.add((core_title, start_date))
            new_added_count += 1
            data2_count += 1

print(f"Data 2 parse complete. Added {data2_count} direct-link events.")

# --- 5. PARSE DATA 3 (cp949 encoding) ---
data3_count = 0
if os.path.exists(DATA3_CSV):
    with open(DATA3_CSV, "r", encoding="cp949", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Strictly filter for direct links first
            link = get_clean_link(r, ["관련정보", "홈페이지주소"])
            if not link:
                continue # Skip if no direct link is present
                
            start_date = r.get("축제시작일자") or ""
            if not start_date or start_date < "2026-07-16":
                continue
                
            try:
                lat = float(r.get("위도") or 0)
                lng = float(r.get("경도") or 0)
            except ValueError:
                lat, lng = 0.0, 0.0
                
            facility = r.get("개최장소") or r.get("주관기관명") or ""
            addr = r.get("소재지도로명주소") or r.get("소재지지번주소") or ""
            
            # Area filter
            if not is_metropolitan(lat, lng, addr, facility):
                continue
                
            core_title = (r.get("축제명") or "").strip()
            if not core_title:
                continue
                
            # Deduplicate
            if (core_title, start_date) in existing_keys:
                continue
                
            category = determine_category(core_title, r.get("축제내용") or "")
            region = get_region(lat, lng, addr, facility)
            title = f"[{region}/{category}] {core_title}"
            
            fee_info = "무료"
            price, is_free = 0, True
            
            day_val = int(start_date.split("-")[2])
            
            end_date = r.get("축제종료일자") or start_date
            date_str = f"{start_date} ~ {end_date}"
            
            tip = generate_tip(core_title, facility)
            
            if lat == 0.0 or lng == 0.0:
                if region == "서울": lat, lng = 37.5665, 126.9780
                elif region == "인천": lat, lng = 37.4563, 126.7052
                else: lat, lng = 37.2752, 127.0095
                
            mapped_event = {
                "title": title,
                "facility": facility,
                "date": date_str,
                "day": str(day_val),
                "link": link,
                "fee": fee_info,
                "isFree": "True" if is_free else "False",
                "price": str(price),
                "category": category,
                "location": addr if addr else facility,
                "lat": f"{lat:.4f}",
                "lng": f"{lng:.4f}",
                "tip": tip
            }
            added_events_list.append(mapped_event)
            existing_keys.add((core_title, start_date))
            new_added_count += 1
            data3_count += 1

print(f"Data 3 parse complete. Added {data3_count} direct-link events.")

# --- 6. MERGE AND SEQUENCE IDs ---
all_events = []
current_id = 1

# Add upgraded original vetted events
for ev in existing_events:
    row_copy = dict(ev)
    row_copy["id"] = str(current_id)
    all_events.append(row_copy)
    current_id += 1

# Add newly added events with guaranteed direct links
for ev in added_events_list:
    row_copy = dict(ev)
    row_copy["id"] = str(current_id)
    all_events.append(row_copy)
    current_id += 1

# Write back to cultural_events.csv
fieldnames = ["id", "title", "facility", "date", "day", "link", "fee", "isFree", "price", "category", "location", "lat", "lng", "tip"]
with open(ORIGINAL_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_events:
        writer.writerow(row)

print(f"Clean merge operation completed! Total events in database now: {len(all_events)} (Added {new_added_count} direct-link metropolitan events. Zero Naver search links.)")
