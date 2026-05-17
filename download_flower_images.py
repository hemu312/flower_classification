"""
India Flowers Image Downloader & Resizer
========================================
Downloads 1000 images per flower (100 flowers = 100,000 images total)
Resizes all to 512x512 (standard for ML/CNN training)

Requirements:
    pip install requests Pillow icrawler pandas

Usage:
    python download_flower_images.py

    # Download only specific flowers (by row index 0-99):
    python download_flower_images.py --start 0 --end 9

    # Resume interrupted download:
    python download_flower_images.py --resume

Output structure:
    flower_dataset/
    ├── lotus/
    │   ├── 0001.jpg
    │   ├── 0002.jpg
    │   └── ...
    ├── marigold/
    │   └── ...
    └── ...
"""

import json
import argparse
import time
import hashlib
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image
from icrawler.builtin import BingImageCrawler


# Custom crawler that handles None parse results gracefully
class SafeBingImageCrawler(BingImageCrawler):
    def parse(self, response, **kwargs):
        result = super().parse(response, **kwargs)
        return result if result is not None else []

# ── CONFIG ─────────────────────────────────────────────────────────────────────
IMAGES_PER_FLOWER = 1000
TARGET_SIZE = (512, 512)
OUTPUT_DIR = Path("flower_dataset")
JSON_FILE = Path("india_garden_flowers.json")   # same directory as this script
MAX_WORKERS = 4                                  # parallel download threads
SOURCES = ["bing"]                              # crawl from Bing only
# ───────────────────────────────────────────────────────────────────────────────


def load_flowers(json_path: Path) -> list[dict]:
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def safe_folder_name(name: str) -> str:
    """Convert flower common name to safe folder name."""
    return name.lower().strip().replace(" ", "_").replace("/", "_").replace("'", "")


def build_search_query(flower: dict) -> str:
    """Build a rich query to get diverse, high-quality results."""
    return (
        f"{flower['common_name']} {flower['scientific_name']} flower high quality image"
    )


def download_for_flower(flower: dict, target_dir: Path, resume: bool) -> int:
    """Download images from Bing for a single flower."""
    target_dir.mkdir(parents=True, exist_ok=True)
    query = build_search_query(flower)

    existing = len(list(target_dir.glob("*.jpg"))) + len(list(target_dir.glob("*.png")))
    if resume and existing >= IMAGES_PER_FLOWER:
        return existing  # already done

    sub_dir = target_dir / "_tmp_bing"
    sub_dir.mkdir(exist_ok=True)
    try:
        crawler = SafeBingImageCrawler(
            storage={"root_dir": str(sub_dir)},
            log_level=50,
        )
        crawler.crawl(
            keyword=query,
            max_num=IMAGES_PER_FLOWER,
            min_size=(100, 100),
            file_idx_offset=0,
        )
    except Exception as e:
        print(f"  ⚠  Bing crawl failed for {flower['common_name']}: {e}")

    return merge_and_resize(target_dir)


def merge_and_resize(flower_dir: Path) -> int:
    """
    Collect all downloaded images from _tmp_* folders,
    deduplicate by hash, resize to 512x512
    Returns number of usable images.
    """
    seen_hashes = set()
    out_index = 1
    raw_images: list[Path] = []

    for tmp_dir in flower_dir.glob("_tmp_*"):
        raw_images.extend(tmp_dir.glob("*"))

    for src in raw_images:
        if out_index > IMAGES_PER_FLOWER:
            break
        try:
            with Image.open(src) as img:
                # Dedup
                img_bytes = img.tobytes()
                h = hashlib.md5(img_bytes).hexdigest()
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                # Resize with high-quality Lanczos
                img_resized = img.convert("RGB").resize(TARGET_SIZE, Image.LANCZOS)
                out_path = flower_dir / f"{out_index:04d}.jpg"
                img_resized.save(out_path, "JPEG", quality=90)
                out_index += 1
        except Exception:
            pass  # skip corrupt files

    # Clean up temp dirs
    for tmp_dir in flower_dir.glob("_tmp_*"):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return out_index - 1


def main():
    parser = argparse.ArgumentParser(description="Download & resize India flower images")
    parser.add_argument("--start", type=int, default=0, help="Start flower index (0-99)")
    parser.add_argument("--end", type=int, default=99, help="End flower index (0-99)")
    parser.add_argument("--resume", action="store_true", help="Skip flowers already downloaded")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help="Parallel downloads")
    args = parser.parse_args()

    if not JSON_FILE.exists():
        print(f"❌ JSON not found: {JSON_FILE}")
        print("   Place india_garden_flowers.json in the same directory as this script.")
        return

    flowers = load_flowers(JSON_FILE)
    selected = flowers[args.start : args.end + 1]

    print(f"\n🌸 India Flower Image Downloader")
    print(f"   Flowers  : {len(selected)} ({args.start}–{args.end})")
    print(f"   Per flower: {IMAGES_PER_FLOWER} images")
    print(f"   Total    : ~{len(selected) * IMAGES_PER_FLOWER:,} images")
    print(f"   Size     : {TARGET_SIZE[0]}×{TARGET_SIZE[1]} px")
    print(f"   Output   : {OUTPUT_DIR.resolve()}\n")

    results = {}

    def process(flower):
        name = flower["id"]
        folder = safe_folder_name(name)
        target_dir = OUTPUT_DIR / folder
        count = download_for_flower(flower, target_dir, args.resume)
        return name, count

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(process, f): f["common_name"] for f in selected}
        total_flowers = len(futures)
        completed = 0
        last_update = time.time()
        start_time = time.time()
        
        for future in as_completed(futures):
            name, count = future.result()
            results[name] = count
            completed += 1
            
            now = time.time()
            elapsed = now - start_time
            if now - last_update >= 10 or completed == total_flowers:
                progress_pct = (completed / total_flowers) * 100
                print(f"  ⏱ {completed}/{total_flowers} flowers ({progress_pct:.1f}%) - elapsed: {elapsed:.0f}s")
                last_update = now

    # Summary
    print("\n✅ Download complete!\n")
    print(f"{'Flower':<35} {'Images':>8}")
    print("─" * 45)
    total = 0
    for name, count in results.items():
        status = "✓" if count >= IMAGES_PER_FLOWER * 0.8 else "⚠"
        print(f"{status} {name:<33} {count:>8,}")
        total += count
    print("─" * 45)
    print(f"{'TOTAL':<35} {total:>8,}\n")

    # Write manifest
    import csv
    manifest_path = OUTPUT_DIR / "manifest.csv"
    with open(manifest_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["folder", "common_name", "scientific_name", "image_count"])
        for flower in selected:
            name = flower["common_name"]
            folder = safe_folder_name(name)
            writer.writerow([folder, name, flower["scientific_name"], results.get(name, 0)])
    print(f"📋 Manifest saved: {manifest_path}")


if __name__ == "__main__":
    main()
