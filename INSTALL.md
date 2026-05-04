# 설치 가이드 — 마우스+키보드만 알면 됩니다

이 가이드는 **컴퓨터 처음 만지는 사람** 기준으로 쓰여있습니다. 모든 명령마다 "이거 입력하면 화면에 뭐가 보이는지" 까지 적혀있어요. 막히면 막힌 단계 캡처 보내주세요.

소요 시간: 20~30분
비용: 무료 (카드 등록 X)

---

## 준비물 3가지

이 3가지를 미리 받아두면 설치가 한 번에 끝납니다.

### 1. Google AI Studio API 키

봇이 AI 두뇌로 쓰는 Gemini 의 비밀번호.

1. Chrome 에서 https://aistudio.google.com/app/apikey 열기
2. 본인 Gmail 로 로그인
3. 화면의 **"API 키 만들기"** 버튼 클릭
4. 새 창이 뜨면 그냥 **"키 만들기"** 클릭 (이름은 아무거나)
5. **`AIzaSy...` 로 시작하는 긴 글자**가 화면에 나타남
6. 옆의 복사 아이콘 클릭 → 메모장에 붙여넣기 (Ctrl+V) → 저장

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
6. 성공 시 BotFather 가 답장으로 **`1234567890:ABCdef...` 형태의 긴 글자**를 줍니다 → 메모장에 복사

### 3. Python 설치

봇을 실행할 프로그램.

1. Chrome 에서 https://python.org/downloads 열기
2. 노란색 큰 **"Download Python"** 버튼 클릭
3. 다운된 파일 (보통 `python-3.13.x-amd64.exe`) 더블클릭으로 실행
4. **⭐ 가장 중요**: 설치 화면 **맨 아래에 "Add python.exe to PATH" 체크박스 반드시 체크** ⭐
5. **"Install Now"** 클릭
6. 설치 끝나면 **"Close"** 클릭

---

## 설치 본격 시작

### STEP 1. PowerShell 열기

**PowerShell** 은 컴퓨터에 글자로 명령 내리는 검은 창입니다.

1. 키보드의 **Windows 키** (왼쪽 아래 깃발 모양) 한 번 누르기
2. `powershell` 이라고 타자
3. 검색결과에 **"Windows PowerShell"** 클릭
4. 검은색 (또는 파란색) 창이 열림. 안에 깜빡이는 커서가 보이면 OK.

화면에 보일 것: `PS C:\Users\사용자이름>` 같은 글자 + 깜빡이는 커서.

### STEP 2. Python 작동 확인

PowerShell 에 입력:
```
python --version
```
[Enter]

✅ **정상**: `Python 3.13.0` 같은 버전 숫자가 나옴.

❌ **에러**: `python을 찾을 수 없습니다` 가 뜨면:
- Python 설치할 때 "Add to PATH" 체크 안 했음
- 가장 빠른 우회: `python` 대신 `py` 명령어 사용
  - 입력: `py --version` → 버전 숫자 뜨면 OK. 이후 모든 명령에서 `python` 자리에 `py` 입력.
- 또는 Python 삭제 후 재설치 (이번엔 PATH 체크 꼭)

### STEP 3. 필요한 도구 5개 설치

PowerShell 에 입력 (한 줄로 통째 복사 → 붙여넣기 → Enter):
```
python -m pip install google-generativeai python-telegram-bot ddgs requests beautifulsoup4
```

✅ **정상**: 화면에 `Collecting...`, `Downloading...`, `Installing...` 같은 메시지가 주르륵 나오다가 마지막에 **`Successfully installed ...`** 한 줄이 뜸. (1~2분 걸림)

❌ **에러**: `pip을 찾을 수 없습니다` 가 뜨면 위 명령에서 `python` 자리에 `py` 사용:
```
py -m pip install google-generativeai python-telegram-bot ddgs requests beautifulsoup4
```

### STEP 4. bot.py 다운로드

bot.py 는 봇의 본체 코드 파일입니다. PowerShell 한 줄로 자동 다운받습니다:

```
Invoke-WebRequest https://raw.githubusercontent.com/wildeconforce/agent-starter-kit/main/bot.py -OutFile $HOME\Desktop\bot.py
```

✅ **정상**: 이 명령은 **메시지 없이 조용히 끝납니다.** 화면에 새 줄이 나오고 다시 `PS C:\Users\사용자>` 가 뜨면 성공.

❌ **에러**: 빨간 글씨로 에러가 뜨면 캡처 보내주세요.

**확인** — 다운로드 됐는지 검증:
```
dir $HOME\Desktop\bot.py
```
[Enter]

✅ **정상**: 파일 정보가 나옴 (예: `Length 8445`, `Name bot.py`).
❌ **에러**: `찾을 수 없습니다` 뜨면 위 다운로드 명령 다시.

### STEP 5. bot.py 안에 키 입력

PowerShell 에 입력:
```
notepad $HOME\Desktop\bot.py
```
[Enter]

✅ **정상**: **메모장 창**이 새로 뜸. 영어/한국어 글자가 가득한 파일이 보임.

메모장 안에서 위쪽 (10~22번째 줄 부근) 의 다음 3줄을 찾으세요:

```python
GOOGLE_API_KEY = "여기에_본인_Google_AI_Studio_키_붙여넣기"
TELEGRAM_BOT_TOKEN = "여기에_본인_봇토큰_붙여넣기"
ALLOWED_USER_IDS = []
```

**수정해야 할 곳 2개**:

1. **`GOOGLE_API_KEY` 줄**:
   - 따옴표 `"` 안의 글자 (`여기에_본인_Google_AI_Studio_키_붙여넣기`) 를 마우스로 드래그해서 선택
   - Delete 키로 지움
   - 준비물 1 에서 받은 API 키 (`AIzaSy...`) 붙여넣기 (Ctrl+V)
   - 결과 예시: `GOOGLE_API_KEY = "AIzaSyBLMQFW7FTf5U7pSqbRGN42QwCAKx5cRkA"`

2. **`TELEGRAM_BOT_TOKEN` 줄**:
   - 마찬가지로 따옴표 안 글자 지우고 준비물 2 의 봇 토큰 (`1234...:ABC...`) 붙여넣기
   - 결과 예시: `TELEGRAM_BOT_TOKEN = "8696980063:AAGVIddm4WpKTYyxGLsIa4jhdI3SiDxiDas"`

**`ALLOWED_USER_IDS = []` 줄은 손대지 마세요.** (선택사항이고 비워두면 본인 + 누구나 사용 가능)

[주의] 따옴표 `""` 와 대괄호 `[]` 는 절대 지우지 마세요. 안의 내용만 바꿉니다.
[주의] 키 앞뒤에 공백이나 줄바꿈이 들어가지 않게 조심.

수정 끝나면:
- 키보드 **Ctrl + S** 로 저장
- 메모장의 X 버튼 으로 닫기

### STEP 6. 봇 실행

PowerShell 로 돌아가서 다음을 차례로 입력 (각 줄 후 Enter):

```
cd ~\Desktop
```
[Enter]

✅ **정상**: 화면 맨 앞이 `PS C:\Users\사용자\Desktop>` 로 바뀜. 다른 메시지 없음.

```
python bot.py
```
[Enter]

✅ **정상**: 약 5~10초 후 다음 글자가 화면에 뜸:
```
==================================================
AI 에이전트 시작 중...
작업 폴더: C:\Users\사용자\Desktop\agent-workspace
모델: gemini-2.5-flash
도구 수: 5
==================================================
에이전트 실행 중! 종료하려면 Ctrl+C
```

동시에 **텔레그램에 본인 봇으로부터 "AI 에이전트 준비 완료" 메시지** 가 옵니다.

❌ **에러 별 대응**:

| 에러 | 해결 |
|---|---|
| `python을 찾을 수 없습니다` | `python bot.py` 대신 `py bot.py` |
| `can't open file 'bot.py': No such file or directory` | bot.py 가 Desktop 에 없음. STEP 4 다시. |
| `Forbidden: bot was blocked by the user` | 텔레그램에서 본인 봇한테 먼저 `/start` 누르고 다시 |
| `401 Unauthorized` | API 키 또는 봇 토큰이 틀림. STEP 5 다시 확인 |
| `[FutureWarning] All support for the google.generativeai...` | **무시해도 됨. 봇은 정상 동작.** |

[주의] PowerShell 창 **닫지 마세요. 닫으면 봇도 꺼집니다.**

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

봇이 만든 파일은 `C:\Users\(본인)\Desktop\agent-workspace\` 안에 쌓입니다.

---

## 컴퓨터 켜질 때 자동 시작 (선택)

PowerShell 창 닫으면 봇 꺼지는 게 싫으면 자동 시작 설정:

1. PowerShell 에 입력:
```
Invoke-WebRequest https://raw.githubusercontent.com/wildeconforce/agent-starter-kit/main/start_bot.bat -OutFile $HOME\Desktop\start_bot.bat
```
✅ **정상**: 메시지 없이 끝남. (다운로드 완료)

2. 키보드 **Win + R** (실행 창 뜸) → 입력:
```
shell:startup
```
[Enter]

✅ **정상**: 시작프로그램 폴더 (윈도우 탐색기 창) 가 열림.

3. 바탕화면에서 `start_bot.bat` 파일을 찾아서 시작프로그램 폴더로 **드래그**.

4. PC 재부팅 후 자동으로 검은 창이 뜨고 봇이 시작됨. 텔레그램에 "AI 에이전트 준비 완료" 알림 옴.

---

## 막히면

**캡처 + 어느 STEP** 알려주세요. 어떤 화면 보이는지 봐야 답할 수 있어요.

자주 묻는 질문은 [README.md](README.md) 의 FAQ 섹션 참고.
