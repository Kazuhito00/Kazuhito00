# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## リポジトリ概要

**Kazuhito00 の GitHub プロフィールリポジトリ** (`Kazuhito00/Kazuhito00`)。GitHub プロフィールページとポートフォリオを兼ねる。ポートフォリオデータは SQLite で管理し、静的 HTML ビューア (GitHub Pages) で表示する。

## アーキテクチャ

```
works.db       ← SQLite DB: ポートフォリオデータの唯一の真実のソース
index.html     ← SQLite WASM (sql.js) でブラウザ上から works.db を直接クエリするビューア
add_work.py    ← エントリの追加・編集用 CLI
README.md      ← GitHub プロフィールページ (自己紹介、ブログフィード、リンク)
_old/          ← アーカイブ: migrate.py, generate.py, WORKS.md (移行前の成果物)
```

### works.db スキーマ

- **categories** — id, name (アンカーキー 例: `ObjectDetection`), display_name, sort_order
- **works** — id, category_id (FK), repo_name, repo_url, description, image_url, image_data (BLOB), image_type, sort_order
- **contributions** — id, section (`書籍関連`/`Axross`), description_html, image_url, image_link, image_data (BLOB), image_type, sort_order
- **external_links** — id, section (`Qiita`/`Zenn`/`Kaggle`), body_md, sort_order

画像はアニメーション GIF 対応のため BLOB で格納 (base64 ではない)。ブラウザ側では `URL.createObjectURL()` で表示する。

### index.html

単一ファイルの静的ページ。sql.js (CDN) 経由で `works.db` を読み込み、クライアントサイドでクエリを実行する。

- ライト/ダークモード (`prefers-color-scheme` で自動切替)
- カテゴリフィルタリング (ドロップダウン + 折り畳みカテゴリ一覧)
- テキスト検索 (リポジトリ名、説明文、カテゴリ名を横断)
- カード全体がリンク (クリックで GitHub リポジトリを別タブで開く)
- Contribution セクションは `<details>` を使用 (書籍関連=デフォルト開、Axross=デフォルト閉)

## よく使うコマンド

```bash
# 新規追加 (カテゴリ先頭に追加、画像は自動ダウンロード)
python add_work.py -c ObjectDetection -r Kazuhito00/New-Repo -d "説明" -i "https://image-url.gif"

# ローカル画像で追加
python add_work.py -c ObjectDetection -r Kazuhito00/New-Repo -d "説明" -i ./thumb.png

# カテゴリ末尾に追加
python add_work.py --append -c ObjectDetection -r Kazuhito00/New-Repo -d "説明"

# 既存エントリの編集 (リポジトリ名で検索)
python add_work.py --edit -r mediapipe-python-sample -d "新しい説明"
python add_work.py --edit -r mediapipe-python-sample -i "https://new-image.gif"
python add_work.py --edit -r mediapipe-python-sample -c NewCategory

# ID 指定で編集 (リポジトリ名が曖昧な場合)
python add_work.py --edit --id 42 -d "説明"

# カテゴリ一覧
python add_work.py --list-categories

# 一括操作は直接 SQL
sqlite3 works.db "UPDATE works SET description = '...' WHERE repo_name = '...';"
```

## 自動ワークフロー

`.github/workflows/blog-feed.yml` が1時間ごとに `sarisia/actions-readme-feed@v1` を使って `https://kazuhito00.hatenablog.com/rss` からブログ記事を取得し、`README.md` のフィードセクション (`<!-- feed start -->` 〜 `<!-- feed end -->`) を更新する。フィードセクションは手動編集しないこと。

## 規約

- コミットメッセージは `docs:` プレフィックスを使用
- コンテンツは日本語メイン、英語サブ
- 画像サムネイルは横幅 240px、16:9 で `object-fit: contain` 表示
- 新規エントリはデフォルトでカテゴリ先頭に追加 (新しいものが上)
- `_old/` には移行時のスクリプトをアーカイブ済み。参照用に削除しないこと
