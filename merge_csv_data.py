import csv
import re
import sys

# Ensure stdout handles Korean characters
sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r"c:\aiclu_1\free_cul\cultural_events.csv"
USER_CSV = r"c:\aiclu_1\free_cul\user_raw_data.csv"

# Read original events to find the max ID
original_events = []
max_id = 0
with open(ORIGINAL_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        original_events.append(r)
        if r.get("id"):
            max_id = max(max_id, int(r["id"]))

print(f"Original events count: {len(original_events)}, Max ID: {max_id}")

# Read user raw CSV
with open(USER_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    user_rows = list(reader)

print(f"User raw rows count: {len(user_rows)}")

# Define helper to determine category
def determine_category(title, content):
    text = (title + " " + content).lower()
    if any(k in text for k in ["공연", "국악", "가요제", "콘서트", "콩구르", "합창", "연주회", "음악회", "오케스트라", "서커스"]):
        return "공연"
    elif any(k in text for k in ["전시", "미술", "갤러리", "박물관", "그림", "사진"]):
        return "전시"
    elif any(k in text for k in ["영화", "시네마", "상영"]):
        return "영화"
    elif any(k in text for k in ["도서관", "책", "독서", "작가", "북토크"]):
        return "도서관"
    elif any(k in text for k in ["강연", "특강", "인문학", "아카데미", "교육", "세미나"]):
        return "강연"
    elif any(k in text for k in ["체험", "공방", "원데이", "만들기", "교실"]):
        return "체험"
    else:
        return "공연"

# Define helper to parse price
def parse_price(fee_info, price_info):
    text = (fee_info + " " + price_info).lower()
    if "무료" in text and "유료" not in text:
        return 0, True
    # Find numbers
    nums = re.findall(r'\d+', text.replace(",", ""))
    if nums:
        # Filter out numbers that are too small (e.g., ages or phone parts)
        valid_prices = [int(n) for n in nums if int(n) >= 1000]
        if valid_prices:
            return min(valid_prices), False
    return 0, True # Default to free/0 if no price found

# Define helper to clean and prefix title
def clean_title(row):
    title = row.get("행사명") or "알 수 없는 기밀 행사"
    addr = row.get("소재지도로명주소") or row.get("소재지지번주소") or row.get("제공기관명") or ""
    cat = determine_category(title, row.get("행사내용") or "")
    
    region = "기타"
    if "통영" in addr or "통영" in row.get("장소", ""):
        region = "경남"
    elif "진주" in addr or "진주" in row.get("장소", ""):
        region = "경남"
    elif "장성" in addr or "장성" in row.get("장소", ""):
        region = "전남"
    elif "서울" in addr:
        region = "서울"
    elif "경기" in addr or "수원" in addr or "부천" in addr:
        region = "경기"
    elif "인천" in addr:
        region = "인천"
        
    return f"[{region}/{cat}] {title}"

# Helper to generate funny spy-style tips based on titles
def generate_tip(title, facility):
    if "가요제" in title:
        return f"통영 앞바다의 푸른 야경을 배경으로 열리는 축제입니다. 가벼운 바람막이 점퍼를 지참하고, 연인 혹은 동료와 한강 둔치처럼 강구안에 숨어들어 낭만을 가로채십시오."
    elif "콩구르" in title or "콩쿠르" in title:
        return f"세계적인 음악 신예들의 숨막히는 클래식 대결을 무료로 도청할 수 있는 기회입니다. 기침이 날 땐 사탕을 미리 머금고, 숨소리조차 숨긴 채 예술의 깊이를 훔치세요."
    elif "문화재 야행" in title:
        return f"삼도수군통제영의 고풍스러운 밤 골목을 은밀히 순찰하십시오. 한밤중에 열리는 비밀 미션에 참가해 특산 기념품을 줍줍하는 작전이 유효합니다."
    elif "합창" in title or "시립교향악단" in title or "시립국악관현악단" in title or "음악회" in title:
        return f"웅장한 관현악의 공명을 대공연장 구석 vip급 시야 방해 없는 자리에 은밀히 포지셔닝하여 감상하십시오. 귓가를 호강시키는 공짜 교양 침투 작전입니다."
    elif "영화상영" in title:
        return f"대강당 한편 구석에 조용히 침투해 스크린을 정조준하십시오. 팝콘 씹는 소리는 보안을 깨뜨리니 쉿! 조용히 녹아내리는 감동을 갈취하십시오."
    elif "아기돼지" in title or "지피" in title or "알라딘" in title or "서커스" in title or "브레맨" in title:
        return f"가족 단위 타겟들이 붐비는 소공연장입니다. 아이들 틈바구니 속으로 자연스럽게 동화되는 페이스 오프 위장 기술이 핵심입니다. 눈치껏 관람권을 빼돌리십시오."
    else:
        return f"{facility} 로비 한복판에서 열리는 은밀한 감성 기동입니다. 사냥꾼 다운 신속한 후퇴를 위해 주차장 출구 근처에 차를 포지셔닝해 두십시오."

# Filter and map rows
merged_rows = list(original_events)
current_id = max_id + 1

added_count = 0
for r in user_rows:
    start_date = r.get("행사시작일자") or ""
    # We only take events starting on or after July 16, 2026
    if start_date and start_date >= "2026-07-16":
        # Extract fields
        addr = r.get("소재지도로명주소") or r.get("소재지지번주소") or r.get("제공기관명") or ""
        
        # Latitude and Longitude check
        lat_val = r.get("위도")
        lng_val = r.get("경도")
        if not lat_val or not lng_val:
            # Fallbacks for known areas
            if "통영" in addr:
                lat_val, lng_val = 34.8417, 128.4253
            elif "진주" in addr:
                lat_val, lng_val = 35.1872, 128.0917
            elif "장성" in addr:
                lat_val, lng_val = 35.3015, 126.7845
            else:
                lat_val, lng_val = 37.5665, 126.9780 # Seoul
        
        lat = float(lat_val)
        lng = float(lng_val)
        
        facility = r.get("장소") or r.get("제공기관명") or "지정 장소"
        
        # Generate full date string
        start_time = r.get("행사시작시각") or ""
        end_time = r.get("행사종료시각") or ""
        if start_time and end_time:
            date_str = f"{start_date} {start_time} ~ {end_time}"
        else:
            date_str = start_date
            
        # Extract day (as int)
        day_val = int(start_date.split("-")[2])
        
        # Handle link
        link = r.get("홈페이지주소") or r.get("예매정보") or ""
        if not link or link == "None" or link.strip() == "":
            link = f"https://search.naver.com/search.naver?query={r.get('행사명')}"
        elif not link.startswith("http"):
            link = "https://" + link
            
        # Parse price and fee
        fee = r.get("요금정보") or r.get("관람요금") or "무료"
        price, is_free = parse_price(r.get("요금정보") or "", r.get("관람요금") or "")
        
        category = determine_category(r.get("행사명") or "", r.get("행사내용") or "")
        title = clean_title(r)
        
        tip = generate_tip(r.get("행사명", ""), facility)
        
        mapped_row = {
            "id": str(current_id),
            "title": title,
            "facility": facility,
            "date": date_str,
            "day": str(day_val),
            "link": link,
            "fee": fee if fee else "무료",
            "isFree": "True" if is_free else "False",
            "price": str(price),
            "category": category,
            "location": addr,
            "lat": f"{lat:.4f}",
            "lng": f"{lng:.4f}",
            "tip": tip
        }
        
        merged_rows.append(mapped_row)
        current_id += 1
        added_count += 1

print(f"Successfully mapped and merged {added_count} rows from user dataset!")

# Write back to cultural_events.csv
fieldnames = ["id", "title", "facility", "date", "day", "link", "fee", "isFree", "price", "category", "location", "lat", "lng", "tip"]
with open(ORIGINAL_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in merged_rows:
        writer.writerow(row)

print("Merged database successfully written to cultural_events.csv!")
