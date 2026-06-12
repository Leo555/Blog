#!/usr/bin/env python3
"""Deploy Hexo public/ to Tencent Cloud COS using official Python SDK."""
import os
import sys
import time
import logging
import traceback
import mimetypes
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from qcloud_cos import CosConfig, CosS3Client

# 降低 SDK 自身日志噪音，但保留 WARNING 以上
logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

BUCKET = os.environ.get('COS_BUCKET', '').strip()
REGION = os.environ.get('COS_REGION', '').strip()
PUBLIC_DIR = Path('./public')


def log(msg: str):
    print(msg, flush=True)


def get_content_type(f: Path) -> str:
    ct, _ = mimetypes.guess_type(str(f))
    if ct:
        return ct
    ext = f.suffix.lower()
    return {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.svg': 'image/svg+xml',
        '.woff2': 'font/woff2',
        '.woff': 'font/woff',
        '.ttf': 'font/ttf',
        '.eot': 'application/vnd.ms-fontobject',
    }.get(ext, 'application/octet-stream')


def main():
    secret_id = os.environ.get('COS_SECRET_ID', '').strip()
    secret_key = os.environ.get('COS_SECRET_KEY', '').strip()

    log(f"[CONFIG] Bucket={BUCKET} Region={REGION}")
    log(f"[CONFIG] SecretId={'set(' + secret_id[:6] + '...' + secret_id[-4:] + ')' if len(secret_id) > 10 else 'EMPTY!'}")
    log(f"[CONFIG] SecretKey={'set' if secret_key else 'EMPTY!'}")

    if not secret_id or not secret_key or not BUCKET or not REGION:
        log("[FATAL] Missing required environment variables. Check GitHub Secrets.")
        sys.exit(1)

    # Timeout=10 避免单个请求卡死几分钟（Retry 参数部分 SDK 版本不支持，故不传）
    config = CosConfig(
        Region=REGION,
        SecretId=secret_id,
        SecretKey=secret_key,
        Token=None,
        Scheme='https',
        Timeout=10,
    )
    client = CosS3Client(config)

    # 0. connectivity check
    log("\n[CHECK] Verifying bucket access...")
    try:
        client.head_bucket(Bucket=BUCKET)
        log("[CHECK] Bucket OK.")
    except Exception as e:
        log(f"[FATAL] Cannot access bucket: {e}")
        traceback.print_exc()
        sys.exit(1)

    # 1. Delete all existing objects
    log(f"\n[{BUCKET}] Clearing bucket...")
    marker = ""
    total_deleted = 0
    while True:
        try:
            resp = client.list_objects(Bucket=BUCKET, Marker=marker, MaxKeys=1000)
        except Exception as e:
            log(f"[ERROR] list_objects failed: {e}")
            traceback.print_exc()
            sys.exit(1)
        objs = resp.get('Contents', [])
        if objs:
            delete_keys = [{'Key': o['Key']} for o in objs]
            try:
                client.delete_objects(Bucket=BUCKET, Delete={'Object': delete_keys})
                total_deleted += len(objs)
                log(f"  Deleted {len(objs)} objects (total: {total_deleted})")
            except Exception as e:
                log(f"[WARN] delete_objects failed: {e}")
        if not resp.get('IsTruncated'):
            break
        marker = resp.get('NextMarker', '')
    log(f"[{BUCKET}] Cleared {total_deleted} objects.")

    # 2. Upload all files from public/
    log(f"\n[{BUCKET}] Uploading {PUBLIC_DIR}...")
    if not PUBLIC_DIR.exists():
        log(f"[ERROR] {PUBLIC_DIR} does not exist! Hexo build may have failed.")
        sys.exit(1)

    files = sorted(f for f in PUBLIC_DIR.rglob('*') if f.is_file())
    total = len(files)
    log(f"[INFO] Found {total} files to upload.")

    uploaded = 0
    failed = 0
    failed_keys = []
    lock = threading.Lock()
    start = time.time()

    def upload_one(f: Path):
        nonlocal uploaded, failed
        cos_key = str(f.relative_to(PUBLIC_DIR))
        ctype = get_content_type(f)
        try:
            data = f.read_bytes()
            client.put_object(Bucket=BUCKET, Body=data, Key=cos_key, ContentType=ctype)
            with lock:
                uploaded += 1
                if uploaded % 25 == 0 or uploaded == total:
                    log(f"  Uploaded {uploaded}/{total} ({time.time()-start:.0f}s)...")
        except Exception as e:
            with lock:
                failed += 1
                failed_keys.append(cos_key)
            log(f"[ERROR] Failed to upload {cos_key}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(upload_one, f) for f in files]
        for future in as_completed(futures):
            future.result()

    log(f"\n[{BUCKET}] Done! {uploaded}/{total} uploaded, {failed} failed, took {time.time()-start:.0f}s.")
    if failed_keys:
        log(f"[ERROR] Failed files: {failed_keys[:20]}")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f"[FATAL] {e}")
        traceback.print_exc()
        sys.exit(1)
