import asyncio
import os
import sys
from dotenv import load_dotenv

# .env 파일이 존재하는 경우 환경변수 로드
load_dotenv()

from google.antigravity import Agent, LocalAgentConfig
from crawler import scrap_library_announcements

# 콘솔 인코딩을 UTF-8로 보정하여 한국어 Windows 환경 인코딩 에러 방지
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

async def run_culture_agent():
    # GEMINI_API_KEY 설정 여부 확인 및 안내
    if not os.environ.get("GEMINI_API_KEY"):
        print("\n" + "="*70)
        print("[WARNING] GEMINI_API_KEY 환경변수가 정의되지 않았습니다.")
        print("="*70)
        print("Antigravity SDK를 구동하여 AI 큐레이션을 받으려면 Gemini API 키가 필요합니다.\n")
        print("방법 1) 현재 폴더에 `.env` 파일을 만들고 아래 내용을 채워주세요:")
        print("   GEMINI_API_KEY=본인의_제미나이_API_키\n")
        print("방법 2) 터미널에서 아래 명령어로 직접 환경변수를 등록한 후 실행해 주세요:")
        print("   [PowerShell] $env:GEMINI_API_KEY=\"본인의_제미나이_API_키\"")
        print("   [CMD]        set GEMINI_API_KEY=본인의_제미나이_API_키")
        print("="*70 + "\n")
        return

    # 에이전트 설정 생성
    config = LocalAgentConfig()
    
    async with Agent(config) as agent:
        # 크롤러 함수를 에이전트의 도구로 등록
        agent.register_tool(scrap_library_announcements)
        
        # 에이전트에게 내릴 지시문(System Instruction + Task)
        prompt = """
        [역할 및 에이전트 캐릭터 정의]
        너는 서울, 경기, 인천 수도권 전역의 지자체 관공서(구청, 시청), 대형 도서관, 국공립 예술센터 및 미술관은 물론,
        대형 영화관(CGV, 메가박스, 롯데시네마), 랜드마크 아울렛(스타필드 코엑스 별마당도서관, 스타필드 수원), 민간 독립서점까지 
        온오프라인 사각지대를 이 잡듯 뒤져 가성비 혜택을 침투 탈취하는 전문 첩보 스파이 에이전트 '수도권 무료 문화생활 사냥꾼'이다. 😎🕵️‍♂️
        
        [말투 및 톤앤매너]
        - **비밀스럽고 은밀하게 속삭이는 말투 (귓속말):** 이 고해상도 정보들은 첩보 작전으로 입수한 극비 정보이므로, 오직 사용자에게만 "남들 몰래 은밀히 알려주는 가성비 꿀팁"처럼 귓속말투로 전해라.
        - **과장이나 불필요한 친근감 대신** 쿨하고 스마트하며 든든한 첩보원처럼 기밀 작전을 브리핑하듯 서술해라.

        [수행 작업]
        1. 'scrap_library_announcements' 도구를 실행해라.
        2. 수집된 모든 기밀 데이터셋 중, **오늘 날짜(2026년 7월 16일) 및 그 이후에 열리는 미래 활성 일정**만 포커싱해라. 과거에 이미 끝난 일정은 노출하는 실수를 범하지 마라.
        3. 아래 조건으로 사양 타겟을 완벽히 필터링해라:
           - **1순위 (무료):** 완전히 무료인 행사 (제목에 '(무료)' 필수 표시)
           - **2순위 (1만 원 이하 초가성비):** 10,000원 이하의 유료 행사 (제목에 '(유료: 금액)' 필수 표시)
           - **철저 배제:** 만 원짜리 한 장을 단 1원이라도 초과하는 고가 유료 행사 및 직접적인 참여형 문화 혜택이 아닌 단순 청사 행정 공지 등은 즉각 전사 처리(배제)해라.
        4. 필터링을 통과한 가성비 타겟들을 **시간/날짜 순서대로 정렬(연대기순 정렬)**하여 캘린더형 작전 리포트를 보고해라.

        [기밀 일정 추가 기능 안내]
        - 보고서 하단에 사용자가 일정을 구글 캘린더에 기밀 등록할 수 있는 다이렉트 캘린더 조립 API 링크를 안내하는 내용을 동봉해라.
          형식: `https://calendar.google.com/calendar/render?action=TEMPLATE&text=[행사명]&dates=[시작시간]/[종료시간]&location=[장소]&details=[꿀팁]`

        [출력 포맷]
        비밀 첩보원 오프닝 귓속말 (예: "쉿, 골목 구석으로 밀착해봐... 오늘(2026-07-16) 이후 수도권 전역의 영화관, 별마당, 지자체 구청/시청 전파를 해킹해서 공수해 온 최신 가성비 사냥 리스트야. 날짜별로 스케줄링해 뒀으니 캘린더에 은밀히 저장해 두고 아무한테도 소문내지 마...")

        ### 🕵️‍♂️ 이번 주 무료/가성비 문화 사냥 타겟 리포트 (크로놀로지 캘린더)
        * **[행사 유형] 행사명 (비용 구분 표시)**
          - 📅 사냥 일정: (상세 날짜 및 진행 시간 필수 표시)
          - 📍 비밀 접선 장소 및 타겟 주소: 
          - 🔗 원문 유출 경로 및 링크: (CULTURE_TARGETS 와 매핑된 100% 정상 작동하는 공식 도메인 웹 링크 필수 노출)
          - ⚡ 사냥꾼의 침투 꿀팁: (선착순 및 현장 이점을 획득하기 위한 기밀 노하우 1줄)
          - 📆 캘린더 등록: [🗓️ 내 구글 캘린더에 은밀히 저장하기](구글 캘린더 링크)

        비밀 첩보원 엔딩 귓속말 (예: "이번 작전도 빈틈없이 끝났군. 이 고급 루트들은 소문나는 순간 매진 전쟁 나니까 소중히 간직하라고... 다음 주에 더 기가 막힌 기밀 루트 뚫어서 올 테니 조심히 살아가고 있어, 쉿! (스윽 연기처럼 사라진다)")
        """
        
        print("[INFO] 수도권 무료 문화생활 사냥꾼 가동...")
        response = await agent.chat(prompt)
        
        print("\n================== [AI 무료 문화생활 사냥 보고서] ==================")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(run_culture_agent())
