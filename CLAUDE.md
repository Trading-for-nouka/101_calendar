# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

翌日の株価に影響しそうな経済イベントを Discord に通知する GitHub Actions ボット。日本株・米株トレーダー向けに JST ベースで動作する。

## 実行方法

ローカルでテストする場合：

```bash
pip install requests
DISCORD_WEBHOOK=<your_webhook_url> python notify.py
```

Webhook URL なしで動作確認（通知は送られず、エラーメッセージのみ出力）：

```bash
python notify.py
```

GitHub Actions からの起動：
- **手動**: GitHub UI の `workflow_dispatch` から実行
- **外部トリガー**: `repository_dispatch` (type: `remote_notify`) を GitHub API に POST

## アーキテクチャ

単一ファイル構成（`notify.py`）。

**データフロー：**
1. JST の現在時刻を取得 → 翌日の日付文字列（`YYYY-MM-DD`）を生成
2. `ECONOMIC_EVENTS` 辞書でその日付を検索
3. 一致するイベントがあれば Discord に通知、なければ「予定なし」メッセージを送信
4. `DISCORD_WEBHOOK` 環境変数が未設定の場合はエラーを出力して終了

**主要な関数：**
- `main()` — 日付計算・イベント検索・メッセージ生成
- `send_discord_notification(message)` — Discord Webhook への POST

## イベントデータの管理

`ECONOMIC_EVENTS` は `notify.py` 内のハードコードされた辞書。キーは `"YYYY-MM-DD"` 形式、値は絵文字 + 日本語テキスト。

イベント追加時のフォーマット：

```python
"2026-MM-DD": "🇺🇸 イベント名",
```

カテゴリ別の絵文字慣例：
- `🇺🇸` — 米国イベント（雇用統計、CPI、FOMC）
- `🇯🇵` — 日本イベント（祝日、SQ、日銀、権利日）
- FOMC の時刻は米夏時間 `2:00`、冬時間 `3:00`（JST 表記）

## Secrets

GitHub リポジトリに以下のシークレットを設定する必要がある：

| 名前 | 内容 |
|---|---|
| `DISCORD_WEBHOOK` | Discord の Webhook URL |
