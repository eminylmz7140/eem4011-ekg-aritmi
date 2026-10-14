import argparse
import io
import os
import re
import zipfile
from urllib.request import Request, urlopen

from common import DATA, save_json

ARCHIVE_URL = "https://physionet.org/static/published-projects/mitdb/mit-bih-arrhythmia-database-1.0.0.zip"
ARCHIVE_ROOT = "mit-bih-arrhythmia-database-1.0.0/"
ARCHIVE_NAME = "mitdb-1.0.0.zip"


def download_archive():
    """Download the full database ZIP, resuming a partial transfer on rerun."""
    partial = DATA / (ARCHIVE_NAME + ".part")
    archive_path = DATA / ARCHIVE_NAME
    if archive_path.is_file() and zipfile.is_zipfile(archive_path):
        return archive_path

    offset = partial.stat().st_size if partial.exists() else 0
    headers = {"Range": f"bytes={offset}-"} if offset else {}
    request = Request(ARCHIVE_URL, headers=headers)
    with urlopen(request, timeout=120) as response:
        status = getattr(response, "status", 200)
        content_range = response.headers.get("Content-Range", "")
        if offset and status == 206:
            match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", content_range)
            if not match or int(match.group(1)) != offset:
                raise RuntimeError(f"Geçersiz indirme devam yanıtı: {content_range or status}")
            total_size = int(match.group(3))
            mode = "ab"
        else:
            offset = 0
            total_size = int(response.headers.get("Content-Length", "0")) or None
            mode = "wb"

        received = offset
        with partial.open(mode) as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
                received += len(chunk)
                if received and received % (10 * 1024 * 1024) < len(chunk):
                    if total_size:
                        print(f"Arşiv indiriliyor: {received / total_size:.0%}")
                    else:
                        print(f"İndirilen: {received:,} bayt")

    if total_size is not None and partial.stat().st_size != total_size:
        raise RuntimeError(
            f"İndirme tamamlanmadı ({partial.stat().st_size}/{total_size} bayt). "
            "Aynı komutu yeniden çalıştırarak kaldığı yerden sürdürün."
        )
    if not zipfile.is_zipfile(partial):
        raise RuntimeError("İndirilen dosya geçerli ZIP arşivi değil; kısmi dosya korunuyor.")
    os.replace(partial, archive_path)
    return archive_path


def extract_archive(archive_path, records=None):
    """Validate and extract requested WFDB records from a PhysioNet ZIP."""
    with zipfile.ZipFile(archive_path) as archive:
        bad_file = archive.testzip()
        if bad_file:
            raise RuntimeError(f"Arşiv CRC kontrolü başarısız: {bad_file}")

        available = [
            line.strip()
            for line in archive.read(ARCHIVE_ROOT + "RECORDS").decode("ascii").splitlines()
            if line.strip()
        ]
        if records is None:
            if len(available) != 48:
                raise RuntimeError(f"Beklenen 48 kayıt yerine {len(available)} kayıt bulundu.")
            records = available

        missing = []
        for record in records:
            for extension in ("hea", "dat", "atr"):
                member = f"{ARCHIVE_ROOT}{record}.{extension}"
                try:
                    content = archive.read(member)
                except KeyError:
                    missing.append(member)
                    continue
                target = DATA / f"{record}.{extension}"
                if not target.is_file() or target.stat().st_size == 0:
                    target.write_bytes(content)
        if missing:
            raise RuntimeError("Arşivde gerekli kayıt dosyaları eksik: " + ", ".join(missing))
    return [str(record) for record in records]


def download_selected_records(records):
    """Download a small requested subset without fetching the full ZIP."""
    downloaded = []
    for record in records:
        try:
            for extension in ("hea", "dat", "atr"):
                target = DATA / f"{record}.{extension}"
                if target.is_file() and target.stat().st_size > 0:
                    continue
                url = f"https://physionet.org/files/mitdb/1.0.0/{record}.{extension}"
                with urlopen(url, timeout=30) as response:
                    content = response.read()
                target.write_bytes(content)
            downloaded.append(str(record))
            print("Hazır", record)
        except Exception as error:
            print(f"Atlandı {record}: {type(error).__name__}: {error}")

    failed = sorted(set(map(str, records)) - set(downloaded))
    if failed:
        raise RuntimeError(f"{len(failed)} kayıt tamamlanamadı: {', '.join(failed)}")
    return downloaded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", nargs="+", default=None)
    parser.add_argument("--local-only", action="store_true")
    args = parser.parse_args()
    if args.local_only and args.records:
        parser.error("--local-only ile --records birlikte kullanılamaz")

    if args.local_only:
        records = sorted(
            path.stem
            for path in DATA.glob("*.hea")
            if (DATA / f"{path.stem}.dat").is_file()
            and (DATA / f"{path.stem}.atr").is_file()
        )
        if not records:
            raise RuntimeError("data/ içinde .hea, .dat ve .atr dosyaları olan kayıt bulunamadı.")
        print("Yerel kayıtlar:", len(records))
    elif args.records:
        records = download_selected_records(args.records)
    else:
        archive_path = download_archive()
        records = extract_archive(archive_path)
        print("Tam MIT-BIH arşivi açıldı:", len(records), "kayıt")

    records = list(map(str, records))
    save_json(
        "download_manifest.json",
        {"records_requested": records, "records_downloaded": records},
    )


if __name__ == "__main__":
    main()
