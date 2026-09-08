# Still HTTP

HTTPのまま閲覧できるウェブサイトを集めています。

サイトを追加するときは `data/sites.csv` に1行足してPull Requestを送ってください。`docs/` はビルド時に生成されるので編集不要です。

```csv
url,name,added_at,note
http://example.com/,Example,2026-09-08,
```

条件は次の3つだけです。

1. URLが `http://` で始まる
2. HTTPSへ転送されず、HTTPで閲覧できる
3. `added_at` が `YYYY-MM-DD` 形式

## API

```text
GET /sites.json
GET /api
GET /api?q=example
```

`/api` はURL、名前、メモを部分一致で検索します。データの追加・修正はAPIではなくPull Requestで受け付けます。

## ビルド

```bash
python scripts/build.py
```

## Cloudflare Pages

```text
Build command: python scripts/build.py
Build output directory: docs
```

## ライセンス

コードはMIT License、`data/` 以下のデータセットはCC0 1.0です。
