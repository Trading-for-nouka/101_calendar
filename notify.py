import os
import csv
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 環境変数からWebhook URLを取得
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# 日本標準時 (JST) の設定
JST = timezone(timedelta(hours=+9), 'JST')

# =====================
# CSVからイベントを読み込む
# =====================
def load_events(csv_path: Path) -> dict:
    """
    events.csv を読み込んで {date_str: event_str} の辞書を返す
    CSVフォーマット: date,event
    """
    events = {}
    if not csv_path.exists():
        print(f"⚠️ events.csv が見つかりません: {csv_path}")
        return events

    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date  = row["date"].strip()
            event = row["event"].strip()
            if date and event:
                events[date] = event

    print(f"✅ イベント読み込み完了: {len(events)}件 ({csv_path.name})")
    return events


def send_discord_notification(message: str) -> None:
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        response.raise_for_status()
        print("Successfully notified Discord.")
    except Exception as e:
        print(f"Failed to send notification: {e}")


def main():
    # CSVはnotify.pyと同じフォルダに置く
    csv_path = Path(__file__).parent / "events.csv"
    ECONOMIC_EVENTS = load_events(csv_path)

    # 日本時間での翌日を取得
    now_jst      = datetime.now(JST)
    tomorrow_jst = now_jst + timedelta(days=1)
    tomorrow_str = tomorrow_jst.strftime("%Y-%m-%d")

    event = ECONOMIC_EVENTS.get(tomorrow_str)

    if event:
        msg = (
            f"[101_calendar] 🔔 **【明日】の経済イベント予定** ({tomorrow_str})\n"
            f"---------------------------\n"
            f"{event}"
        )
    else:
        msg = f"[101_calendar] 📅 {tomorrow_str}：明日の主要な予定はありません。"

    if DISCORD_WEBHOOK:
        send_discord_notification(msg)
    else:
        print("Error: DISCORD_WEBHOOK is not set.")
        print(f"本日の確認結果: {msg}")


if __name__ == "__main__":
    main()
