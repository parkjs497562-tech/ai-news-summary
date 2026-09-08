# 🤖 AI 뉴스 요약 기능

저장된 뉴스 본문을 **OpenAI API**에 전달하여 핵심 내용을 자동으로 요약하고, 생성된 요약문을 **SQLite 데이터베이스에 저장**하는 기능입니다.

---

## 📌 담당 기능

이번 프로젝트에서 **AI 뉴스 요약 기능**을 담당했습니다.

주요 구현 내용은 다음과 같습니다.

* 뉴스 본문을 OpenAI API에 전달
* AI를 이용한 뉴스 요약
* 요약 결과 SQLite DB 저장
* CLI를 통한 요약 대상 선택
* 이미 요약된 뉴스 중복 처리 방지
* API 오류 발생 시 다음 뉴스로 계속 진행
* 요약 성공/실패 건수 출력
* API Key 환경변수 관리

---

## 🧠 AI 뉴스 요약 방식

뉴스 본문을 **OpenAI API**에 전달하여 요약하도록 구현했습니다.

### 사용 모델

**OpenAI `gpt-5-mini`**

`src/summarizer.py`에서 OpenAI Python SDK를 사용하여 API를 호출합니다.

```python
response = client.responses.create(
    model="gpt-5-mini",
    input=...
)
```

### 요약 기준

AI에게 다음과 같은 조건을 전달했습니다.

* 핵심 내용 중심으로 요약
* 3~5문장으로 작성
* 객관적인 문체 사용
* 불필요한 표현 제거
* 원문에 없는 내용 추가 금지

이를 통해 뉴스마다 요약 형식이 크게 달라지지 않도록 구성했습니다.

---

## 🔄 전체 처리 과정

```text
뉴스 수집
   ↓
SQLite DB 저장
   ↓
뉴스 본문 조회
   ↓
summarizer.py
   ↓
OpenAI API
   ↓
AI 요약문 생성
   ↓
summary 컬럼 저장
```

---

## 🖥️ CLI 기능

사용자가 터미널에서 요약 대상을 직접 지정할 수 있도록 `argparse`를 사용했습니다.

### 특정 뉴스 요약

```bash
python main.py summarize --id 2
```

특정 뉴스 ID 하나만 선택하여 요약합니다.

---

### 미요약 뉴스 요약

```bash
python main.py summarize --unsummarized
```

아직 `summary`가 저장되지 않은 뉴스만 대상으로 합니다.

---

### 전체 미요약 뉴스 요약

```bash
python main.py summarize --all
```

현재 저장된 뉴스 중 아직 요약되지 않은 뉴스를 모두 처리합니다.

---

### 요약 개수 제한

```bash
python main.py summarize --unsummarized --limit 10
```

최대 10개의 뉴스만 처리할 수 있습니다.

---

## 🗄️ 데이터 저장

뉴스 데이터는 SQLite를 사용하여 관리합니다.

### `news` 테이블

| 컬럼        | 역할          |
| --------- | ----------- |
| `id`      | 뉴스 고유 ID    |
| `title`   | 뉴스 제목       |
| `content` | 뉴스 본문       |
| `summary` | AI가 생성한 요약문 |

AI 요약이 성공하면 생성된 요약문을 `summary` 컬럼에 저장합니다.

---

## 🛡️ API 오류 처리

AI API 호출에 실패하더라도 프로그램 전체가 종료되지 않도록 예외 처리를 적용했습니다.

예를 들어 여러 개의 뉴스를 처리하는 중 API 오류가 발생하면:

```text
[INFO] [1/3] ID=1 요약 시작
[ERROR] AI 요약 실패
[INFO] [1/3] ID=1 요약 실패

[INFO] [2/3] ID=2 요약 시작
...
```

와 같이 해당 뉴스는 실패 처리하고 **다음 뉴스의 요약을 계속 진행**하도록 구현했습니다.

마지막에는 성공 및 실패 건수를 출력합니다.

```text
[INFO] 요약 완료: 0건 성공, 3건 실패
```

---

## 🧪 테스트 결과

CLI와 DB 연결 및 API 호출 과정은 실제 환경에서 테스트했습니다.

### 테스트한 기능

* `--id` 뉴스 선택 ✅
* `--unsummarized` 미요약 뉴스 조회 ✅
* `--all` 전체 미요약 뉴스 처리 ✅
* `--limit` 처리 개수 제한 ✅
* SQLite 뉴스 조회 ✅
* API 호출 과정 ✅
* API 오류 발생 시 다음 뉴스로 진행 ✅
* 요약 성공 시 DB 저장 로직 구현 ✅

### API 테스트 결과

코드 구현 및 API 호출 자체는 정상적으로 이루어졌지만, 테스트에 사용한 OpenAI API 계정의 **사용 가능한 크레딧이 없어 실제 AI 요약 결과 생성은 확인하지 못했습니다.**

실제 테스트에서는 다음과 같은 API 오류가 발생했습니다.

```text
Error code: 429
credit_balance_exhausted
You have no credits remaining.
```

따라서 현재 테스트 결과는 다음과 같이 정리할 수 있습니다.

```text
CLI 입력
  ↓
뉴스 조회
  ↓
OpenAI API 요청
  ↓
API 호출 성공 여부 확인
  ↓
크레딧 부족으로 429 오류 발생
  ↓
오류 처리
  ↓
다음 뉴스 계속 처리
```

**API 크레딧 문제는 코드 오류가 아닌 계정의 사용 가능 크레딧 부족으로 발생한 문제입니다.**

크레딧이 충전된 환경에서는 동일한 코드로 실제 AI 요약문을 생성하고 `summary` 컬럼에 저장할 수 있도록 구현했습니다.

---

## 🔐 API Key 관리

OpenAI API Key는 코드에 직접 작성하지 않고 `.env` 파일의 환경변수로 관리했습니다.

```env
OPENAI_API_KEY=your_api_key
```

Python에서는 `python-dotenv`를 사용하여 환경변수를 불러옵니다.

```python
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

또한 API Key가 포함된 `.env` 파일은 `.gitignore`에 등록하여 GitHub에 업로드되지 않도록 했습니다.

```text
.env
news.db
__pycache__/
*.pyc
```

---

## 📂 프로젝트 구조

```text
ai-news-summary/
│
├── .gitignore
├── main.py
│
└── src/
    ├── __init__.py
    ├── database.py
    ├── insert_test_news.py
    └── summarizer.py
```

### 파일 역할

| 파일                    | 역할                       |
| --------------------- | ------------------------ |
| `main.py`             | CLI 명령어 처리 및 전체 요약 흐름 관리 |
| `database.py`         | 뉴스 조회 및 요약 결과 저장         |
| `summarizer.py`       | OpenAI API 호출 및 AI 요약    |
| `insert_test_news.py` | 테스트용 뉴스 데이터 생성           |
| `.gitignore`          | API Key 및 불필요한 파일 제외     |

---

## 🛠️ 사용 기술

* **Python 3**
* **OpenAI API**
* **GPT-5 mini**
* **OpenAI Python SDK**
* **SQLite**
* **argparse**
* **python-dotenv**
* **Git / GitHub**

---

## 💡 구현하면서 확인한 점

이번 구현을 통해 단순히 AI API를 호출하는 것뿐만 아니라,

**뉴스 데이터 조회 → AI API 요청 → 오류 처리 → 결과 저장**

까지 하나의 흐름으로 연결하는 과정을 구현했습니다.

특히 여러 뉴스를 한 번에 처리할 때 API 오류가 발생하더라도 전체 작업이 중단되지 않고 다음 뉴스로 넘어가도록 예외 처리를 적용했습니다.

또한 API Key를 코드에 직접 작성하지 않고 환경변수로 분리하여 **보안상 안전하게 관리할 수 있도록 구성**했습니다.

---

## 👤 담당

**AI 뉴스 요약 기능**

* OpenAI API 연동
* GPT-5 mini 기반 뉴스 요약
* SQLite DB 연동
* CLI 요약 옵션 구현
* API 오류 처리
* 요약 결과 저장
* 환경변수 기반 API Key 관리
* GitHub 코드 관리
