# 수도권 무료 문화생활 사냥꾼 - 수집 기관 데이터베이스 (target_sources.py)

CULTURE_TARGETS = {
    "서울": {
        "통합허브": [
            {"name": "서울문화포털", "url": "https://culture.seoul.go.kr", "type": "hub"},
            {"name": "서울시립미술관", "url": "https://sema.seoul.go.kr", "type": "gallery"},
            {"name": "세종문화회관", "url": "https://www.sejongpac.or.kr", "type": "theater"},
            {"name": "예술의전당", "url": "https://www.sac.or.kr", "type": "theater"},
            {"name": "국립극장", "url": "https://www.ntok.go.kr", "type": "theater"},
            {"name": "서울역사박물관", "url": "https://museum.seoul.go.kr", "type": "gallery"}
        ],
        "공공행정_구청및주민센터": [
            {"name": "강남구청 문화포털", "url": "https://www.gangnam.go.kr/office/gct/main.do", "type": "district"},
            {"name": "마포구청 고시공고", "url": "https://www.mapo.go.kr/site/main/board/notice", "type": "district"},
            {"name": "종로구청 새소식", "url": "https://www.jongno.go.kr/portal/subMain.do?menuNo=400192", "type": "district"},
            {"name": "송파구청 문화체육", "url": "https://www.songpa.go.kr/culture/index.do", "type": "district"},
            {"name": "서초구청 공지사항", "url": "https://www.seocho.go.kr/html/site/seocho/index.html", "type": "district"},
            {"name": "영등포구청 새소식", "url": "https://www.ydp.go.kr", "type": "district"},
            {"name": "용산구청 고시공고", "url": "https://www.yongsan.go.kr", "type": "district"},
            {"name": "성동구청 고시공고", "url": "https://www.sd.go.kr", "type": "district"},
            {"name": "서대문구청 새소식", "url": "https://www.sdm.go.kr", "type": "district"},
            {"name": "은평구청 고시공고", "url": "https://www.ep.go.kr", "type": "district"},
            {"name": "노원구청 문화공지", "url": "https://www.nowon.kr", "type": "district"},
            {"name": "동대문구청 새소식", "url": "https://www.ddm.go.kr", "type": "district"}
        ],
        "도서관_및_공공복합": [
            {"name": "서울도서관 행사안내", "url": "https://lib.seoul.go.kr", "type": "library"},
            {"name": "정독도서관", "url": "https://jdlib.sen.go.kr", "type": "library"},
            {"name": "남산도서관", "url": "https://nslib.sen.go.kr", "type": "library"},
            {"name": "마포중앙도서관", "url": "https://mplib.mapo.go.kr", "type": "library"},
            {"name": "송파글마루도서관", "url": "https://www.splib.or.kr/gmlib", "type": "library"},
            {"name": "문화역서울284", "url": "https://www.seoul284.org", "type": "complex"},
            {"name": "시민청 (서울시청 지하)", "url": "https://www.seoulsisul.or.kr", "type": "complex"}
        ],
        "민간소극장_및_독립서점": [
            {"name": "대학로 소극장 연합(예술경영지원센터)", "url": "https://www.goklas.com", "type": "theater_association"},
            {"name": "홍대 두부공장 (독립예술공간)", "url": "https://www.instagram.com/explore/tags/홍대소극장", "type": "sns_tag"},
            {"name": "창비서교빌딩 (북토크)", "url": "https://www.changbi.com", "type": "bookstore"},
            {"name": "최인아책방 (선릉)", "url": "https://www.instagram.com/choiinabooks", "type": "sns_tag"},
            {"name": "당인리책발전소", "url": "https://www.instagram.com/danginribookplant", "type": "sns_tag"},
            # 신규 소극장 리스트 추가
            {"name": "대학로 소극장 연합 (아르코·대학로예술극장)", "url": "https://theater.arko.or.kr", "type": "theater"},
            {"name": "홍대 클럽빵 (인디뮤직 라이브)", "url": "https://www.instagram.com/clubbbang", "type": "sns_tag"},
            {"name": "신촌 플레이버스 (이색 공연공간)", "url": "https://www.sdm.go.kr/culture", "type": "complex"},
            {"name": "삼청로 소극장", "url": "https://www.instagram.com/explore/tags/삼청로소극장", "type": "sns_tag"}
        ],
        "야외광장_및_대형유통": [
            {"name": "한강사업본부 (여의도/반포 무대)", "url": "https://hangang.seoul.go.kr", "type": "square"},
            {"name": "청계천광장 행사공지", "url": "https://www.sisul.or.kr/open_content/cheonggye/", "type": "square"},
            {"name": "스타필드 코엑스몰 (별마당)", "url": "https://www.starfield.co.kr/coexmall", "type": "mall"},
            {"name": "현대백화점 신촌점 유플렉스 광장", "url": "https://www.ehyundai.com", "type": "mall"}
        ]
    },
    "경기도": {
        "통합허브": [
            {"name": "경기문화플랫폼 (지지씨)", "url": "https://ggc.ggcf.kr", "type": "hub"},
            {"name": "경기아트센터", "url": "https://www.ggac.or.kr", "type": "theater"},
            {"name": "경기도미술관", "url": "https://gmoma.ggcf.kr", "type": "gallery"},
            {"name": "백남준아트센터", "url": "https://njp.ggcf.kr", "type": "gallery"},
            {"name": "경기도박물관", "url": "https://mus.ggcf.kr", "type": "gallery"}
        ],
        "공공행정_시청및주민센터": [
            {"name": "경기도청 고시공고", "url": "https://www.gg.go.kr/bbs/board.do?bsId=49", "type": "gov"},
            {"name": "수원시청 새소식", "url": "https://www.suwon.go.kr/web/saf/board/BD_board.list.do?bbsCd=1002", "type": "district"},
            {"name": "성남시청 고시공고", "url": "https://www.seongnam.go.kr", "type": "district"},
            {"name": "부천시청 새소식", "url": "https://www.bucheon.go.kr", "type": "district"},
            {"name": "용인시청 공지사항", "url": "https://www.yongin.go.kr", "type": "district"},
            {"name": "고양시청 열린광장", "url": "https://www.goyang.go.kr", "type": "district"},
            {"name": "안양시청 고시공고", "url": "https://www.anyang.go.kr", "type": "district"},
            {"name": "화성시청 새소식", "url": "https://www.hscity.go.kr", "type": "district"},
            {"name": "남양주시청 공지사항", "url": "https://www.nyj.go.kr", "type": "district"},
            {"name": "안산시청 고시공고", "url": "https://www.ansan.go.kr", "type": "district"},
            {"name": "평택시청 새소식", "url": "https://www.pyeongtaek.go.kr", "type": "district"},
            {"name": "시흥시청 고시공고", "url": "https://www.siheung.go.kr", "type": "district"},
            {"name": "김포시청 공지사항", "url": "https://www.gimpo.go.kr", "type": "district"},
            {"name": "의정부시청 새소식", "url": "https://www.ui4u.go.kr", "type": "district"}
        ],
        "도서관_및_공공복합": [
            {"name": "경기평생교육학습관", "url": "https://www.ggle.go.kr", "type": "library"},
            {"name": "수원시립선경도서관", "url": "https://www.suwonlib.go.kr/sk", "type": "library"},
            {"name": "성남시립분당도서관", "url": "https://snlib.go.kr/bd", "type": "library"},
            {"name": "고양 아람누리도서관", "url": "https://www.goyanglib.or.kr/aram", "type": "library"},
            {"name": "부천 상동도서관", "url": "https://www.bcl.go.kr", "type": "library"},
            {"name": "경기스타트업캠퍼스 (판교)", "url": "https://www.gcon.or.kr", "type": "complex"}
        ],
        "민간소형공간_및_공방": [
            {"name": "수원 행궁동 독립서점 '브로콜리숲'", "url": "https://www.instagram.com/broccoliforest", "type": "sns_tag"},
            {"name": "동두천 보산동 공방거리", "url": "https://www.instagram.com/explore/tags/보산동공방거리", "type": "sns_tag"},
            {"name": "헤이리 예술마을 사무국", "url": "https://www.heyri.net", "type": "complex"},
            {"name": "일산 백석동 북카페 거리", "url": "https://www.instagram.com/explore/tags/백석동북카페", "type": "sns_tag"},
            # 신규 경기도 소극장 리스트 추가
            {"name": "수원 고색뉴지엄 (복합문화공간)", "url": "https://www.suwon.go.kr/web/goseg", "type": "complex"},
            {"name": "고양시 소극장 연합", "url": "https://www.artgy.or.kr", "type": "theater"},
            {"name": "부천시민소극장", "url": "https://www.bcf.or.kr", "type": "theater"},
            {"name": "의정부 아트캠프 (이색 소극장)", "url": "https://www.uac.or.kr", "type": "theater"}
        ],
        "야외광장_및_대형유통": [
            {"name": "스타필드 수원 (별마당)", "url": "https://www.starfield.co.kr/suwon", "type": "mall"},
            {"name": "스타필드 하남", "url": "https://www.starfield.co.kr/hanam", "type": "mall"},
            {"name": "스타필드 고양", "url": "https://www.starfield.co.kr/goyang", "type": "mall"},
            {"name": "현대아울렛 스페이스원 (다산)", "url": "https://www.hyundaioutlets.com", "type": "mall"},
            {"name": "수원 남문시장 야외무대", "url": "https://www.suwon.go.kr/web/visitsuwon", "type": "market"}
        ]
    },
    "인천": {
        "통합허브": [
            {"name": "인천문화예술포털 (inArt)", "url": "https://inart.iiac.or.kr", "type": "hub"},
            {"name": "인천문화예술회관", "url": "https://www.incheon.go.kr/art", "type": "theater"},
            {"name": "인천시립박물관", "url": "https://www.incheon.go.kr/museum", "type": "gallery"},
            {"name": "인천문화재단 공지사항", "url": "https://www.ifac.or.kr", "type": "hub"}
        ],
        "공공행정_구청및주민센터": [
            {"name": "인천시청 고시공고", "url": "https://www.incheon.go.kr/board/9", "type": "gov"},
            {"name": "연수구청 공지사항", "url": "https://www.yeonsu.go.kr/main/notice.asp", "type": "district"},
            {"name": "부평구청 새소식", "url": "https://www.icbp.go.kr/open_content/main/news/notice.jsp", "type": "district"},
            {"name": "남동구청 고시공고", "url": "https://www.namdong.go.kr", "type": "district"},
            {"name": "서구청 새소식", "url": "https://www.seo.incheon.kr", "type": "district"},
            {"name": "중구청 고시공고", "url": "https://www.icjg.go.kr", "type": "district"},
            {"name": "계양구청 고시공고", "url": "https://www.gyeyang.go.kr", "type": "district"},
            {"name": "미추홀구청 새소식", "url": "https://michu.incheon.kr", "type": "district"}
        ],
        "도서관_및_공공복합": [
            {"name": "인천미추홀도서관", "url": "https://lib.incheon.go.kr/web", "type": "library"},
            {"name": "부평도서관", "url": "https://bplib.ice.go.kr", "type": "library"},
            {"name": "주안영상미디어센터", "url": "https://www.juanmedia.or.kr", "type": "complex"},
            {"name": "인천서구문화회관", "url": "https://iscf.kr", "type": "theater"},
            {"name": "인천나비공원", "url": "https://www.icbp.go.kr/butterfly", "type": "complex"}
        ],
        "민간소형공간_및_개항장": [
            {"name": "인천 개항장 문화지구 (공방/소극장)", "url": "https://www.instagram.com/explore/tags/개항장거리", "type": "sns_tag"},
            {"name": "인천 신포동 재즈클럽 '버텀라인'", "url": "https://www.instagram.com/explore/tags/버텀라인", "type": "sns_tag"},
            {"name": "부평 삼산동 독립서점 '북극서점'", "url": "https://www.instagram.com/bookgeuk", "type": "sns_tag"},
            # 신규 인천 소극장 리스트 추가
            {"name": "인천 문학시어터 (소극장)", "url": "http://www.munhaktheater.oo.ms", "type": "theater"},
            {"name": "부평 아트하우스", "url": "https://www.bpcf.or.kr", "type": "theater"},
            {"name": "인천 떼아뜨르 다락 (소극장)", "url": "https://www.instagram.com/teatredarak", "type": "sns_tag"},
            {"name": "개항장 다락 소극장", "url": "https://www.instagram.com/explore/tags/다락소극장", "type": "sns_tag"}
        ],
        "야외광장_및_대형유통": [
            {"name": "인천아트플랫폼 야외광장", "url": "https://www.inartplatform.kr", "type": "complex"},
            {"name": "송도 트리플스트리트 광장", "url": "https://www.triplestreet.co.kr", "type": "mall"},
            {"name": "스퀘어원 (동춘동)", "url": "https://www.square1.co.kr", "type": "mall"},
            {"name": "인천 신기시장 고객 쉼터 야외무대", "url": "https://www.singimarket.com", "type": "market"}
        ]
    }
}
