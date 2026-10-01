"""Import the exact NIST archives recorded in the checksum manifest."""
import argparse
import asyncio
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.request

DATA = Path(__file__).resolve().parents[1] / "NIST_PV_2015_2018"


def digest(path, algorithm):
    result = hashlib.new(algorithm)
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            result.update(block)
    return result.hexdigest()


def valid(path, record):
    return (path.is_file() and path.stat().st_size == record["size"]
            and digest(path, "sha256") == record["sha256"])


async def public_download_token():
    import websockets
    async with websockets.connect(
        "wss://pvdata.nist.gov/socket.io/?EIO=4&transport=websocket",
        open_timeout=45,
    ) as socket:
        await socket.recv()
        await socket.send("40")
        requested = False
        while True:
            message = await asyncio.wait_for(socket.recv(), 60)
            if message == "2":
                await socket.send("3")
            elif message.startswith("40") and not requested:
                await socket.send('42["get box token",{}]')
                requested = True
            elif message.startswith("42"):
                name, payload = json.loads(message[2:])
                if name == "box token":
                    return payload["access_token"]


def import_archive(record, token):
    path = DATA / record["relative_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if valid(path, record):
        print("Already verified:", path.name, flush=True)
        return
    for attempt in range(3):
        try:
            request = urllib.request.Request(
                f"https://api.box.com/2.0/files/{record['id']}?fields=name,size,sha1,download_url",
                headers={"Authorization": "Bearer " + token},
            )
            with urllib.request.urlopen(request, timeout=90) as response:
                metadata = json.load(response)
            if any(metadata[key] != record[key] for key in ("name", "size", "sha1")):
                raise ValueError("Publisher metadata changed: " + path.name)
            partial = path.with_suffix(path.suffix + ".partial")
            with urllib.request.urlopen(metadata["download_url"], timeout=180) as response, partial.open("wb") as target:
                while block := response.read(1024 * 1024):
                    target.write(block)
            if not valid(partial, record) or digest(partial, "sha1") != record["sha1"]:
                raise ValueError("Checksum mismatch: " + path.name)
            partial.replace(path)
            print("Verified:", path.name, record["size"], "bytes", flush=True)
            return
        except Exception as error:
            # Do not log temporary access tokens or signed download URLs.
            print("Attempt failed:", path.name, type(error).__name__, flush=True)
            if attempt == 2:
                raise RuntimeError("Could not import " + path.name) from None
            time.sleep(3 * (attempt + 1))


def import_document(record):
    path = DATA / record["relative_path"]
    if valid(path, record):
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".partial")
    subprocess.run([
        "curl", "--fail", "--silent", "--show-error", "--location",
        "--retry", "3", "--max-time", "120", record["url"], "--output", str(partial),
    ], check=True)
    if not valid(partial, record):
        raise ValueError("Documentation checksum mismatch: " + path.name)
    partial.replace(path)
    print("Verified documentation:", path.name, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    records = json.loads((DATA / "download_manifest.json").read_text())
    documents = json.loads((DATA / "documentation_manifest.json").read_text())
    if len(records) != 20:
        raise ValueError("Expected exactly 20 data archives")
    if not args.verify_only:
        token = asyncio.run(public_download_token())
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(import_archive, record, token) for record in records]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        for record in documents:
            import_document(record)
    for record in records + documents:
        if not valid(DATA / record["relative_path"], record):
            raise ValueError("Missing or invalid file: " + record["relative_path"])
    print("SUCCESS: 20 data archives and 2 PDFs match the recorded SHA-256 checksums.", flush=True)


if __name__ == "__main__":
    main()
