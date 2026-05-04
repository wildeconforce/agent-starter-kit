# Mac 설치 가이드 — 마우스+키보드만 알면 됩니다

이 가이드는 **Mac 처음 만지는 사람** 기준으로 쓰여있습니다. 모든 명령마다 "이거 입력하면 화면에 뭐가 보이는지" 까지 적혀있어요. 막히면 막힌 단계 캡처 보내주세요.

소요 시간: 20~30분
비용: 무료 (카드 등록 X)

> Windows 사용자는 [INSTALL.md](INSTALL.md) 로 가세요.

---

## 준비물 3가지

이 3가지를 미리 받아두면 설치가 한 번에 끝납니다.

### 1. Google AI Studio API 키

봇이 AI 두뇌로 쓰는 Gemini 의 비밀번호.

1. Safari/Chrome 에서 https://aistudio.google.com/app/apikey 열기
2. 본인 Gmail 로 로그인
3. 화면의 **"API 키 만들기"** 버튼 클릭
4. 새 창이 뜨면 그냥 **"키 만들기"** 클릭 (이름은 아무거나)
5. **`AIzaSy...` 로 시작하는 긴 글자**가 화면에 나타남
6. 옆의 복사 아이콘 클릭 → 메모앱 또는 텍스트편집기에 붙여넣기 (Cmd+V) → 저장

[주의] "결제 정보를 등록하세요" 같은 창이 뜨면 그냥 닫으세요. **무료로 충분합니다. 카드 등록 절대 X.**

### 2. 텔레그램 봇 토큰

내 봇의 비밀번호.

1. 핸드폰에서 텔레그램 앱 열기
2. 위쪽 검색창에 `@BotFather` 검색
3. BotFather (파란 체크 마크 봇) 클릭해서 들어감
4. 채팅창에 `/newbot` 입력 후 전송
5. 봇이 묻는 대로 답하기:
   - **"Alright, a new bot..."** → 봇 이름 입력 (예: 나의AI에이전트)
   - **"Good. Now let's choose a username..."** → username 입력. **반드시 `_bot` 으로 끝나야 함** (예: `myagent_2026_bot`)
6. 성공 시 BotFather 가 답장으로 **`1234567890:ABCdef...` 형태의 긴 글자**를 줍니다 → 메모앱에 복사

### 3. Python 설치

봇을 실행할 프로그램. macOS 는 기본적으로 Python 3 가 없거나 너무 오래된 버전이니 새로 설치합니다.

1. Safari 에서 https://python.org/downloads 열기
2. 노란색 큰 **"Download Python"** 버튼 클릭 (macOS 용 .pkg 파일이 다운됨)
3. 다운된 파일 (`python-3.13.x-macos11.pkg`) 더블클릭으로 실행
4. 설치 마법사 따라가기 (계속 → 계속 → 동의 → 설치)
5. 관리자 비밀번호 묻는 창 뜨면 입력
6. "설치 성공" 메시지 뜨면 완료

---

## 설치 본격 시작

### STEP 1. Terminal 열기

**Terminal** 은 Mac 에서 글자로 명령 내리는 검은 창입니다.

1. 키보드의 **⌘ Command + Space** 동시에 누르기 (Spotlight 검색 창 뜸)
2. `terminal` 또는 `터미널` 이라고 타자
3. 검색결과에 **"터미널"** 클릭 (Enter 도 OK)
4. 검은색 (또는 흰색) 창이 열림. 안에 깜빡이는 커서가 보이면 OK.

화면에 보일 것: `사용자이름@MacBook ~ %` 같은 글자 + 깜빡이는 커서.

### STEP 2. Python 작동 확인

Terminal 에 입력:
```
python3 --version
```
[Enter]

✅ **정상**: `Python 3.13.0` 같은 버전 숫자가 나옴.

❌ **에러**: `python3: command not found` 가 뜨면:
- Python 설치가 제대로 안 된 것. 준비물 3 단계 다시 (python.org 에서 .pkg 다운로드 → 설치)
- 또는 Terminal 완전히 닫고 (⌘+Q) 새로 열어보기

### STEP 3. 필요한 도구 5개 설치

Terminal 에 입력 (한 줄로 통째 복사 → 붙여넣기 → Enter):
```
python3 -m pip install google-generativeai python-telegram-bot ddgs requests beautifulsoup4
```

✅ **정상**: 화면에 `Collecting...`, `Downloading...`, `Installing...` 같은 메시지가 주르륵 나오다가 마지막에 **`Successfully installed ...`** 한 줄이 뜸. (1~2분 걸림)

❌ **에러**: `pip is not the recommended way` 같은 경고가 떠도 무시 가능. **`Successfully installed`** 가 마지막에 뜨면 OK.

❌ **에러**: `Permission denied` 가 뜨면 명령에 `--user` 옵션 추가:
```
python3 -m pip install --user google-generativeai python-telegram-bot ddgs requests beautifulsoup4
```

### STEP 4. bot.py 다운로드

bot.py 는 봇의 본체 코드 파일입니다. Terminal 한 줄로 자동 다운받습니다:

```
curl -o ~/Desktop/bot.py https://raw.githubusercontent.com/wildeconforce/agent-starter-kit/main/bot.py
```

✅ **정상**: 다운로드 진행 막대가 뜨고 끝나면 `100   8445  100  8445` 같은 숫자가 보임.

❌ **에러**: `command not found: curl` 이 뜨면 (거의 없음, Mac 기본 내장):
```
wget -O ~/Desktop/bot.py https://raw.githubusercontent.com/wildeconforce/agent-starter-kit/main/bot.py
```

**확인** — 다운로드 됐는지 검증:
```
ls -la ~/Desktop/bot.py
```
[Enter]

✅ **정상**: 파일 정보가 나옴 (예: `-rw-r--r--  1 user  staff  8445 ... bot.py`).
❌ **에러**: `No such file or directory` 뜨면 위 다운로드 명령 다시.

### STEP 5. bot.py 안에 키 입력

Terminal 에 입력:
```
open -e ~/Desktop/bot.py
```
[Enter]

✅ **정상**: **TextEdit (텍스트편집기) 창**이 새로 뜸. 영어/한국어 글자가 가득한 파일이 보임.

[참고] TextEdit 가 자동 서식 모드 (rich text) 로 열릴 수 있습니다. 메뉴 → "포맷" → "일반 텍스트로 만들기" 한 번 누르고 진행하면 안전합니다.

TextEdit 안에서 위쪽 (10~22번째 줄 부근) 의 다음 3줄을 찾으세요:

```python
GOOGLE_API_KEY = "여기에_본인_Google_AI_Studio_키_붙여넣기"
TELEGRAM_BOT_TOKEN = "여기에_본인_봇토큰_붙여넣기"
ALLOWED_USER_IDS = []
```

**수정해야 할 곳 2개**:

1. **`GOOGLE_API_KEY` 줄**:
   - 따옴표 `"` 안의 글자를 마우스로 드래그해서 선택
   - Delete 키로 지움
   - 준비물 1 의 API 키 (`AIzaSy...`) 붙여넣기 (Cmd+V)
   - 결과 예시: `GOOGLE_API_KEY = "AIzaSyBLMQFW7FTf5U7pSqbRGN42QwCAKx5cRkA"`

2. **`TELEGRAM_BOT_TOKEN` 줄**:
   - 마찬가지로 따옴표 안 글자 지우고 준비물 2 의 봇 토큰 붙여넣기
   - 결과 예시: `TELEGRAM_BOT_TOKEN = "8696980063:AAGVIddm4WpKTYyxGLsIa4jhdI3SiDxiDas"`

**`ALLOWED_USER_IDS = []` 줄은 손대지 마세요.** (선택사항이고 비워두면 봇 작동)

[주의] 따옴표 `""` 와 대괄호 `[]` 는 절대 지우지 마세요. 안의 내용만 바꿉니다.
[주의] 키 앞뒤에 공백이나 줄바꿈이 들어가지 않게 조심.

수정 끝나면:
- 키보드 **⌘ Cmd + S** 로 저장
- TextEdit 창 빨간 닫기 버튼

### STEP 6. 봇 실행

Terminal 로 돌아가서 다음을 차례로 입력 (각 줄 후 Enter):

```
cd ~/Desktop
```
[Enter]

✅ **정상**: 화면 맨 앞이 `사용자이름@MacBook Desktop %` 로 바뀜. 다른 메시지 없음.

```
python3 bot.py
```
[Enter]

✅ **정상**: 약 5~10초 후 다음 글자가 화면에 뜸:
```
==================================================
AI 에이전트 시작 중...
작업 폴더: /Users/사용자/Desktop/agent-workspace
모델: gemini-2.5-flash
도구 수: 5
==================================================
에이전트 실행 중! 종료하려면 Ctrl+C
```

동시에 **텔레그램에 본인 봇으로부터 "AI 에이전트 준비 완료" 메시지** 가 옵니다.

❌ **에러 별 대응**:

| 에러 | 해결 |
|---|---|
| `python3: command not found` | 준비물 3 다시 (Python 설치) |
| `can't open file 'bot.py': [Errno 2] No such file or directory` | bot.py 가 Desktop 에 없음. STEP 4 다시. |
| `Forbidden: bot was blocked by the user` | 텔레그램에서 본인 봇한테 먼저 `/start` 누르고 다시 |
| `401 Unauthorized` | API 키 또는 봇 토큰이 틀림. STEP 5 다시 확인 |
| `[FutureWarning] All support for the google.generativeai...` | **무시해도 됨. 봇은 정상 동작.** |

[주의] Terminal 창 **닫지 마세요. 닫으면 봇도 꺼집니다.**

### STEP 7. 텔레그램에서 봇 사용

1. 핸드폰에서 텔레그램 열기
2. 위 검색창에 본인 봇 username 검색 (예: `@myagent_2026_bot`)
3. 봇 채팅방 들어가서 **"시작"** 버튼 또는 `/start`
4. 봇이 인사 답장. 그 다음 자유롭게 명령:
   - `안녕! 오늘 뭐 할까?` → 단순 대화
   - `오늘 할 일 3가지를 todo.md 파일로 저장해줘` → 파일 저장
   - `agent-workspace 폴더 뭐 있어?` → 폴더 목록
   - `2026년 AI 트렌드 검색해서 알려줘` → 웹 검색
   - `ChatGPT 와 Gemini 비교해서 ai-compare.md 로 저장해줘` → 검색 + 정리 + 파일

봇이 만든 파일은 `~/Desktop/agent-workspace/` 안에 쌓입니다 (Finder 에서: 사용자 → 데스크탑 → agent-workspace).

---

## Terminal 창 닫지 않고 자동 시작하기 (선택)

Terminal 닫으면 봇 꺼지는 게 싫으면, 더블클릭으로 봇 키는 스크립트 받기:

1. Terminal 에 입력:
```
curl -o ~/Desktop/start_bot.command https://raw.githubusercontent.com/wildeconforce/agent-starter-kit/main/start_bot.command
```
✅ **정상**: 다운로드 진행 막대 뜨고 완료.

2. 실행 권한 부여:
```
chmod +x ~/Desktop/start_bot.command
```
✅ **정상**: 메시지 없이 끝남.

3. 이제 Finder 에서 바탕화면의 `start_bot.command` 더블클릭하면 봇 자동 시작.

[주의] 처음 더블클릭 시 macOS 가 **"확인되지 않은 개발자"** 경고를 띄울 수 있습니다.
- 시스템 설정 → 개인정보 보호 및 보안 → "그래도 열기" 클릭
- 또는 Finder 에서 파일 우클릭 → "열기" → "열기" 한 번 더 → 이후로는 더블클릭 OK

### Mac 부팅 시 자동 실행 (옵션)

매번 더블클릭 안 하고 자동으로 봇 켜지게 하려면:
1. 시스템 설정 → 일반 → 로그인 항목
2. **"+"** 버튼 클릭
3. `~/Desktop/start_bot.command` 선택 후 추가
4. 재부팅 시 자동 시작

---

## 막히면

**캡처 + 어느 STEP** 알려주세요. 어떤 화면 보이는지 봐야 답할 수 있어요.

자주 묻는 질문은 [README.md](README.md) 의 FAQ 섹션 참고.
