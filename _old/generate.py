"""works.db から WORKS.md を生成するスクリプト

--download-images: image_url から画像をダウンロードして image_data (BLOB) に格納
"""

import argparse
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

DB_PATH = Path(__file__).parent / "works.db"
WORKS_MD = Path(__file__).parent / "WORKS.md"


def download_images(conn: sqlite3.Connection):
    """image_data が NULL のエントリについて image_url から画像をダウンロード"""
    tables = ["works", "contributions"]
    for table in tables:
        rows = conn.execute(
            f"SELECT id, image_url FROM {table} WHERE image_url IS NOT NULL AND image_data IS NULL"
        ).fetchall()

        if not rows:
            print(f"  {table}: no images to download")
            continue

        print(f"  {table}: downloading {len(rows)} images...")
        success = 0
        fail = 0
        for row_id, url in rows:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                    content_type = resp.headers.get("Content-Type", "")

                # Content-Type から image_type を判定
                if "gif" in content_type:
                    img_type = "gif"
                elif "png" in content_type:
                    img_type = "png"
                elif "jpeg" in content_type or "jpg" in content_type:
                    img_type = "jpeg"
                elif "webp" in content_type:
                    img_type = "webp"
                else:
                    img_type = _guess_type_from_url(url)

                conn.execute(
                    f"UPDATE {table} SET image_data = ?, image_type = ? WHERE id = ?",
                    (data, img_type, row_id),
                )
                success += 1
                # Rate limiting
                time.sleep(0.2)
            except Exception as e:
                print(f"    FAIL [{row_id}] {url}: {e}")
                fail += 1

        conn.commit()
        print(f"    done: {success} ok, {fail} failed")


def _guess_type_from_url(url: str) -> str:
    url_lower = url.lower()
    if ".gif" in url_lower:
        return "gif"
    elif ".png" in url_lower:
        return "png"
    elif ".jpg" in url_lower or ".jpeg" in url_lower:
        return "jpeg"
    return "png"


def generate_works_md(conn: sqlite3.Connection):
    """works.db から WORKS.md を生成"""
    lines = []
    lines.append(
        "<!-- https://developers.google.com/speed/pagespeed/insights/?hl=JA&url=https%3A%2F%2Fgithub.com%2FKazuhito00%2FKazuhito00%2Fblob%2Fmaster%2FWORKS.md -->"
    )
    lines.append("")
    lines.append("# WORKS")
    lines.append("提供物、寄稿、公開リポジトリの内容をまとめています。")
    lines.append("")

    # Contribution セクション
    lines.append("## Contribution")
    lines.append("提供した情報等をまとめています。")
    lines.append("")

    sections = conn.execute(
        "SELECT DISTINCT section FROM contributions ORDER BY sort_order"
    ).fetchall()

    for (section,) in sections:
        is_first = section == sections[0][0]
        if is_first:
            lines.append(f'<details  open>')
        else:
            lines.append(f'<details>')
        lines.append(f'<summary>{section}</summary>')
        lines.append("")
        lines.append("<table>")

        contribs = conn.execute(
            "SELECT description_html, image_url, image_link FROM contributions "
            "WHERE section = ? ORDER BY sort_order",
            (section,),
        ).fetchall()

        for desc_html, image_url, image_link in contribs:
            lines.append("    <tr>")
            lines.append('        <td width="220">')
            if image_link:
                lines.append(
                    f'            <a href="{image_link}"><img src="{image_url}" loading="lazy" width="200px"></a>'
                )
            elif image_url:
                lines.append(
                    f'            <img src="{image_url}" loading="lazy" width="200px">'
                )
            lines.append("        </td>")
            lines.append("        <td>")
            lines.append(f"            {desc_html}")
            lines.append("        </td>")
            lines.append("    </tr>")

        lines.append("</table>")
        lines.append("</details>")
        lines.append("")

    # Repositories セクション
    lines.append('## <a name="#Repositories">Repositories</a>')
    lines.append("リポジトリ数が増えてきたためカテゴリー分けしてまとめています。")
    lines.append("")

    categories = conn.execute(
        "SELECT id, name, display_name FROM categories ORDER BY sort_order"
    ).fetchall()

    # 目次
    for cat_id, name, display in categories:
        lines.append(f'* <a href="#{name}">{display}</a>')
    lines.append("")

    # テーブル
    lines.append("<table>")
    for cat_id, name, display in categories:
        lines.append("    <tr>")
        lines.append(f'        <th align="left" colspan="2">')
        lines.append(
            f'            <a name="{name}">{display}</a>　<a href="#Repositories">🔙</a>'
        )
        lines.append("        </th>")
        lines.append("    </tr>")

        works = conn.execute(
            "SELECT repo_name, repo_url, description, image_url FROM works "
            "WHERE category_id = ? ORDER BY sort_order",
            (cat_id,),
        ).fetchall()

        for repo_name, repo_url, desc, image_url in works:
            lines.append("    <tr>")
            lines.append('        <td width="220">')
            if image_url:
                lines.append(
                    f'            <img src="{image_url}" loading="lazy" width="200px">'
                )
            lines.append("        </td>")
            lines.append("        <td>")
            if repo_url and repo_name:
                lines.append(
                    f'            <a href="{repo_url}">[{repo_name}]</a><br>'
                )
            if desc:
                # 改行を <br> に戻す
                desc_html = desc.replace("\n", "<br>")
                lines.append(f"            {desc_html}<br>")
            lines.append("        </td>")
            lines.append("    </tr>")

    lines.append("</table>")
    lines.append("")

    # External links
    ext_links = conn.execute(
        "SELECT section, body_md FROM external_links ORDER BY sort_order"
    ).fetchall()
    for section, body in ext_links:
        lines.append(f"## {section}")
        lines.append(body)
        lines.append("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate WORKS.md and docs/works.db from works.db")
    parser.add_argument(
        "--download-images",
        action="store_true",
        help="Download images from image_url and store as BLOB in DB",
    )
    parser.add_argument(
        "--skip-md",
        action="store_true",
        help="Skip WORKS.md generation",
    )
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Error: {DB_PATH} not found. Run migrate.py first.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    if args.download_images:
        print("Downloading images...")
        download_images(conn)

    if not args.skip_md:
        print("Generating WORKS.md...")
        md = generate_works_md(conn)
        WORKS_MD.write_text(md, encoding="utf-8")
        print(f"  WORKS.md: {len(md)} bytes")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
