"""Import and verify the original HEMS input files in raw_manifest.json."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

DATA = Path(__file__).resolve().parents[1] / "HEMS_inputs"
CHUNK_BYTES = 64 * 1024 * 1024


def digest(path, algorithm):
    with path.open("rb") as source:
        return hashlib.file_digest(source, algorithm).hexdigest()


def import_file(record):
    path = DATA / "raw" / record["filename"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not record.get("split") and is_valid(path, record):
        print(f"Verified existing {path.name}", flush=True)
        return
    with tempfile.TemporaryDirectory(dir=path.parent) as staging:
        downloaded = Path(staging) / path.name
        subprocess.run([
            "curl", "--fail", "--silent", "--show-error", "--location",
            "--retry", "4", "--retry-all-errors", "--connect-timeout", "20",
            "--max-time", "420", "--output", str(downloaded), record["url"],
        ], check=True)
        if not is_valid(downloaded, record):
            raise ValueError(f"Publisher file checksum or size changed: {path.name}")
        if record.get("split"):
            split_file(downloaded, path, record)
        else:
            downloaded.replace(path)
    print(f"Verified {path.name} ({record['bytes']} bytes)", flush=True)


def is_valid(path, record):
    return (
        path.is_file()
        and path.stat().st_size == record["bytes"]
        and digest(path, record["algorithm"]) == record["digest"]
    )


def split_file(downloaded, destination, record):
    checksum = hashlib.new(record["algorithm"])
    with downloaded.open("rb") as source:
        index = 0
        while block := source.read(CHUNK_BYTES):
            index += 1
            part = destination.with_name(f"{destination.name}.part-{index:02d}")
            part.write_bytes(block)
            checksum.update(part.read_bytes())
    if sum(part.stat().st_size for part in destination.parent.glob(destination.name + ".part-*")) != record["bytes"]:
        raise ValueError(f"Incorrect total of split byte lengths for {destination.name}")
    if checksum.hexdigest() != record["digest"]:
        raise ValueError(f"Split checksum mismatch for {destination.name}")


def main():
    records = json.loads((DATA / "raw_manifest.json").read_text())
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(import_file, records))


if __name__ == "__main__":
    main()
