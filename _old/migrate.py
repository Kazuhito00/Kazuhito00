"""WORKS.md をパースして works.db に移行するスクリプト"""

import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "works.db"
WORKS_MD = Path(__file__).parent / "WORKS.md"


def create_schema(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS works (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL REFERENCES categories(id),
            repo_name TEXT,
            repo_url TEXT,
            description TEXT,
            image_url TEXT,
            image_data BLOB,
            image_type TEXT,
            sort_order INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            description_html TEXT,
            image_url TEXT,
            image_link TEXT,
            image_data BLOB,
            image_type TEXT,
            sort_order INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS external_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            body_md TEXT,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
    """)


def parse_contributions(text: str, conn: sqlite3.Connection):
    """Contribution セクション (<details> ブロック) をパース"""
    # 書籍関連 と Axross の details ブロックを抽出
    details_pattern = re.compile(
        r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<table>(.*?)</table>\s*</details>',
        re.DOTALL,
    )

    for match in details_pattern.finditer(text):
        section_name = match.group(1).strip()
        table_html = match.group(2)
        parse_contribution_table(section_name, table_html, conn)


def parse_contribution_table(section: str, table_html: str, conn: sqlite3.Connection):
    """Contribution テーブルの各行をパース"""
    # <tr> で分割 (重複 <tr> タグにも対応)
    rows = re.split(r'(?:<tr>\s*)+', table_html)

    sort_order = 0
    for row in rows:
        row = row.strip()
        if not row or '<th' in row:
            continue

        # 画像URL抽出
        img_match = re.search(r'<img\s+src="([^"]+)"', row)
        image_url = img_match.group(1) if img_match else None

        # 画像リンク抽出
        link_match = re.search(r'<a\s+href="([^"]+)">\s*<img', row)
        image_link = link_match.group(1) if link_match else None

        # 説明HTML (2つ目の <td> の中身)
        td_matches = list(re.finditer(r'<td[^>]*>(.*?)</td>', row, re.DOTALL))
        desc_html = td_matches[1].group(1).strip() if len(td_matches) >= 2 else ""

        image_type = _guess_image_type(image_url) if image_url else None

        conn.execute(
            "INSERT INTO contributions (section, description_html, image_url, image_link, image_data, image_type, sort_order) "
            "VALUES (?, ?, ?, ?, NULL, ?, ?)",
            (section, desc_html, image_url, image_link, image_type, sort_order),
        )
        sort_order += 1


def parse_repositories(text: str, conn: sqlite3.Connection):
    """Repositories セクションをパース"""
    # Repositories セクションを抽出 (## Repositories の後の <table>...</table>)
    repo_section = re.search(
        r'## <a name="#Repositories">Repositories</a>.*?<table>(.*)</table>',
        text,
        re.DOTALL,
    )
    if not repo_section:
        return

    table_content = repo_section.group(1)

    # カテゴリヘッダ (<th>) で分割
    # パターン: <th ...><a name="CategoryName">表示名</a> ...
    parts = re.split(r'<tr>\s*<th[^>]*>(.*?)</th>\s*</tr>', table_content, flags=re.DOTALL)

    cat_sort = 0
    for i in range(1, len(parts), 2):
        header_html = parts[i]
        entries_html = parts[i + 1] if i + 1 < len(parts) else ""

        # カテゴリ名抽出
        name_match = re.search(r'<a\s+name="([^"]+)">(.*?)</a>', header_html)
        if not name_match:
            continue

        cat_name = name_match.group(1)
        cat_display = name_match.group(2).strip()

        conn.execute(
            "INSERT INTO categories (name, display_name, sort_order) VALUES (?, ?, ?)",
            (cat_name, cat_display, cat_sort),
        )
        cat_id = conn.execute(
            "SELECT id FROM categories WHERE name = ?", (cat_name,)
        ).fetchone()[0]
        cat_sort += 1

        parse_work_entries(cat_id, entries_html, conn)


def parse_work_entries(cat_id: int, html: str, conn: sqlite3.Connection):
    """カテゴリ内の各リポジトリエントリをパース"""
    # <td width="220"> を区切りとしてエントリを分割
    # (<tr> が欠落しているケースにも対応)
    parts = re.split(r'(?:\s*</tr>\s*)?(?:\s*<tr>\s*)?(?:\s*)<td\s+width="220">', html)

    sort_order = 0
    for part in parts:
        part = part.strip()
        if not part or '<th' in part:
            continue

        # 画像URL (最初の <td> 内)
        img_match = re.search(r'<img\s+src="([^"]+)"', part)
        image_url = img_match.group(1) if img_match else None

        # リポジトリリンク (2つ目の <td> 内)
        repo_match = re.search(r'<a\s+href="([^"]+)">\[([^\]]+)\]</a>', part)
        repo_url = repo_match.group(1) if repo_match else None
        repo_name = repo_match.group(2) if repo_match else None

        # 説明文 (リポジトリリンクの後の <br> 以降)
        desc = ""
        if repo_match:
            # 2つ目の <td> の中身を取得
            td_matches = list(re.finditer(r'<td[^>]*>(.*?)</td>', part, re.DOTALL))
            if td_matches:
                # 最初の (or 唯一の) <td> がリポジトリ情報
                td_content = td_matches[0].group(1).strip()
                # リンク部分を除去して残りを説明文とする
                after_link = re.sub(
                    r'<a\s+href="[^"]*">\[[^\]]*\]</a>\s*<br>\s*', '', td_content
                )
                # HTMLタグ除去して整形
                desc = re.sub(r'<br\s*/?>\s*', '\n', after_link).strip()
                desc = re.sub(r'<[^>]+>', '', desc).strip()

        if not repo_name and not image_url:
            continue

        image_type = _guess_image_type(image_url) if image_url else None

        conn.execute(
            "INSERT INTO works (category_id, repo_name, repo_url, description, image_url, image_data, image_type, sort_order) "
            "VALUES (?, ?, ?, ?, ?, NULL, ?, ?)",
            (cat_id, repo_name, repo_url, desc, image_url, image_type, sort_order),
        )
        sort_order += 1


def parse_external_links(text: str, conn: sqlite3.Connection):
    """末尾の Qiita, Zenn, Kaggle セクション"""
    # </table> 以降の ## セクション
    after_table = text.split("</table>")[-1]
    sections = re.split(r'^## ', after_table, flags=re.MULTILINE)

    sort_order = 0
    for section in sections:
        section = section.strip()
        if not section:
            continue
        lines = section.split('\n', 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        if not body:
            continue

        conn.execute(
            "INSERT INTO external_links (section, body_md, sort_order) VALUES (?, ?, ?)",
            (title, body, sort_order),
        )
        sort_order += 1


def _guess_image_type(url: str) -> str:
    url_lower = url.lower()
    if '.gif' in url_lower:
        return 'gif'
    elif '.png' in url_lower:
        return 'png'
    elif '.jpg' in url_lower or '.jpeg' in url_lower:
        return 'jpeg'
    # GitHub assets URL (拡張子なし) はデフォルト png
    return 'png'


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    text = WORKS_MD.read_text(encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)

    parse_contributions(text, conn)
    parse_repositories(text, conn)
    parse_external_links(text, conn)

    conn.commit()

    # 統計表示
    cat_count = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]
    work_count = conn.execute("SELECT COUNT(*) FROM works").fetchone()[0]
    contrib_count = conn.execute("SELECT COUNT(*) FROM contributions").fetchone()[0]
    link_count = conn.execute("SELECT COUNT(*) FROM external_links").fetchone()[0]

    print(f"Migration complete:")
    print(f"  Categories:    {cat_count}")
    print(f"  Works:         {work_count}")
    print(f"  Contributions: {contrib_count}")
    print(f"  External links:{link_count}")

    conn.close()


if __name__ == "__main__":
    main()
