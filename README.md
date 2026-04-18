# 📅 101_calendar — 市場イベント通知 Bot

翌日の株価に影響しそうな経済イベントを毎朝 Discord に通知するボットです。

## 対応イベント

| カテゴリ | 内容 |
|---|---|
| 🇺🇸 雇用 | 米・雇用統計（毎月第1金曜） |
| 🇺🇸 物価 | 米・CPI |
| 🇺🇸 金融政策 | FRB FOMC 政策金利発表 |
| 🇯🇵 金融政策 | 日銀・金融政策決定会合 |
| 🇯🇵 需給 | メジャーSQ（3・6・9・12月） |
| 🇯🇵 権利 | 権利付き最終日・権利落ち日・権利確定日 |
| 🇯🇵 休場 | 祝日・年末年始・大発会・大納会 |

## トリガー

| 方法 | 用途 |
|---|---|
| `workflow_dispatch` | GitHub UI から手動実行 |
| `repository_dispatch` (type: `remote_notify`) | iPhone ショートカット等 外部 API から起動 |

### iPhone ショートカット設定例（毎朝 07:00）

```
URL   : https://api.github.com/repos/trading-for-nouka/101_calendar/actions/workflows/notify.yml/dispatches
方法  : POST
ヘッダー: Authorization: Bearer <PAT_TOKEN>
         Accept: application/vnd.github+json
本文(JSON): { "ref": "main", "event_type": "remote_notify" }
```

## Secrets

| 名前 | 内容 |
|---|---|
| `DISCORD_WEBHOOK` | Discord の Webhook URL |

## ファイル構成

```
101_calendar/
├── notify.py
└── .github/workflows/
    └── notify.yml
```

## イベントの追加・修正

`notify.py` の `ECONOMIC_EVENTS` 辞書に追記するだけです。

```python
"2026-MM-DD": "🇺🇸 イベント名",
```
