"""works.db のエントリを追加・編集するCLI

使用例 (追加):
  python add_work.py -c ObjectDetection -r Kazuhito00/New-Repo \
    -d "説明文" -i "https://example.com/image.gif"

  python add_work.py -c ObjectDetection -r Kazuhito00/New-Repo \
    -d "説明文" -i ./local_thumb.gif

使用例 (編集):
  python add_work.py --edit --id 42 -d "新しい説明"
  python add_work.py --edit -r mediapipe-python-sample -i "https://new-image.gif"
  python add_work.py --edit -r mediapipe -c NewCategory  # カテゴリ移動

使用例 (一覧):
  python add_work.py --list-categories
"""

import argparse
import sqlite3
import sys
import urllib.request
from pathlib import Path

DB_PATH = Path(__file__).parent / "works.db"


def list_categories(conn: sqlite3.Connection):
    rows = conn.execute(
        "SELECT name, display_name, (SELECT COUNT(*) FROM works w WHERE w.category_id = c.id) "
        "FROM categories c ORDER BY sort_order"
    ).fetchall()
    print(f"{'Name':<30s} {'Display Name':<40s} {'Count':>5s}")
    print("-" * 77)
    for name, display, count in rows:
        print(f"{name:<30s} {display:<40s} {count:>5d}")


def load_image(source: str) -> tuple:
    """画像を読み込んで (data, image_type) を返す。URL またはローカルパス対応"""
    path = Path(source)
    if path.exists():
        data = path.read_bytes()
        return data, _guess_type_from_path(path.suffix)
    else:
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type", "")

        if "gif" in content_type:
            return data, "gif"
        elif "png" in content_type:
            return data, "png"
        elif "jpeg" in content_type or "jpg" in content_type:
            return data, "jpeg"
        elif "webp" in content_type:
            return data, "webp"
        return data, _guess_type_from_path(Path(source).suffix)


def _guess_type_from_path(suffix: str) -> str:
    return {
        ".gif": "gif",
        ".png": "png",
        ".jpg": "jpeg",
        ".jpeg": "jpeg",
        ".webp": "webp",
    }.get(suffix.lower(), "png")


def find_work(conn: sqlite3.Connection, args) -> dict:
    """--id または --repo でエントリを特定して返す"""
    if args.id:
        row = conn.execute(
            "SELECT w.id, w.repo_name, w.repo_url, w.description, w.image_url, c.name "
            "FROM works w JOIN categories c ON w.category_id = c.id WHERE w.id = ?",
            (args.id,),
        ).fetchone()
        if not row:
            print(f"Error: id={args.id} not found.", file=sys.stderr)
            sys.exit(1)
        return {"id": row[0], "repo_name": row[1], "repo_url": row[2],
                "description": row[3], "image_url": row[4], "category": row[5]}

    if args.repo:
        search = args.repo.split("/")[-1]  # Kazuhito00/Repo → Repo
        rows = conn.execute(
            "SELECT w.id, w.repo_name, w.repo_url, w.description, w.image_url, c.name "
            "FROM works w JOIN categories c ON w.category_id = c.id "
            "WHERE w.repo_name LIKE ? ORDER BY w.id",
            (f"%{search}%",),
        ).fetchall()

        if not rows:
            print(f"Error: no entry matching '{search}'.", file=sys.stderr)
            sys.exit(1)

        if len(rows) == 1:
            r = rows[0]
            return {"id": r[0], "repo_name": r[1], "repo_url": r[2],
                    "description": r[3], "image_url": r[4], "category": r[5]}

        # 複数候補
        print(f"Multiple entries found for '{search}':")
        for r in rows:
            print(f"  id={r[0]:>4d}  [{r[5]}] {r[1]}")
        print("\nUse --id to specify.", file=sys.stderr)
        sys.exit(1)

    print("Error: --id or --repo is required for --edit.", file=sys.stderr)
    sys.exit(1)


def edit_work(conn: sqlite3.Connection, args):
    """既存エントリを編集"""
    work = find_work(conn, args)
    work_id = work["id"]

    print(f"Editing id={work_id}: {work['repo_name']} [{work['category']}]")

    updates = []
    params = []

    if args.description is not None:
        updates.append("description = ?")
        params.append(args.description)
        print(f"  description: {work['description']!r} -> {args.description!r}")

    if args.image is not None:
        try:
            is_local = Path(args.image).exists()
            label = "Reading" if is_local else "Downloading"
            print(f"  {label} image: {args.image}")
            image_data, image_type = load_image(args.image)
            print(f"    {len(image_data)} bytes, type={image_type}")
            updates.append("image_data = ?")
            params.append(image_data)
            updates.append("image_type = ?")
            params.append(image_type)
            if is_local:
                updates.append("image_url = NULL")
            else:
                updates.append("image_url = ?")
                params.append(args.image)
        except Exception as e:
            print(f"  Warning: failed to load image: {e}", file=sys.stderr)

    if args.category:
        cat_row = conn.execute(
            "SELECT id FROM categories WHERE name = ?", (args.category,)
        ).fetchone()
        if not cat_row:
            print(f"Error: category '{args.category}' not found.", file=sys.stderr)
            sys.exit(1)
        updates.append("category_id = ?")
        params.append(cat_row[0])
        print(f"  category: {work['category']} -> {args.category}")

    if not updates:
        print("Nothing to update. Specify -d, -i, or -c.")
        return

    params.append(work_id)
    sql = f"UPDATE works SET {', '.join(updates)} WHERE id = ?"
    conn.execute(sql, params)
    conn.commit()
    print("Updated.")


def add_work(conn: sqlite3.Connection, args):
    """新規エントリを追加"""
    row = conn.execute(
        "SELECT id FROM categories WHERE name = ?", (args.category,)
    ).fetchone()

    if not row:
        print(f"Error: category '{args.category}' not found.", file=sys.stderr)
        print("Use --list-categories to see available categories.", file=sys.stderr)
        sys.exit(1)

    cat_id = row[0]

    if args.append:
        max_order = conn.execute(
            "SELECT COALESCE(MAX(sort_order), -1) FROM works WHERE category_id = ?",
            (cat_id,),
        ).fetchone()[0]
        sort_order = max_order + 1
    else:
        conn.execute(
            "UPDATE works SET sort_order = sort_order + 1 WHERE category_id = ?",
            (cat_id,),
        )
        sort_order = 0

    image_data = None
    image_type = None
    image_url = args.image
    if args.image:
        try:
            is_local = Path(args.image).exists()
            label = "Reading" if is_local else "Downloading"
            print(f"{label} image: {args.image}")
            image_data, image_type = load_image(args.image)
            print(f"  {len(image_data)} bytes, type={image_type}")
            if is_local:
                image_url = None
        except Exception as e:
            print(f"  Warning: failed to load image: {e}", file=sys.stderr)

    repo_url = f"https://github.com/{args.repo}" if args.repo and not args.repo.startswith("http") else args.repo

    conn.execute(
        "INSERT INTO works (category_id, repo_name, repo_url, description, image_url, image_data, image_type, sort_order) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            cat_id,
            args.repo.split("/")[-1] if args.repo else None,
            repo_url,
            args.description,
            image_url,
            image_data,
            image_type,
            sort_order,
        ),
    )
    conn.commit()

    work_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"Added work id={work_id} to category '{args.category}' (sort_order={sort_order})")


def main():
    parser = argparse.ArgumentParser(description="Add or edit work entries in works.db")
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--edit", action="store_true", help="Edit an existing entry")
    parser.add_argument("--id", type=int, help="Work ID (for --edit)")
    parser.add_argument("--category", "-c", help="Category name")
    parser.add_argument("--repo", "-r", help="Repository (e.g. Kazuhito00/RepoName or RepoName)")
    parser.add_argument("--description", "-d", help="Description text")
    parser.add_argument("--image", "-i", help="Image source (URL or local file path)")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to end of category (default: prepend to top)",
    )
    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"Error: {DB_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    if args.list_categories:
        list_categories(conn)
        conn.close()
        return

    if args.edit:
        edit_work(conn, args)
        conn.close()
        return

    if not args.category or not args.repo:
        parser.error("--category and --repo are required (or use --edit / --list-categories)")

    add_work(conn, args)
    conn.close()


if __name__ == "__main__":
    main()
