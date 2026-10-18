"""File-based state: gzip CSV bars, JSON, JSONL. Writes are atomic; bar history is never allowed to shrink."""
from __future__ import annotations

import gzip
import io
import json
import os
import shutil
from pathlib import Path

import pandas as pd

from .config import state_dir

COLS = ["open", "high", "low", "close", "volume"]


def bars_path(symbol: str, base: Path | None = None) -> Path:
    p = (base or state_dir()) / "bars"
    p.mkdir(parents=True, exist_ok=True)
    return p / f"{symbol}_5m.csv.gz"


def _atomic_write_bytes(path: Path, data: bytes):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def load_raw(symbol: str, base: Path | None = None) -> pd.DataFrame:
    p = bars_path(symbol, base)
    if not p.exists():
        return pd.DataFrame(columns=COLS, index=pd.DatetimeIndex([], tz="UTC"))
    df = pd.read_csv(p, index_col=0)
    df.index = pd.DatetimeIndex(pd.to_datetime(df.index, utc=True))
    return df.sort_index()


def save_bars(symbol: str, new: pd.DataFrame, base: Path | None = None) -> dict:
    """Merge `new` into stored history. Newer rows win on duplicate timestamps. Returns counts."""
    old = load_raw(symbol, base)
    before = len(old)
    if len(new):
        merged = pd.concat([old, new[COLS]])
        merged = merged[~merged.index.duplicated(keep="last")].sort_index()
    else:
        merged = old
    p = bars_path(symbol, base)
    if p.exists() and len(merged) < before:
        raise RuntimeError("refusing to overwrite history with fewer rows")
    if p.exists():
        shutil.copy2(p, p.with_suffix(".bak"))
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(merged.to_csv().encode())
    _atomic_write_bytes(p, buf.getvalue())
    return {"before": before, "after": len(merged), "added": len(merged) - before}


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_bytes(path, json.dumps(obj, indent=2, default=str).encode())


def read_json(path: Path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def append_jsonl(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(obj, default=str) + "\n")


def read_jsonl(path: Path, last_n: int | None = None) -> list[dict]:
    if not Path(path).exists():
        return []
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # tolerate a torn last line after a crash
    return rows[-last_n:] if last_n else rows
