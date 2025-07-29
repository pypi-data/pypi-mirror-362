import json
import os
import shutil
from pathlib import Path
from sys import stdout
from typing import Any, NamedTuple

from tqdm import tqdm

from edmgr.config import settings


class Download:
    def __init__(self, content: Any = None, error: dict = None):
        self._content = content
        if error is None:
            error = {}
        self.error = error

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def iter_content(self, chunk_size: int):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    @property
    def content_length(self):
        raise NotImplementedError()


class HTTPDownload(Download):
    def __enter__(self):
        if self._content:
            self._content.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._content:
            self._content.__exit__(exc_type, exc_value, traceback)

    def iter_content(self, chunk_size: int = None):
        if self._content:
            if chunk_size is None:
                chunk_size = 1024
            return self._content.iter_content(chunk_size=chunk_size)
        else:
            return ()

    def close(self):
        if self._content:
            self._content.close()

    @property
    def content_length(self) -> int:
        if self._content:
            return int(self._content.headers.get("content-length", 0))
        return 0


class FASPSpec(NamedTuple):
    spec: dict = {}
    error: dict = {}


class ProgressBar(tqdm):
    def __init__(self, total: int, unit_divisor: int = 1000, disable: bool = None):
        l_bar = "{desc}: {percentage:3.0f}%["
        r_bar = (
            "] {n_fmt}/{total_fmt} {unit} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        )
        bar_format = f"{l_bar}{{bar}}{r_bar}"

        if disable is None:
            disable_bar = settings.get("no_progress_bar", False)
        else:
            disable_bar = disable

        super().__init__(
            unit="B",
            unit_scale=True,
            unit_divisor=unit_divisor,
            total=total,
            file=stdout,
            bar_format=bar_format,
            ascii=" -=",
            disable=disable_bar,
        )


def write_download(file_path: Path, download: Download) -> int:
    written_bytes = 0
    with download as stream:
        total_bytes = stream.content_length
        with open(file_path, mode="wb") as file, ProgressBar(total_bytes) as bar:
            for chunk in stream.iter_content():
                data_size = file.write(chunk)
                bar.update(data_size)
                written_bytes += data_size
    return written_bytes


def _fasp_download(file_path: Path, fasp_spec: FASPSpec) -> None:
    if not shutil.which("ascli"):
        raise RuntimeError(
            "aspera-cli executable not found."
            " Please follow https://github.com/IBM/aspera-cli#installation"
        )
    fasp_spec.spec["paths"][0]["destination"] = str(file_path)
    cmd = [
        "ascli",
        "server",
        "download",
        f"--url={settings['aspera_url']}",
        f"--ts=@json:'{json.dumps(fasp_spec.spec)}'",
        "--sources=@ts",
    ]
    os.system(" ".join(cmd))
