import os

from dotenv import load_dotenv
from openai import OpenAI


# .env 파일에서 환경변수 불러오기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY가 설정되지 않았습니다."
    )


# OpenAI 클라이언트
client = OpenAI(api_key=api_key)


def summarize_text(text):
    """
    뉴스 본문을 OpenAI API에 전달하여
    요약문을 반환한다.

    API 오류가 발생하면 None을 반환한다.
    """

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=f"""
다음 뉴스 기사를 핵심 내용 중심으로 요약해주세요.

조건:
- 핵심 내용을 중심으로 작성
- 3~5문장
- 객관적인 문체
- 불필요한 표현 제거
- 원문에 없는 내용은 추가하지 않기

[뉴스 본문]
{text}
"""
        )

        return response.output_text

    except Exception as e:
        print(f"[ERROR] AI 요약 실패: {e}")
        return None

