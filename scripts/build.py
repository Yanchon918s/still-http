#!/usr/bin/env python3
import csv
import html
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "sites.csv"
OUTPUT = ROOT / "docs"
FIELDS = ["url", "name", "added_at", "note"]


def load_sites():
    with SOURCE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"columns must be: {','.join(FIELDS)}")
        sites = list(reader)

    seen = set()
    for line, site in enumerate(sites, start=2):
        parsed = urlsplit(site["url"])
        if parsed.scheme != "http" or not parsed.hostname:
            raise ValueError(f"data/sites.csv:{line}: URL must start with http://")
        try:
            date.fromisoformat(site["added_at"])
        except ValueError as error:
            raise ValueError(f"data/sites.csv:{line}: invalid added_at") from error
        if site["url"] in seen:
            raise ValueError(f"data/sites.csv:{line}: duplicate URL")
        seen.add(site["url"])

    return sorted(sites, key=lambda site: (site["added_at"], site["url"]), reverse=True)


def build_html(sites):
    rows = []
    for site in sites:
        url = html.escape(site["url"], quote=True)
        name = html.escape(site["name"] or site["url"])
        added_at = html.escape(site["added_at"])
        note = html.escape(site["note"])
        rows.append(
            f'<tr><td><a href="{url}">{name}</a></td><td><code>{url}</code></td>'
            f"<td>{added_at}</td><td>{note}</td></tr>"
        )

    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Still HTTP</title>
<style>
body{{max-width:1000px;margin:40px auto;padding:0 20px;font-family:system-ui;line-height:1.6}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:8px;border-bottom:1px solid #ccc;text-align:left}}
code{{overflow-wrap:anywhere}}nav a{{margin-right:12px}}
</style>
</head>
<body>
<h1>Still HTTP</h1>
<p>HTTPのまま閲覧できるウェブサイト。{len(sites)}件。</p>
<nav><a href="sites.csv">CSV</a><a href="sites.json">JSON</a><a href="/api">API</a></nav>
<table><thead><tr><th>サイト</th><th>URL</th><th>追加日</th><th>メモ</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</body>
</html>
'''


def main():
    sites = load_sites()
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "index.html").write_text(build_html(sites), encoding="utf-8")
    (OUTPUT / "sites.json").write_text(
        json.dumps(sites, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "sites.csv").write_text(SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
    (OUTPUT / "_routes.json").write_text(
        '{"version":1,"include":["/api"],"exclude":[]}\n', encoding="utf-8"
    )
    (OUTPUT / "_headers").write_text(
        "/*.json\n  Access-Control-Allow-Origin: *\n\n"
        "/*.csv\n  Access-Control-Allow-Origin: *\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
