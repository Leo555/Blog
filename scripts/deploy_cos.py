#!/usr/bin/env python3
"""Deploy Hexo public/ to Tencent Cloud COS using official Python SDK."""
import os
import sys
import traceback
import mimetypes
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from qcloud_cos import CosConfig, CosS3Client

BUCKET = os.environ['COS_BUCKET']
REGION = os.environ['COS_REGION']
PUBLIC_DIR = Path('./public')

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
    bucket = os.environ.get('COS_BUCKET', '').strip()
    region = os.environ.get('COS_REGION', '').strip()

    print(f"[CONFIG] Bucket={bucket} Region={region}")
    print(f"[CONFIG] SecretId={'set(' + secret_id[:6] + '...' + secret_id[-4:] + ')' if len(secret_id) > 10 else 'EMPTY!'}")
    print(f"[CONFIG] SecretKey={'set' if secret_key else 'EMPTY!'}")

    if not secret_id or not secret_key or not bucket or not region:
        print("[FATAL] Missing required environment variables. Check GitHub Secrets.")
        sys.exit(1)

    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
        Token=None,
        Scheme='https',
        Timeout=30,
    )
    client = CosS3Client(config)

    # 1. Delete all existing objects
    print(f"\n[{BUCKET}] Clearing bucket...")
    marker = ""
    total_deleted = 0
    while True:
        try:
            resp = client.list_objects(Bucket=BUCKET, Marker=marker, MaxKeys=1000)
        except Exception as e:
            print(f"[ERROR] list_objects failed: {e}")
            traceback.print_exc()
            sys.exit(1)
        objs = resp.get('Contents', [])
        if objs:
            delete_keys = [{'Key': o['Key']} for o in objs]
            try:
                client.delete_objects(Bucket=BUCKET, Delete={'Object': delete_keys})
                total_deleted += len(objs)
                print(f"  Deleted {len(objs)} objects (total: {total_deleted})")
            except Exception as e:
                print(f"[WARN] delete_objects failed: {e}")
        if not resp.get('IsTruncated'):
            break
        marker = resp.get('NextMarker', '')
    print(f"[{BUCKET}] Cleared {total_deleted} objects.")

    # 2. Upload all files from public/
    print(f"\n[{BUCKET}] Uploading {PUBLIC_DIR}...")
    if not PUBLIC_DIR.exists():
        print(f"[ERROR] {PUBLIC_DIR} does not exist! Hexo build may have failed.")
        sys.exit(1)

    files = sorted(f for f in PUBLIC_DIR.rglob('*') if f.is_file())
    total = len(files)
    print(f"[INFO] Found {total} files to upload.")

    uploaded = 0
    failed = 0
    lock = threading.Lock()

    def upload_one(f: Path) -> bool:
        nonlocal uploaded, failed
        cos_key = str(f.relative_to(PUBLIC_DIR))
        extra = {'ContentType': get_content_type(f)}
        try:
            with open(f, 'rb') as fp:
                client.put_object(Bucket=BUCKET, Body=fp, Key=cos_key, **extra)
            with lock:
                uploaded += 1
                if uploaded % 50 == 0 or uploaded == total:
                    print(f"  Uploaded {uploaded}/{total}...")
            return True
        except Exception as e:
            with lock:
                failed += 1
            print(f"[ERROR] Failed to upload {cos_key}: {e}")
            return False

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(upload_one, f): f for f in files}
        for future in as_completed(futures):
            future.result()

    print(f"\n[{BUCKET}] Done! Total {uploaded}/{total} files uploaded, {failed} failed.")
    if failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] {e}")
        traceback.print_exc()
        sys.exit(1)
