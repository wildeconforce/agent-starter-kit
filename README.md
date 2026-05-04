# telegram-ai-agent

폰에서 텔레그램으로 호출하는 나만의 AI 에이전트.
파일 읽기/쓰기 + 웹 검색 + 자료 조사 + 자동 시작.

> 🆕 **컴퓨터 처음 만지는 분은 [INSTALL.md](INSTALL.md) 로 가세요.** 마우스+키보드만 알면 따라할 수 있게 한 줄씩 적혀있습니다.

## 무엇을 할 수 있나

- 작업 폴더의 파일 읽기/쓰기
- 인터넷 검색 (DuckDuckGo)
- 웹페이지 내용 가져오기
- 자료 조사 후 정리·글쓰기
- 컴퓨터 켜질 때 자동 시작
- 시작 시 텔레그램에 "준비 완료" 알림

ChatGPT 처럼 단순 대화만 하는 게 아니라, "AI 트렌드 검색해서 ai-trend.md 로 저장해줘" 같은 실제 작업을 처리합니다.

## 5분 셋업

### 1. 준비물 4가지

- **Google AI Studio API 키** — https://aistudio.google.com/app/apikey (무료, 카드 등록 X)
- **텔레그램 봇 토큰** — 텔레그램에서 `@BotFather` → `/newbot`
- **본인 텔레그램 user ID** — 텔레그램에서 `@userinfobot` → `/start`
- **Python 3.10+** — https://python.org/downloads ("Add to PATH" 반드시 체크)

### 2. 패키지 설치

PowerShell:
```
py -m pip install -r requirements.txt
```

> `python` 대신 `py` 사용 권장 — Python Launcher 라서 설치 시 "Add to PATH" 체크 안 했어도 무조건 작동함. `py` 가 안 되면 `python -m pip install -r requirements.txt` 시도.

### 3. bot.py 키 입력

`bot.py` 상단 3개 변수 채우기:

```python
GOOGLE_API_KEY = "AIzaSy..."
TELEGRAM_BOT_TOKEN = "1234567890:..."
ALLOWED_USER_IDS = [123456789]  # 본인 텔레그램 user ID
```

### 4. 실행

```
python bot.py
```

콘솔에 "AI 에이전트 시작 중..." 떠야 정상.
동시에 텔레그램에 "AI 에이전트 준비 완료" 메시지가 와야 셋업 성공.

### 5. 자동 시작 (선택)

`start_bot.bat` 을 윈도우 시작프로그램 폴더로 이동:

1. Win + R → `shell:startup` 입력 → 폴더 열림
2. `start_bot.bat` 을 그 폴더로 드래그
3. 단, `bot.py` 는 `%USERPROFILE%\Desktop\bot.py` 에 위치해야 함

## 사용 예시

텔레그램 봇에게:

- `"오늘 할 일 3가지를 todo.md 로 저장해줘"` → 파일 작성
- `"agent-workspace 폴더 뭐 있어?"` → 폴더 목록
- `"todo.md 읽어줘"` → 파일 읽기
- `"2026년 AI 트렌드 검색해서 알려줘"` → 웹 검색
- `"ChatGPT 와 Gemini 비교해서 ai-compare.md 로 저장해줘"` → 검색 + 정리 + 저장

작업 결과는 `~/Desktop/agent-workspace/` 에 저장됩니다.

## 구조

```
.
├── bot.py              ← 에이전트 본체 (Python, 약 240줄)
├── requirements.txt    ← 패키지 5개 목록
├── start_bot.bat       ← 자동 시작 스크립트 (Windows, ASCII-safe)
├── README.md           ← 이 파일
└── LICENSE             ← MIT
```

## 보안 모델

- **작업 폴더 격리**: 봇은 `~/Desktop/agent-workspace/` 안에서만 파일 접근. 그 밖은 차단.
- **사용자 화이트리스트**: `ALLOWED_USER_IDS` 에 등록된 텔레그램 user ID 만 응답.
- **외부 데이터 노출 X**: API 키 / 토큰은 본인 PC 에만 저장됨.

## 도구 (Function Calling)

`bot.py` 안에서 Gemini 에 등록된 도구 5개:

| 도구 | 역할 |
|------|------|
| `list_files(directory)` | 작업 폴더 목록 |
| `read_file(filename)` | 파일 읽기 |
| `write_file(filename, content)` | 파일 쓰기 |
| `web_search(query)` | DuckDuckGo 검색 |
| `fetch_url(url)` | 웹페이지 내용 가져오기 |

도구를 더 추가하려면 새 함수를 정의하고 `TOOLS` 리스트에 넣으면 됩니다.

## 라이선스

MIT
