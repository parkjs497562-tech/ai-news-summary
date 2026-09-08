import sqlite3


DB_PATH = "news.db"


def connect_db():
    """SQLite 데이터베이스에 연결한다."""
    return sqlite3.connect(DB_PATH)


def create_table():
    """뉴스 테이블이 없으면 생성한다."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            summary TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_unsummarized_news():
    """
    아직 요약되지 않은 뉴스만 가져온다.
    """

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content
        FROM news
        WHERE summary IS NULL
    """)

    news = cursor.fetchall()

    conn.close()

    return news


def get_news_by_id(news_id):
    """특정 ID의 뉴스를 가져온다."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, summary
        FROM news
        WHERE id = ?
    """, (news_id,))

    news = cursor.fetchone()

    conn.close()

    return news


def save_summary(news_id, summary):
    """뉴스의 요약문을 데이터베이스에 저장한다."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE news
        SET summary = ?
        WHERE id = ?
    """, (summary, news_id))

    conn.commit()
    conn.close()

