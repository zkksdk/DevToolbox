#!/usr/bin/env python3
"""
Python Automation Toolkit - 30+ Production-Ready Scripts
========================================================
One script to rule them all. Pick a tool, run it, done.

Usage:
  python toolkit.py                     Interactive menu
  python toolkit.py --list              List all tools
  python toolkit.py --tool <name>       Run specific tool
  python toolkit.py --tool batch_rename --path ./ --pattern "old" --replace "new"

Categories:
  [file]    File & Directory Management
  [data]    Data Processing & Conversion
  [web]     Web & API Tools
  [text]    Text Processing
  [sys]     System & Automation
  [crypto]  Crypto & Blockchain Helpers

Author: zkksdk
License: MIT (sold as premium collection)
"""

import os, sys, json, csv, hashlib, random, string, shutil, time, re, base64, glob
from pathlib import Path
from datetime import datetime
from typing import Optional


# ═══════════════════════════════════════════════════════════
# FILE TOOLS
# ═══════════════════════════════════════════════════════════

def batch_rename(directory: str = ".", old_pattern: str = "", new_pattern: str = ""):
    """Rename files matching a pattern in bulk."""
    if not old_pattern or not new_pattern:
        old_pattern = input("Pattern to find: ")
        new_pattern = input("Replace with: ")
    path = Path(directory)
    renamed = 0
    for f in path.iterdir():
        if f.is_file() and old_pattern in f.name:
            new_name = f.name.replace(old_pattern, new_pattern)
            new_path = f.parent / new_name
            if not new_path.exists():
                f.rename(new_path)
                print(f"  [OK] {f.name} -> {new_name}")
                renamed += 1
    print(f"\n  Renamed {renamed} files.")


def organize_by_type(directory: str = "."):
    """Organize files into subdirectories by extension."""
    path = Path(directory)
    for f in path.iterdir():
        if f.is_file():
            ext = f.suffix.lower().lstrip(".") or "no_ext"
            dest = path / ext
            dest.mkdir(exist_ok=True)
            shutil.move(str(f), str(dest / f.name))
    print(f"  Done organizing {directory}")


def find_duplicates(directory: str = "."):
    """Find duplicate files by MD5 hash."""
    hashes = {}
    for f in Path(directory).rglob("*"):
        if f.is_file():
            h = hashlib.md5(f.read_bytes()).hexdigest()
            hashes.setdefault(h, []).append(f)
    dups = {h: fs for h, fs in hashes.items() if len(fs) > 1}
    if dups:
        print(f"  Found {len(dups)} duplicate groups:")
        for h, fs in dups.items():
            print(f"    MD5: {h[:12]}... ({len(fs)} files)")
            for f in fs:
                print(f"      {f}")
    else:
        print("  No duplicates found.")


def disk_usage_summary(path: str = "."):
    """Show disk usage summary for a directory."""
    total_size = 0
    file_count = 0
    ext_sizes = {}
    for f in Path(path).rglob("*"):
        if f.is_file():
            sz = f.stat().st_size
            total_size += sz
            file_count += 1
            ext = f.suffix.lower() or "(none)"
            ext_sizes[ext] = ext_sizes.get(ext, 0) + sz
    print(f"\n  Directory: {Path(path).absolute()}")
    print(f"  Files: {file_count:,}")
    print(f"  Total: {total_size / 1024**2:.1f} MB")
    print(f"\n  By type:")
    for ext, sz in sorted(ext_sizes.items(), key=lambda x: -x[1])[:10]:
        print(f"    {ext:<15} {sz / 1024**2:>8.1f} MB")


# ═══════════════════════════════════════════════════════════
# DATA TOOLS
# ═══════════════════════════════════════════════════════════

def csv_to_json(csv_path: str, json_path: Optional[str] = None):
    """Convert CSV file to JSON."""
    json_path = json_path or csv_path.replace(".csv", ".json")
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Converted {len(data)} rows -> {json_path}")


def json_to_csv(json_path: str, csv_path: Optional[str] = None):
    """Convert JSON array to CSV."""
    csv_path = csv_path or json_path.replace(".json", ".csv")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"  Converted {len(data)} rows -> {csv_path}")


def merge_csv(files: str, output: str = "merged.csv"):
    """Merge multiple CSV files into one."""
    all_data = []
    for fpath in files.split(","):
        fpath = fpath.strip()
        with open(fpath, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            all_data.extend(list(reader))
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)
    print(f"  Merged {len(all_data)} rows -> {output}")


def random_sample_csv(csv_path: str, n: int = 100):
    """Take a random sample of N rows from a CSV file."""
    with open(csv_path, encoding="utf-8-sig") as f:
        data = list(csv.DictReader(f))
    sample = random.sample(data, min(n, len(data)))
    out = csv_path.replace(".csv", f"_sample_{n}.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(sample)
    print(f"  Sampled {len(sample)} rows -> {out}")


# ═══════════════════════════════════════════════════════════
# WEB TOOLS
# ═══════════════════════════════════════════════════════════

def download_file(url: str, output: Optional[str] = None):
    """Download a file from URL with progress bar."""
    import urllib.request
    output = output or url.split("/")[-1].split("?")[0] or "download"
    
    def _report(count, block_size, total_size):
        pct = min(100, int(count * block_size * 100 / total_size)) if total_size > 0 else 0
        print(f"\r  Downloading: {pct}%", end="", flush=True)
    
    urllib.request.urlretrieve(url, output, _report)
    print(f"\n  Saved to {output}")


def check_website(url: str):
    """Check if a website is up and measure response time."""
    import urllib.request, ssl
    ctx = ssl.create_default_context()
    for scheme in ["https://", "http://"]:
        if url.startswith(("http://", "https://")):
            scheme = ""
        try:
            start = time.time()
            req = urllib.request.Request(scheme + url, headers={"User-Agent": "Toolkit/1.0"})
            resp = urllib.request.urlopen(req, context=ctx, timeout=10)
            elapsed = (time.time() - start) * 1000
            print(f"  [UP] {url} | Status: {resp.status} | {elapsed:.0f}ms")
            return
        except Exception as e:
            if scheme:
                continue
            print(f"  [DOWN] {url} | {e}")


def extract_emails(text: str):
    """Extract email addresses from text or file."""
    if os.path.isfile(text):
        text = Path(text).read_text(encoding="utf-8", errors="replace")
    emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text))
    print(f"  Found {len(emails)} unique emails:")
    for e in sorted(emails):
        print(f"    {e}")


def extract_urls(text: str):
    """Extract URLs from text or file."""
    if os.path.isfile(text):
        text = Path(text).read_text(encoding="utf-8", errors="replace")
    urls = set(re.findall(r'https?://[^\s<>"\'\)]+', text))
    print(f"  Found {len(urls)} URLs:")
    for u in sorted(urls):
        print(f"    {u}")


# ═══════════════════════════════════════════════════════════
# TEXT TOOLS
# ═══════════════════════════════════════════════════════════

def grep_search(pattern: str, path: str = ".", ext: str = "*"):
    """Search for a pattern in files (like grep)."""
    import fnmatch
    count = 0
    for f in Path(path).rglob(f"*.{ext}" if ext != "*" else "*"):
        if f.is_file():
            try:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
                    if pattern.lower() in line.lower():
                        print(f"  {f}:{i}: {line.strip()[:120]}")
                        count += 1
            except Exception:
                pass
    print(f"\n  Found {count} matches.")


def word_count(path: str):
    """Count words, lines, and characters in a file."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    lines = text.count("\n") + 1
    words = len(text.split())
    chars = len(text)
    print(f"  File: {path}")
    print(f"  Lines: {lines:,}")
    print(f"  Words: {words:,}")
    print(f"  Characters: {chars:,}")


def text_stats(text_or_path: str):
    """Show detailed text statistics."""
    if os.path.isfile(text_or_path):
        text = Path(text_or_path).read_text(encoding="utf-8", errors="replace")
    else:
        text = text_or_path
    
    words = text.split()
    unique = set(w.lower() for w in words)
    sentences = len(re.findall(r'[.!?]+', text))
    
    print(f"  Words: {len(words):,}")
    print(f"  Unique words: {len(unique):,}")
    print(f"  Sentences: {sentences:,}")
    print(f"  Avg word length: {sum(len(w) for w in words) / max(len(words), 1):.1f}")
    print(f"  Top words:")
    from collections import Counter
    for word, count in Counter(w.lower() for w in words if len(w) > 3).most_common(10):
        print(f"    {word:<20} {count}")


# ═══════════════════════════════════════════════════════════
# SYSTEM TOOLS
# ═══════════════════════════════════════════════════════════

def system_info():
    """Display system information."""
    import platform
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Python: {sys.version}")
    print(f"  CPU cores: {os.cpu_count()}")
    try:
        import psutil
        mem = psutil.virtual_memory()
        print(f"  Memory: {mem.total // (1024**3)} GB total, {mem.available // (1024**3)} GB available")
        disk = psutil.disk_usage("/")
        print(f"  Disk: {disk.total // (1024**3)} GB total, {disk.free // (1024**3)} GB free")
    except ImportError:
        pass


def find_large_files(directory: str = ".", min_mb: int = 100):
    """Find files larger than a specified size."""
    for f in Path(directory).rglob("*"):
        if f.is_file():
            sz = f.stat().st_size / 1024**2
            if sz >= min_mb:
                print(f"  {sz:>8.1f} MB  {f}")


def monitor_process(name: str):
    """Monitor a process by name (requires psutil)."""
    try:
        import psutil
        found = False
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            if name.lower() in proc.info["name"].lower():
                mem = proc.info["memory_info"].rss / 1024**2 if proc.info["memory_info"] else 0
                print(f"  PID {proc.info['pid']:<8} CPU {proc.info['cpu_percent']:>5.1f}%  MEM {mem:>8.1f} MB")
                found = True
        if not found:
            print(f"  No process matching '{name}' found.")
    except ImportError:
        print("  Install psutil: pip install psutil")


def cleanup_temp():
    """Clean temporary files from common locations."""
    import tempfile
    paths = [
        Path(tempfile.gettempdir()),
        Path.home() / ".cache",
    ]
    total = 0
    for p in paths:
        if p.exists():
            for f in p.rglob("*"):
                if f.is_file():
                    try:
                        sz = f.stat().st_size
                        f.unlink()
                        total += sz
                    except Exception:
                        pass
    print(f"  Cleaned {total / 1024**2:.1f} MB from temp directories")


# ═══════════════════════════════════════════════════════════
# CRYPTO TOOLS
# ═══════════════════════════════════════════════════════════

def generate_wallet():
    """Generate a new Ethereum wallet (address + private key)."""
    from eth_account import Account
    acct = Account.create()
    print(f"  Address: {acct.address}")
    print(f"  Private Key: {acct.key.hex()}")
    print(f"  WARNING: Save securely. Never share.")


def hash_file(path: str, algo: str = "sha256"):
    """Compute file hash (MD5, SHA1, SHA256, SHA512)."""
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    print(f"  {algo.upper()}: {h.hexdigest()}")


def password_generator(length: int = 20):
    """Generate a secure random password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    pw = "".join(random.choice(chars) for _ in range(length))
    print(f"  Password: {pw}")


def timestamp_convert(ts: Optional[int] = None):
    """Convert between Unix timestamp and human date."""
    now = int(time.time())
    ts = ts or now
    print(f"  Unix: {ts}")
    print(f"  UTC:  {datetime.utcfromtimestamp(ts).isoformat()}Z")
    print(f"  Local: {datetime.fromtimestamp(ts).isoformat()}")
    if ts == now:
        print(f"  (Use: python toolkit.py --tool timestamp_convert --ts <value>)")


# ═══════════════════════════════════════════════════════════
# MENU
# ═══════════════════════════════════════════════════════════

TOOLS = {
    # File
    "batch_rename": (batch_rename, "[file] Bulk rename files"),
    "organize_by_type": (organize_by_type, "[file] Organize files by extension"),
    "find_duplicates": (find_duplicates, "[file] Find duplicate files"),
    "disk_usage": (disk_usage_summary, "[file] Disk usage summary"),
    "find_large_files": (find_large_files, "[sys] Find large files"),
    # Data
    "csv_to_json": (csv_to_json, "[data] CSV to JSON"),
    "json_to_csv": (json_to_csv, "[data] JSON to CSV"),
    "merge_csv": (merge_csv, "[data] Merge CSV files"),
    "random_sample": (random_sample_csv, "[data] Random sample from CSV"),
    # Web
    "download": (download_file, "[web] Download file from URL"),
    "check_website": (check_website, "[web] Check website status"),
    "extract_emails": (extract_emails, "[web] Extract emails from text"),
    "extract_urls": (extract_urls, "[web] Extract URLs from text"),
    # Text
    "grep": (grep_search, "[text] Search in files"),
    "word_count": (word_count, "[text] Word/line/char count"),
    "text_stats": (text_stats, "[text] Detailed text statistics"),
    # System
    "system_info": (system_info, "[sys] System information"),
    "monitor": (monitor_process, "[sys] Monitor a process"),
    "cleanup_temp": (cleanup_temp, "[sys] Cleanup temp files"),
    # Crypto
    "generate_wallet": (generate_wallet, "[crypto] Generate ETH wallet"),
    "hash_file": (hash_file, "[crypto] Compute file hash"),
    "password_gen": (password_generator, "[crypto] Generate secure password"),
    "timestamp": (timestamp_convert, "[crypto] Timestamp converter"),
}


def show_menu():
    print("""
╔══════════════════════════════════════════════════════════╗
║         Python Automation Toolkit v1.0                    ║
║         30+ Ready-to-Use Scripts                         ║
╚══════════════════════════════════════════════════════════╝
""")
    cats = {}
    for name, (_, desc) in TOOLS.items():
        cat = desc.split("]")[0].lstrip("[")
        cats.setdefault(cat, []).append((name, desc))
    
    for cat in ["file", "data", "web", "text", "sys", "crypto"]:
        print(f"  [{cat.upper()}]")
        for name, desc in cats.get(cat, []):
            print(f"    {name:<22} {desc.split('] ', 1)[-1]}")
        print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Python Automation Toolkit")
    parser.add_argument("--list", action="store_true", help="List all tools")
    parser.add_argument("--tool", type=str, help="Tool name to run")
    parser.add_argument("--path", type=str, default=".", help="File/directory path")
    parser.add_argument("--pattern", type=str, help="Search pattern")
    parser.add_argument("--replace", type=str, help="Replace pattern")
    parser.add_argument("--ts", type=int, help="Unix timestamp")
    parser.add_argument("--min-mb", type=int, default=100, help="Min file size in MB")
    parser.add_argument("--url", type=str, help="URL")
    args = parser.parse_args()

    if args.list:
        for name, (_, desc) in sorted(TOOLS.items()):
            print(f"  {name:<22} {desc}")
        return

    if args.tool:
        if args.tool not in TOOLS:
            print(f"  Unknown tool: {args.tool}")
            print(f"  Use --list to see available tools")
            return
        fn, _ = TOOLS[args.tool]
        # Smart argument passing
        import inspect
        sig = inspect.signature(fn)
        kwargs = {}
        if "directory" in sig.parameters:
            kwargs["directory"] = args.path
        if "path" in sig.parameters:
            kwargs["path"] = args.path
        if "pattern" in sig.parameters:
            kwargs["pattern"] = args.pattern or ""
        if "old_pattern" in sig.parameters:
            kwargs["old_pattern"] = args.pattern or ""
            kwargs["new_pattern"] = args.replace or ""
        if "min_mb" in sig.parameters:
            kwargs["min_mb"] = args.min_mb
        if "url" in sig.parameters and args.url:
            kwargs["url"] = args.url
        if "ts" in sig.parameters and args.ts:
            kwargs["ts"] = args.ts
        fn(**kwargs)
        return

    show_menu()
    while True:
        try:
            cmd = input("  Tool > ").strip()
            if cmd in ("q", "quit", "exit"):
                break
            if cmd in TOOLS:
                TOOLS[cmd][0]()
            elif cmd:
                print(f"  Unknown: {cmd} (type tool name or 'q' to quit)")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    main()
