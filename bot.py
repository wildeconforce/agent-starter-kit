"""
나만의 AI 텔레그램 에이전트 (v2)
- 파일 읽기/쓰기 (작업 폴더 내)
- 웹 검색 (DuckDuckGo)
- 웹페이지 내용 가져오기
- 시작 시 텔레그램에 "준비 완료" 알림
"""
import os
import asyncio
import google.generativeai as genai
from telegram import Bot
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

# ============ 여기만 수정하세요 ============
GOOGLE_API_KEY = "여기에_본인_Google_AI_Studio_키_붙여넣기"
TELEGRAM_BOT_TOKEN = "여기에_본인_봇토큰_붙여넣기"

# 본인의 텔레그램 user id를 입력하세요 (@userinfobot에게 물어보면 알려줌)
# 비워두면 누구나 봇 사용 가능. 본인만 쓰려면 [123456789] 형태로 입력.
ALLOWED_USER_IDS = []

MODEL_NAME = "gemini-2.5-flash"
# ==========================================

WORKSPACE = os.path.join(os.path.expanduser("~"), "Desktop", "agent-workspace")
os.makedirs(WORKSPACE, exist_ok=True)


def _safe_path(filename: str) -> str:
    """작업 폴더 밖으로 못 나가게 막아주는 안전 함수"""
    target = os.path.abspath(os.path.join(WORKSPACE, filename))
    if not target.startswith(os.path.abspath(WORKSPACE)):
        raise ValueError("작업 폴더 밖은 접근 불가")
    return target


def list_files(directory: str = "") -> str:
    """작업 폴더 또는 하위 폴더의 파일/폴더 목록을 가져온다.

    Args:
        directory: 하위 폴더 이름 (비우면 작업 폴더 자체)
    """
    try:
        target = _safe_path(directory)
        if not os.path.exists(target):
            return f"폴더 없음: {directory}"
        items = os.listdir(target)
        if not items:
            return "(빈 폴더)"
        result = []
        for name in sorted(items):
            full = os.path.join(target, name)
            kind = "[폴더]" if os.path.isdir(full) else "[파일]"
            result.append(f"{kind} {name}")
        return "\n".join(result)
    except Exception as e:
        return f"목록 실패: {e}"


def read_file(filename: str) -> str:
    """작업 폴더에서 텍스트 파일을 읽는다.

    Args:
        filename: 읽을 파일 이름 (예: notes.txt)
    """
    try:
        path = _safe_path(filename)
        if not os.path.exists(path):
            return f"파일 없음: {filename}"
        if os.path.isdir(path):
            return f"이건 폴더입니다: {filename}"
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if len(content) > 10000:
            return content[:10000] + "\n\n...(이하 생략, 너무 길어서 잘림)"
        return content if content else "(빈 파일)"
    except Exception as e:
        return f"읽기 실패: {e}"


def write_file(filename: str, content: str) -> str:
    """작업 폴더에 텍스트 파일을 쓴다 (있으면 덮어쓰기).

    Args:
        filename: 저장할 파일 이름 (예: report.md)
        content: 파일 내용
    """
    try:
        path = _safe_path(filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"저장 완료: {filename} ({len(content)}자)"
    except Exception as e:
        return f"저장 실패: {e}"


def web_search(query: str) -> str:
    """DuckDuckGo로 웹을 검색한다. 최대 5개 결과 반환.

    Args:
        query: 검색어
    """
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                title = r.get("title", "")
                href = r.get("href", "")
                body = r.get("body", "")[:300]
                results.append(f"제목: {title}\nURL: {href}\n요약: {body}")
        return "\n\n---\n\n".join(results) if results else "검색 결과 없음"
    except Exception as e:
        return f"검색 실패: {e}"


def fetch_url(url: str) -> str:
    """웹페이지의 텍스트 내용을 가져온다 (HTML 제거 후).

    Args:
        url: 가져올 페이지 URL
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AIAgent/1.0)"}
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        result = "\n".join(lines)
        if len(result) > 8000:
            result = result[:8000] + "\n\n...(이하 생략)"
        return result if result else "(내용 없음)"
    except Exception as e:
        return f"가져오기 실패: {e}"


TOOLS = [list_files, read_file, write_file, web_search, fetch_url]
SYSTEM_PROMPT = (
    "당신은 한국어로 답하는 유능한 AI 비서입니다. "
    "사용자 요청에 맞춰 도구를 적극 사용하세요:\n"
    f"- 작업 폴더는 {WORKSPACE} 입니다.\n"
    "- 파일 읽기/쓰기는 list_files, read_file, write_file 사용.\n"
    "- 웹 검색은 web_search, 특정 URL 내용은 fetch_url 사용.\n"
    "- 자료 조사 후 정리·글쓰기를 요청받으면 검색 → 페이지 가져오기 → "
    "내용 종합 → write_file 로 저장하는 흐름을 따르세요.\n"
    "- 도구 사용 후 결과를 한국어로 명확하게 설명하세요."
)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    MODEL_NAME,
    tools=TOOLS,
    system_instruction=SYSTEM_PROMPT,
)
chats = {}


async def start(update, context):
    msg = (
        "안녕하세요! AI 에이전트입니다.\n\n"
        "할 수 있는 일:\n"
        "- 작업 폴더 파일 읽기/쓰기\n"
        "- 웹 검색 및 페이지 내용 가져오기\n"
        "- 자료 조사 후 글쓰기/정리\n\n"
        f"작업 폴더: {WORKSPACE}\n\n"
        "예시:\n"
        "- \"AI 트렌드 검색해서 ai-trend.md 로 저장해줘\"\n"
        "- \"agent-workspace 폴더에 뭐 있어?\"\n"
        "- \"notes.txt 읽어줘\""
    )
    await update.message.reply_text(msg)


async def reply(update, context):
    user_id = update.message.from_user.id

    if ALLOWED_USER_IDS and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text(
            f"권한이 없습니다. 본인 user_id ({user_id}) 를 "
            "ALLOWED_USER_IDS 에 추가해주세요."
        )
        return

    user_msg = update.message.text
    if user_id not in chats:
        chats[user_id] = model.start_chat(enable_automatic_function_calling=True)

    try:
        response = chats[user_id].send_message(user_msg)
        text = response.text or "(응답 없음)"
        for i in range(0, len(text), 4000):
            await update.message.reply_text(text[i:i+4000])
    except Exception as e:
        await update.message.reply_text(f"오류: {str(e)[:300]}")


async def post_init(app):
    """봇 시작 시 ALLOWED_USER_IDS 에게 준비 완료 알림 전송"""
    if not ALLOWED_USER_IDS:
        print("[알림] ALLOWED_USER_IDS 가 비어있어 준비 알림은 건너뜀")
        return
    bot: Bot = app.bot
    for uid in ALLOWED_USER_IDS:
        try:
            await bot.send_message(
                chat_id=uid,
                text=(
                    "🟢 AI 에이전트 준비 완료\n"
                    f"작업 폴더: {WORKSPACE}\n"
                    "무엇을 도와드릴까요?"
                ),
            )
            print(f"[알림] {uid} 에게 준비 알림 전송")
        except Exception as e:
            print(f"[알림] {uid} 전송 실패: {e}")


def main():
    print("=" * 50)
    print("AI 에이전트 시작 중...")
    print(f"작업 폴더: {WORKSPACE}")
    print(f"모델: {MODEL_NAME}")
    print(f"도구 수: {len(TOOLS)}")
    print("=" * 50)

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("에이전트 실행 중! 종료하려면 Ctrl+C")
    app.run_polling()


if __name__ == "__main__":
    main()
