// 🕵️‍♂️ "수도권 무료 문화생활 사냥꾼" - 단일 진실 공급원 (CSV) 비동기 로드형 웹 컨트롤러 (app.js)
let futureCulturalEvents = [];

// GIS 및 상호 연동 전역 관리용 객체
let map;
let mapMarkers = {};

// 활성 다차원 필터 상태 변수
let activeFilters = {
    region: 'all',
    category: 'all',
    fee: 'all',
    search: ''
};

// 현재 활성화된 캘린더 월 (기본: 7월)
let currentCalendarMonth = 7;

// 📥 CSV 파일 비동기 로딩 및 PapaParse 분석 가동
async function loadEventsFromCSV() {
    try {
        const response = await fetch('cultural_events.csv');
        if (!response.ok) {
            throw new Error(`CSV 파일을 읽어오는 중 에러 발생: ${response.statusText}`);
        }
        const csvText = await response.text();
        
        // PapaParse 동적 데이터 정밀 파싱 개시
        const parsed = Papa.parse(csvText, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true
        });

        // 데이터 정합성 보정 (문자열 불리언 보정 등)
        futureCulturalEvents = parsed.data.map(row => ({
            id: Number(row.id),
            title: String(row.title),
            facility: String(row.facility),
            date: String(row.date),
            day: Number(row.day),
            link: String(row.link),
            fee: String(row.fee),
            isFree: row.isFree === true || String(row.isFree).toLowerCase() === 'true',
            price: row.price ? Number(row.price) : 0,
            category: String(row.category),
            location: String(row.location),
            lat: Number(row.lat),
            lng: Number(row.lng),
            tip: String(row.tip)
        }));

        console.log("[CSV LOAD SUCCESS] 총 수집 타겟 카운트:", futureCulturalEvents.length);
        
        // 데이터 연동 대시보드 컴포넌트 순차 가동
        initLeafletMap();
        generateLargeCalendar(currentCalendarMonth);
        updateFilterCounts();
        renderEvents();

    } catch (error) {
        console.error("데이터베이스 로딩 실패:", error);
        document.getElementById("events-timeline").innerHTML = `
            <div class="no-events" style="text-align:center; padding:40px; color:var(--color-danger);">
                <p>⚠️ 기밀 문화생활 CSV 데이터베이스 연결 실패. 로컬 웹 서버 상태를 점검하십시오.</p>
                <p style="font-size:0.8rem; margin-top:8px;">${error.message}</p>
            </div>
        `;
    }
}

// Google 캘린더 다이렉트 일정 생성 URL 빌더 (100% 동적 파싱)
function generateGoogleCalendarUrl(event) {
    const baseUrl = "https://calendar.google.com/calendar/render?action=TEMPLATE";
    const text = encodeURIComponent(event.title);
    
    // date 형식 "2026-07-17 19:00 ~ 21:00" 또는 "2026-09-05" 등에서 년/월/일 파싱
    const yr = "2026";
    const mo = String(event.date.substring(5, 7)).padStart(2, '0');
    const dy = String(event.date.substring(8, 10)).padStart(2, '0');
    
    let startIso = `${yr}${mo}${dy}T140000`;
    let endIso = `${yr}${mo}${dy}T160000`;
    
    // 시간 정보가 매칭되는지 확인 (HH:MM 형식)
    const timeMatch = event.date.match(/(\d{2}):(\d{2})\s*~\s*(\d{2}):(\d{2})/);
    if (timeMatch) {
        const startH = timeMatch[1];
        const startM = timeMatch[2];
        const endH = timeMatch[3];
        const endM = timeMatch[4];
        
        startIso = `${yr}${mo}${dy}T${startH}${startM}00`;
        endIso = `${yr}${mo}${dy}T${endH}${endM}00`;
    }
    
    const dates = `${startIso}/${endIso}`;
    const location = encodeURIComponent(`${event.facility} (${event.location})`);
    
    // 세부 본문에 꿀팁과 유출 웹사이트 원문 링크를 동봉
    const details = encodeURIComponent(
        `🕵️‍♂️ [수도권 무료 문화생활 사냥꾼의 기밀 노하우]\n` +
        `- 타겟 요금: ${event.fee}\n` +
        `- 침투 전용 꿀팁: ${event.tip}\n` +
        `- 기밀 원문 연결: ${event.link}\n\n` +
        `* 본 정보는 가볍게 본인만 소지하시고 외부 유출을 엄금해 주세요!`
    );

    return `${baseUrl}&text=${text}&dates=${dates}&details=${details}&location=${location}`;
}

// 🗺️ Leaflet.js GIS 지도 초기화 함수
function initLeafletMap() {
    // 디폴트 뷰는 수도권 전역을 아우르는 지점 (all filter 기준)
    map = L.map('map-canvas', {
        zoomControl: true,
        scrollWheelZoom: false // 스크롤 시 브라우저 방해 방지
    }).setView([37.45, 126.95], 9);

    // OpenStreetMap 타일 레이어 추가 (스타일은 style.css의 invert 필터로 웅장한 다크 연출)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // 각 이벤트에 맵 마커 핀 투척 및 바인딩
    futureCulturalEvents.forEach(event => {
        const popupContent = `
            <div class="leaflet-popup-title">📌 ${event.facility}</div>
            <div class="leaflet-popup-desc" style="font-weight:bold; color:var(--color-primary); margin-bottom:4px;">
                ${event.isFree ? '🎁 완전 무료' : `💸 유료: ${(event.price || 0).toLocaleString()}원`}
            </div>
            <div class="leaflet-popup-desc">${event.title}</div>
            <div class="leaflet-popup-desc" style="font-size:0.7rem; color:var(--color-text-muted);">📅 ${event.date}</div>
            <a href="javascript:void(0)" onclick="focusOnEventCard(${event.id})" 
               style="font-size:0.75rem; color:var(--color-warning); font-weight:bold; text-decoration:none; display:block; margin-top:6px;">
                🕵️‍♂️ 이 리포트 카드로 이동하기 →
            </a>
        `;

        // 마커 생성
        const marker = L.marker([event.lat, event.lng]);
        marker.bindPopup(popupContent);
        
        // 맵마커 전역 매핑 풀에 등록
        mapMarkers[event.id] = marker;
    });
}

// 맵 마커 동적 갱신 필터링 함수
function updateMapMarkers(filteredEvents) {
    if (!map) return;
    
    // 1. 모든 마커 지도에서 일시적 제거
    Object.values(mapMarkers).forEach(marker => {
        map.removeLayer(marker);
    });
    
    // 2. 필터링 통과한 마커만 지도에 표시
    filteredEvents.forEach(event => {
        if (mapMarkers[event.id]) {
            mapMarkers[event.id].addTo(map);
        }
    });
}

// 📅 2026년 대형 그리드 캘린더 생성기 (동적 월 지원)
function generateLargeCalendar(month = 7) {
    const calendarGrid = document.getElementById("large-calendar-grid");
    calendarGrid.innerHTML = ""; // 초기화

    // 첫날 요일(startOffset) 및 총 일수(totalDays) 동적 계산
    const startOffset = new Date(2026, month - 1, 1).getDay();
    const totalDays = new Date(2026, month, 0).getDate();
    
    // 35개 또는 42개 그리드 셀 카운트 자동 결정
    const neededCells = startOffset + totalDays;
    const totalCells = neededCells <= 35 ? 35 : 42;
    
    // 이전 달 마지막 날짜 채우기 (비활성 셀)
    const prevMonthTotalDays = new Date(2026, month - 1, 0).getDate();
    for (let i = startOffset - 1; i >= 0; i--) {
        const cell = document.createElement("div");
        cell.className = "calendar-cell inactive";
        cell.innerHTML = `<span class="cell-day-num">${prevMonthTotalDays - i}</span>`;
        calendarGrid.appendChild(cell);
    }

    // 선택된 월의 날짜 채우기 (1일 ~ totalDays)
    for (let day = 1; day <= totalDays; day++) {
        const cell = document.createElement("div");
        
        // 오늘 날짜(7월 16일) 하이라이트 클래스 (7월일 때만)
        const isToday = (month === 7 && day === 16) ? "today" : "";
        
        // 요일 계산
        const dayOfWeekIndex = (day + startOffset - 1) % 7;
        let dayClass = "";
        if (dayOfWeekIndex === 0) dayClass = "sun";
        if (dayOfWeekIndex === 6) dayClass = "sat";

        cell.className = `calendar-cell current-month ${isToday} ${dayClass}`;
        cell.innerHTML = `<span class="cell-day-num">${day}</span>`;

        // 해당 날짜 및 해당 월에 할당된 기밀 사냥 정보 매핑
        const daysEvents = futureCulturalEvents.filter(e => {
            const eventMonth = Number(e.date.substring(5, 7));
            return eventMonth === month && e.day === day;
        });

        daysEvents.forEach(evt => {
            const eventPill = document.createElement("span");
            eventPill.className = `cal-event-pill ${evt.isFree ? 'free' : 'budget'}`;
            eventPill.title = evt.title;
            
            // 캘린더 칸이 좁으므로 태그명 위주 축약 송출
            let tag = evt.title.split("]")[0].replace("[", "");
            if (tag.includes("/")) {
                tag = tag.split("/")[1]; // ex) "서울/공연" -> "공연"
            }
            eventPill.textContent = `[${tag}] ${evt.title.split("]")[1]?.substring(0, 7) || ""}...`;
            
            // 클릭 시 해당 카드 줌 워프 인터랙션 바인딩
            eventPill.addEventListener("click", (e) => {
                e.stopPropagation();
                // 작전 월이 다를 경우 카드 피드 필터가 캘린더 타겟을 가리는 것을 막기 위해 임시 초기화
                resetFiltersToMatchEvent(evt);
                focusOnEventCard(evt.id);
            });
            cell.appendChild(eventPill);
        });

        calendarGrid.appendChild(cell);
    }

    // 다음 달 비활성 채우기
    const remainingCells = totalCells - (startOffset + totalDays);
    for (let day = 1; day <= remainingCells; day++) {
        const cell = document.createElement("div");
        cell.className = "calendar-cell inactive";
        cell.innerHTML = `<span class="cell-day-num">${day}</span>`;
        calendarGrid.appendChild(cell);
    }
}

// 캘린더의 일정을 눌렀을 때, 필터 때문에 해당 카드가 안 보이는 걸 방지하는 동기화 필터 보정장치
function resetFiltersToMatchEvent(event) {
    let region = "서울";
    if (event.title.startsWith("[경기/")) region = "경기";
    else if (event.title.startsWith("[인천/")) region = "인천";

    activeFilters.region = "all";
    activeFilters.category = "all";
    activeFilters.fee = "all";

    // UI 버튼 상태 동기화 복구
    document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
    document.querySelector(`[data-region="all"]`).classList.add("active");
    document.querySelector(`[data-category="all"]`).classList.add("active");
    document.querySelector(`[data-fee="all"]`).classList.add("active");

    renderEvents();
}

// 🎯 특정 리포트 카드로 스크롤 이동, 하이라이트 점멸 및 지도 포커스 이동 (Warp Interaction)
function focusOnEventCard(eventId) {
    const card = document.getElementById(`event-card-${eventId}`);
    if (!card) return;

    // 1. 카드로 보드 스무스 워핑 이동
    card.scrollIntoView({ behavior: "smooth", block: "center" });

    // 2. 카드 윤곽선 네온 하이라이트 점멸 효과
    document.querySelectorAll(".event-card").forEach(c => c.classList.remove("highlight-pulse"));
    card.classList.add("highlight-pulse");
    
    // 3. 지도 포커스 플라이 (Fly-to) 줌인 모션 동기화
    const event = futureCulturalEvents.find(e => e.id === eventId);
    if (event && map) {
        map.flyTo([event.lat, event.lng], 14, {
            animate: true,
            duration: 1.5
        });

        // 지도의 해당 핀 팝업 강제 트리거 개방
        setTimeout(() => {
            if (mapMarkers[eventId]) {
                mapMarkers[eventId].openPopup();
            }
        }, 1500);
    }

    // 3초 후 점멸 스킨 소거
    setTimeout(() => {
        card.classList.remove("highlight-pulse");
    }, 4500);
}

// 🧠 자연어 형태의 검색어 매칭 엔진 (Multi-Word Semantic Search Matcher)
function matchNaturalLanguage(event, query) {
    const qClean = query.trim().toLowerCase();
    if (!qClean) return true;
    
    // 공백 단위로 검색어를 토큰화
    const rawTokens = qClean.split(/\s+/);
    // 조사, 접속사 등의 정지어 소거
    const stopWords = new Set(["하는", "에서", "있는", "열리는", "의", "그리고", "를", "을", "가", "이", "에", "과", "와", "로", "으로", "해서", "및"]);
    const tokens = rawTokens.filter(t => t.length > 0 && !stopWords.has(t));
    
    if (tokens.length === 0) return true;
    
    // AND 매칭 (모든 유효 토큰이 해당 이벤트를 만족해야 함)
    return tokens.every(token => {
        // 1. 유무료 조건의 은밀한 의미론적 번역 매칭
        if (token === "무료" || token === "공짜" || token === "무상" || token === "공짜로" || token === "0원") {
            return event.isFree;
        }
        if (token === "유료" || token === "돈" || token === "유상" || token === "유료인") {
            return !event.isFree;
        }
        
        // 2. 작전 지역의 은밀한 의미론적 매칭
        if (token === "서울" || token === "서울시" || token === "서울특별시") {
            return event.title.startsWith("[서울/");
        }
        if (token === "경기" || token === "경기도" || token === "경인") {
            return event.title.startsWith("[경기/");
        }
        if (token === "인천" || token === "인천시" || token === "인천광역시") {
            return event.title.startsWith("[인천/");
        }
        
        // 3. 기밀 카테고리의 의미론적 매칭
        const categories = ["공연", "전시", "영화", "도서관", "강연", "체험"];
        if (categories.includes(token)) {
            return event.category === token;
        }
        
        // 4. 일반 텍스트 포함 매칭 (대소문자 무시)
        return event.title.toLowerCase().includes(token) || 
               event.facility.toLowerCase().includes(token) || 
               event.location.toLowerCase().includes(token) || 
               event.tip.toLowerCase().includes(token) || 
               event.category.toLowerCase().includes(token) ||
               event.fee.toLowerCase().includes(token);
    });
}

// 📋 사냥 타겟 리포트 피드 렌더링 함수 (다차원 결합 필터 적용)
function renderEvents() {
    const timelineContainer = document.getElementById("events-timeline");
    timelineContainer.innerHTML = ""; // 기존 아이템 클리어

    // 다차원 필터 적용
    const filteredEvents = futureCulturalEvents.filter(event => {
        // 1. 기밀 키워드 검색 필터 (자연어 검색 통합 적용)
        if (activeFilters.search) {
            if (!matchNaturalLanguage(event, activeFilters.search)) return false;
        }

        // 2. 지역 필터
        if (activeFilters.region !== "all") {
            let rTag = "서울";
            if (event.title.startsWith("[경기/")) rTag = "경기";
            else if (event.title.startsWith("[인천/")) rTag = "인천";
            
            if (rTag !== activeFilters.region) return false;
        }

        // 3. 카테고리 필터
        if (activeFilters.category !== "all") {
            if (event.category !== activeFilters.category) return false;
        }

        // 4. 요금 필터
        if (activeFilters.fee !== "all") {
            if (activeFilters.fee === "free" && !event.isFree) return false;
            if (activeFilters.fee === "budget" && (event.isFree || event.price > 10000)) return false;
        }

        return true;
    });

    // 지도 핀 동기화 갱신
    updateMapMarkers(filteredEvents);

    // 필터 변경 시 지도 위치를 지능적으로 자동 조정
    if (map) {
        if (activeFilters.region === "all") {
            map.setView([37.45, 126.95], 9);
        } else if (activeFilters.region === "서울") {
            map.setView([37.56, 126.97], 11);
        } else if (activeFilters.region === "경기") {
            map.setView([37.28, 127.05], 10);
        } else if (activeFilters.region === "인천") {
            map.setView([37.46, 126.65], 11);
        }
    }

    if (filteredEvents.length === 0) {
        timelineContainer.innerHTML = `
            <div class="no-events" style="text-align:center; padding:40px; color:var(--color-text-muted);">
                <p>⚠️ 선택하신 필터 조건과 일치하는 사냥 타겟이 존재하지 않습니다. 탐색 주파수를 다시 맞춰 보십시오.</p>
            </div>
        `;
        return;
    }

    // 카드 목록 렌더링
    filteredEvents.forEach(event => {
        const card = document.createElement("div");
        card.className = "event-card";
        card.id = `event-card-${event.id}`;
        
        const googleCalendarLink = generateGoogleCalendarUrl(event);

        // 월/일 추출
        const evMonth = Number(event.date.substring(5, 7));
        const evDay = Number(event.date.substring(8, 10));

        // 요일 계산
        const dayOfWeek = new Date(2026, evMonth - 1, evDay).getDay();
        const weekNames = ['일', '월', '화', '수', '목', '금', '토'];
        const weekdayStr = weekNames[dayOfWeek];

        card.innerHTML = `
            <!-- Date Badge -->
            <div class="event-date-badge">
                <span class="date-month">${evMonth}월</span>
                <span class="date-day">${evDay}</span>
                <span class="date-weekday" style="color:${dayOfWeek === 0 ? '#FDA4AF' : dayOfWeek === 6 ? '#93C5FD' : 'var(--color-primary)'}">${weekdayStr}요일</span>
            </div>

            <!-- Details -->
            <div class="event-details">
                <div class="event-badge-row">
                    <span class="category-tag">${event.category}</span>
                    <span class="fee-tag ${event.isFree ? 'free' : 'paid'}">
                        ${event.isFree ? '🎁 완전 무료' : `💸 유료: ${(event.price || 0).toLocaleString()}원`}
                    </span>
                </div>
                <h4 class="event-title">${event.title}</h4>
                
                <div class="event-info-line">
                    <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 8V12L14 14"/>
                    </svg>
                    <span>${event.date}</span>
                </div>

                <div class="event-info-line">
                    <svg class="info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2Z"/>
                        <circle cx="12" cy="9" r="3"/>
                    </svg>
                    <span>${event.facility} (${event.location})</span>
                </div>

                <div class="event-tip">
                    <span class="tip-emoji">⚡</span>
                    <p class="tip-text"><strong>침투 꿀팁:</strong> ${event.tip}</p>
                </div>
            </div>

            <!-- Actions -->
            <div class="event-actions">
                <a href="${googleCalendarLink}" target="_blank" class="btn btn-primary">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    구글 캘린더 등록
                </a>
                <a href="${event.link}" target="_blank" class="btn btn-secondary">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                    기밀 원문 접속
                </a>
            </div>
        `;
        
        // 카드 자체를 눌렀을 때 맵 연동 활성화
        card.addEventListener("click", (e) => {
            // 버튼 요소가 눌린 것이 아닐 때만 맵을 워핑
            if (!e.target.closest(".btn") && !e.target.closest("a")) {
                focusOnEventCard(event.id);
            }
        });

        timelineContainer.appendChild(card);
    });
}

// 🕵️‍♂️ 터미널 시뮬레이터 구동 로그
const terminalLogs = [
    { text: "[SYSTEM] 민간 및 공공 복합문화망 스캐닝 드라이버 탑재 완료.", type: "system-msg" },
    { text: "[INFO] 작전 개시: 오늘(2026-07-16) 이후의 미래형 가치 혜택만 필터링합니다.", type: "log-line" },
    { text: "[INFO] CSV 파일 데이터베이스 연동 감지 (`cultural_events.csv` 로딩완료).", type: "success-line" },
    { text: "[OK] 서울도서관, 국립현대미술관, 세종문화회관, 예술의전당 GPS 추출 완료.", type: "success-line" },
    { text: "[OK] 스타필드 코엑스 별마당도서관 및 신세계/현대 아카데미 첩보 갱신 성공.", type: "success-line" },
    { text: "[OK] 대학로 소극장, 부천시민소극장, 문학시어터 연동 및 GPS 보정 기동.", type: "success-line" },
    { text: "[INFO] 수도권 전역의 37개 핵심 가성비 미래 캘린더 합격선 타겟 노출 완료.", type: "success-line" },
    { text: "[FILTER] 요금 위반 자동 차단: 'VIP석 170,000원 (뮤지컬 레미제라블 내한공연)'", type: "log-line" },
    { text: "[OK] 총 37개 가성비 미래 캘린더 합격선 타겟 노출 완료.", type: "success-line" }
];

const whisperQuotes = [
    "쉿, 비밀번호는 없어. 이건 진짜 너한테만 살짝 흘려주는 수도권 극비 문화 루트니까 아무한테도 말하지 마...",
    "남들 비싼 돈 내고 티켓 살 때, 우린 이걸로 몰래 무료 침투하는 거야. 알았지? (찡긋)",
    "이 정보 퍼지면 백화점 광클 예매 전쟁 나니까, 너만 조용히 선착순 슬롯을 타격해서 획득하라고...",
    "쉿, 골목 구석으로 은밀히 와봐. 이번 주 수도권에서 돈 단 한 푼 안 쓰고 교양 호사 누릴 수 있는 극비 일정을 훔쳐왔어."
];

function runTerminalSimulation() {
    const terminalBody = document.getElementById("terminal-body");
    const btnScan = document.getElementById("btn-run-scan");
    const whisperText = document.getElementById("whisper-text");
    
    // 버튼 비활성화
    btnScan.disabled = true;
    btnScan.classList.add("pulsing");
    
    // 기존 터미널 내용 초기화 및 신호음 느낌 콘솔
    terminalBody.innerHTML = `<div class="terminal-line system-msg">[SYSTEM] 전용 주파수 재동기화 중...</div>`;
    
    let index = 0;
    
    function printNextLine() {
        if (index < terminalLogs.length) {
            const log = terminalLogs[index];
            const div = document.createElement("div");
            div.className = `terminal-line ${log.type}`;
            div.textContent = log.text;
            terminalBody.appendChild(div);
            
            // 자동 스크롤
            terminalBody.scrollTop = terminalBody.scrollHeight;
            
            index++;
            // 무작위 딜레이로 실감 나는 느낌 배가
            setTimeout(printNextLine, 300 + Math.random() * 300);
        } else {
            // 시뮬레이션 종료 시 처리
            btnScan.disabled = false;
            btnScan.classList.remove("pulsing");
            
            // 귓속말 배너 랜덤 코멘트로 교체
            const randomQuote = whisperQuotes[Math.floor(Math.random() * whisperQuotes.length)];
            whisperText.textContent = randomQuote;
            
            // 터미널 피드백 완료 라인
            const completeDiv = document.createElement("div");
            completeDiv.className = "terminal-line success-line";
            completeDiv.textContent = "[SYSTEM] 대시보드 GIS 및 달력 동기화 완료. 타겟 무력화 성공.";
            terminalBody.appendChild(completeDiv);
            terminalBody.scrollTop = terminalBody.scrollHeight;
        }
    }
    
    setTimeout(printNextLine, 500);
}

// 필터 버튼들의 실시간 뱃지 개수 업데이트 (실시간 카운트 동기화)
function updateFilterCounts() {
    // 검색어가 있다면 자연어 검색 엔진을 적용해 일차적으로 필터링이 가해진 데이터를 기틀로 삼습니다.
    let baseEvents = futureCulturalEvents;
    if (activeFilters.search) {
        baseEvents = futureCulturalEvents.filter(event => {
            return matchNaturalLanguage(event, activeFilters.search);
        });
    }

    // 1. 지역별 카운트
    const rAll = baseEvents.length;
    const rSeoul = baseEvents.filter(e => e.title.startsWith("[서울/")).length;
    const rGyeonggi = baseEvents.filter(e => e.title.startsWith("[경기/")).length;
    const rIncheon = baseEvents.filter(e => e.title.startsWith("[인천/")).length;
    
    document.querySelector(".badge-region-all").textContent = rAll;
    document.querySelector(".badge-region-seoul").textContent = rSeoul;
    document.querySelector(".badge-region-gyeonggi").textContent = rGyeonggi;
    document.querySelector(".badge-region-incheon").textContent = rIncheon;
    
    // 2. 종류별 카운트
    const cAll = baseEvents.length;
    const cShow = baseEvents.filter(e => e.category === "공연").length;
    const cExhibit = baseEvents.filter(e => e.category === "전시").length;
    const cMovie = baseEvents.filter(e => e.category === "영화").length;
    const cLibrary = baseEvents.filter(e => e.category === "도서관").length;
    const cLecture = baseEvents.filter(e => e.category === "강연").length;
    const cExp = baseEvents.filter(e => e.category === "체험").length;
    
    document.querySelector(".badge-category-all").textContent = cAll;
    document.querySelector(".badge-category-show").textContent = cShow;
    document.querySelector(".badge-category-exhibit").textContent = cExhibit;
    document.querySelector(".badge-category-movie").textContent = cMovie;
    document.querySelector(".badge-category-library").textContent = cLibrary;
    document.querySelector(".badge-category-lecture").textContent = cLecture;
    document.querySelector(".badge-category-exp").textContent = cExp;
    
    // 3. 요금별 카운트
    const fAll = baseEvents.length;
    const fFree = baseEvents.filter(e => e.isFree).length;
    const fBudget = baseEvents.filter(e => !e.isFree && e.price <= 10000).length;
    
    document.querySelector(".badge-fee-all").textContent = fAll;
    document.querySelector(".badge-fee-free").textContent = fFree;
    document.querySelector(".badge-fee-budget").textContent = fBudget;
    
    // 4. 왼쪽 사이드바 TARGET SCOPE 통계 실시간 연동
    const statsSeoul = document.querySelector(".stats-body .stat-row:nth-child(1) .stat-value");
    if (statsSeoul) statsSeoul.textContent = `${rSeoul} Targets`;
    
    const statsGyeonggi = document.querySelector(".stats-body .stat-row:nth-child(2) .stat-value");
    if (statsGyeonggi) statsGyeonggi.textContent = `${rGyeonggi} Targets`;
    
    const statsIncheon = document.querySelector(".stats-body .stat-row:nth-child(3) .stat-value");
    if (statsIncheon) statsIncheon.textContent = `${rIncheon} Targets`;
    
    const statsTotal = document.querySelector(".stats-body .total-count");
    if (statsTotal) statsTotal.textContent = `${rAll} 건`;
}

// 초기 로딩 및 이벤트 핸들링 바인딩
document.addEventListener("DOMContentLoaded", () => {
    // 🔍 CSV로부터 데이터 세트를 비동기로 가져옵니다.
    loadEventsFromCSV();

    // 1. 작전 지역 필터 클릭 이벤트 바인딩
    const regionPills = document.querySelectorAll("#region-filter-group .filter-pill");
    regionPills.forEach(pill => {
        pill.addEventListener("click", (e) => {
            const btn = e.target.closest(".filter-pill");
            if (!btn) return;
            
            regionPills.forEach(p => p.classList.remove("active"));
            btn.classList.add("active");
            
            activeFilters.region = btn.getAttribute("data-region");
            renderEvents();
        });
    });

    // 2. 타겟 종류 필터 클릭 이벤트 바인딩
    const categoryPills = document.querySelectorAll("#category-filter-group .filter-pill");
    categoryPills.forEach(pill => {
        pill.addEventListener("click", (e) => {
            const btn = e.target.closest(".filter-pill");
            if (!btn) return;
            
            categoryPills.forEach(p => p.classList.remove("active"));
            btn.classList.add("active");
            
            activeFilters.category = btn.getAttribute("data-category");
            renderEvents();
        });
    });

    // 3. 침투 요금 필터 클릭 이벤트 바인딩
    const feePills = document.querySelectorAll("#fee-filter-group .filter-pill");
    feePills.forEach(pill => {
        pill.addEventListener("click", (e) => {
            const btn = e.target.closest(".filter-pill");
            if (!btn) return;
            
            feePills.forEach(p => p.classList.remove("active"));
            btn.classList.add("active");
            
            activeFilters.fee = btn.getAttribute("data-fee");
            renderEvents();
        });
    });

    // 4. 작전 월 선택 드롭다운 체인지 리스너 바인딩
    const monthSelect = document.getElementById("month-select");
    if (monthSelect) {
        monthSelect.addEventListener("change", (e) => {
            const selectedMonth = Number(e.target.value);
            currentCalendarMonth = selectedMonth;
            
            // 캘린더 위 제목 텍스트 갱신
            document.getElementById("calendar-month-title").textContent = `2026년 ${selectedMonth}월`;
            
            // 대형 달력 재생성
            generateLargeCalendar(selectedMonth);
        });
    }

    // 🔍 실시간 기밀 암호검색창 실시간 이벤트 리스너 마운트
    const spySearchInput = document.getElementById("spy-search-input");
    const spySearchClearBtn = document.getElementById("spy-search-clear-btn");
    
    if (spySearchInput && spySearchClearBtn) {
        spySearchInput.addEventListener("input", (e) => {
            const query = e.target.value.trim().toLowerCase();
            activeFilters.search = query;
            
            // X 버튼 가시성
            if (query.length > 0) {
                spySearchClearBtn.style.display = "block";
            } else {
                spySearchClearBtn.style.display = "none";
            }
            
            // 실시간 리포트 피드 및 카운트 뱃지 재정밀 스캔
            renderEvents();
            updateFilterCounts();
        });
        
        spySearchClearBtn.addEventListener("click", () => {
            spySearchInput.value = "";
            spySearchClearBtn.style.display = "none";
            activeFilters.search = "";
            renderEvents();
            updateFilterCounts();
        });
    }

    // GPS 스캔 시뮬레이터 연동
    document.getElementById("btn-run-scan").addEventListener("click", () => {
        runTerminalSimulation();
    });
});
