import sqlite3


DB_PATH = "news.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


news_list = [
    (
        "삼성전자, AI 반도체 사업 확대",
        "삼성전자가 인공지능 반도체 사업을 확대한다. "
        "회사는 AI 관련 기술 개발과 연구에 대한 투자를 늘리고 "
        "글로벌 시장에서 경쟁력을 강화할 계획이라고 밝혔다."
    ),
    (
        "정부, 청년 취업 지원 정책 발표",
        "정부가 청년들의 취업을 지원하기 위한 새로운 정책을 발표했다. "
        "청년 구직자를 대상으로 직업 교육과 취업 지원 프로그램을 확대하고 "
        "기업의 청년 채용을 지원할 계획이다."
    ),
    (
        "한국 프로야구, 새로운 시즌 준비",
        "한국 프로야구 구단들이 새로운 시즌을 앞두고 훈련에 돌입했다. "
        "각 구단은 선수들의 체력과 전술을 점검하며 시즌 준비에 박차를 가하고 있다."
    )
]


for title, content in news_list:
    cursor.execute(
        """
        INSERT INTO news (title, content)
        VALUES (?, ?)
        """,
        (title, content)
    )


conn.commit()
conn.close()


print("테스트 뉴스 3개가 저장되었습니다.")