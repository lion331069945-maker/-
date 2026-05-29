import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


SYMBOL = "sh600105"
OUTPUT = Path("data/yd_600105_daily.json")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 stock-dashboard-actions",
            "Accept": "application/json,text/plain,*/*",
            "Referer": "https://finance.qq.com/",
        },
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw)


def fetch_tencent_daily(limit: int = 420) -> list[dict]:
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={SYMBOL},day,,,{limit},qfq"
    payload = fetch_json(url)
    node = payload.get("data", {}).get(SYMBOL, {})
    rows = node.get("qfqday") or node.get("day") or []
    daily = []
    for index, row in enumerate(rows):
        open_price = float(row[1])
        close = float(row[2])
        high = float(row[3])
        low = float(row[4])
        volume = float(row[5])
        prev_close = float(rows[index - 1][2]) if index > 0 else open_price
        change = close - prev_close
        change_pct = change / prev_close * 100 if prev_close else 0
        daily.append(
            {
                "date": row[0],
                "open": round(open_price, 4),
                "close": round(close, 4),
                "high": round(high, 4),
                "low": round(low, 4),
                "volume": round(volume, 2),
                "amount": round(volume * close * 100, 2),
                "amplitude": round((high - low) / prev_close * 100, 4) if prev_close else 0,
                "changePct": round(change_pct, 4),
                "change": round(change, 4),
                "turnover": None,
            }
        )
    return daily


def main() -> int:
    last_error = None
    daily = []
    for attempt in range(3):
        try:
            daily = fetch_tencent_daily()
            if daily:
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ValueError) as exc:
            last_error = exc
            time.sleep(2 + attempt)

    if not daily:
        print(f"Failed to fetch daily data: {last_error}", file=sys.stderr)
        return 1

    payload = {
        "symbol": SYMBOL,
        "name": "永鼎股份",
        "market": "SH",
        "source": "Tencent qfqday",
        "updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(daily),
        "latest": daily[-1]["date"],
        "daily": daily,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {OUTPUT} with {len(daily)} rows, latest {daily[-1]['date']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
