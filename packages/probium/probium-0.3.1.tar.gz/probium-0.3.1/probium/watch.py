"""File system watchers that run detection on new files."""

from __future__ import annotations
from pathlib import Path
from typing import Callable, Iterable, Any
import logging
import threading
import time
import os
import concurrent.futures as cf

try:  # use real watchdog if available
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent

    USING_STUB = False
except ImportError:  # pragma: no cover - fallback when watchdog missing
    from watchdog_stub.observers import Observer  # type: ignore
    from watchdog_stub.events import FileSystemEventHandler, FileSystemEvent  # type: ignore

    USING_STUB = True
    logging.getLogger(__name__).warning(
        "watchdog package not installed; using stub implementation"
    )

from .core import _detect_file as detect
from .models import Result
from .google_magika import require_magika

logger = logging.getLogger(__name__)


class _FilterHandler(FileSystemEventHandler):
    def __init__(
        self,
        callback: Callable[[Path, Result], Any],
        *,
        recursive: bool = True,
        only: Iterable[str] | None = None,
        extensions: Iterable[str] | None = None,
        magika: bool = False,
        cache: bool = True,
    ) -> None:
        self.callback = callback
        self.recursive = recursive
        self.only = set(only) if only else None
        self.extensions = (
            {e.lower().lstrip(".") for e in extensions} if extensions else None
        )
        self._seen: set[Path] = set()
        self.magika = magika
        self.cache = cache

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle created paths."""
        self._handle_path(event.src_path)

    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle paths moved into the watched directory."""
        self._handle_path(event.dest_path)

    def _handle_path(self, raw: str | Path) -> None:
        path = Path(raw)
        if path in self._seen:
            return
        self._seen.add(path)

        if path.is_dir():
            if not self.recursive:
                return
            for p in path.rglob("*"):
                if p.is_file():
                    self._handle_path(p)
            return
        if self.extensions and path.suffix.lower().lstrip(".") not in self.extensions:
            return
        if self.magika:
            res = detect(path, engine="magika", cap_bytes=None, cache=self.cache)
        else:
            res = detect(
                path,
                only=self.only,
                extensions=self.extensions,
                cap_bytes=None,
                cache=self.cache,
            )
        try:
            self.callback(path, res)
        except Exception:
            logger.exception("watcher callback failed for %s", path)


class WatchContainer:
    """Simple wrapper around :mod:`watchdog` observers."""

    def __init__(
        self,
        root: str | Path,
        callback: Callable[[Path, Result], Any],
        *,
        recursive: bool = True,
        only: Iterable[str] | None = None,
        extensions: Iterable[str] | None = None,
        magika: bool = False,
        cache: bool = True,
    ) -> None:
        self.root = Path(root)
        self.callback = callback
        self.recursive = recursive
        self.handler = _FilterHandler(
            callback,
            recursive=recursive,
            only=only,
            extensions=extensions,
            magika=magika,
            cache=cache,
        )
        self.observer = Observer()

    def start(self) -> None:
        """Begin monitoring ``root`` for filesystem events."""

        if USING_STUB:
            logger.warning("watchdog not available; file events will not be reported")

        self.observer.schedule(self.handler, str(self.root), recursive=self.recursive)
        self.observer.start()

    def stop(self) -> None:
        """Stop the observer and wait for the thread to exit."""

        self.observer.stop()
        self.observer.join()


class PollingWatchContainer:
    """Portable polling-based directory watcher."""

    def __init__(
        self,
        root: str | Path,
        callback: Callable[[Path, Result], Any],
        *,
        recursive: bool = True,
        only: Iterable[str] | None = None,
        extensions: Iterable[str] | None = None,
        interval: float = 1.0,
        magika: bool = False,
        cache: bool = True,
        workers: int | None = None,
    ) -> None:
        """Create a polling-based watcher.

        Parameters
        ----------
        workers:
            Number of threads used to scan files concurrently. Defaults to the
            CPU count when ``None``.
        """
        self.root = Path(root)
        self.callback = callback
        self.recursive = recursive
        self.interval = interval
        self.handler = _FilterHandler(
            callback,
            recursive=recursive,
            only=only,
            extensions=extensions,
            magika=magika,
            cache=cache,
        )
        self._executor = cf.ThreadPoolExecutor(max_workers=workers or os.cpu_count() or 4)
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _scan(self) -> None:
        paths = [
            p
            for p in (
                self.root.rglob("*") if self.recursive else self.root.iterdir()
            )
            if p.is_file()
        ]
        if not paths:
            return
        list(self._executor.map(self.handler._handle_path, paths))

    def _run(self) -> None:
        while not self._stop.is_set():
            self._scan()
            time.sleep(self.interval)

    def start(self) -> None:
        # seed seen set so existing files are ignored
        for p in self.root.rglob("*") if self.recursive else self.root.iterdir():
            if p.is_file():
                self.handler._seen.add(p)
        self._scan()
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join()
        self._executor.shutdown(wait=True)


def watch(
    root: str | Path,
    callback: Callable[[Path, Result], Any],
    *,
    recursive: bool = True,
    only: Iterable[str] | None = None,
    extensions: Iterable[str] | None = None,
    interval: float = 1.0,
    magika: bool = False,
    cache: bool = True,
    workers: int | None = None,
) -> WatchContainer:
    """Start watching ``root`` and invoke ``callback`` for new files.

    If the optional :mod:`watchdog` package is available, native file system
    events are used. Otherwise a portable polling loop is started. The polling
    interval can be customized with ``interval``. When polling is used,
    ``workers`` controls the size of the thread pool used to scan files.
    """
    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(f"watch root does not exist: {root}")

    if magika:
        require_magika()

    if USING_STUB:
        container: WatchContainer | PollingWatchContainer = PollingWatchContainer(
            root,
            callback,
            recursive=recursive,
            only=only,
            extensions=extensions,
            interval=interval,
            magika=magika,
            cache=cache,
            workers=workers,
        )
    else:
        container = WatchContainer(
            root,
            callback,
            recursive=recursive,
            only=only,
            extensions=extensions,
            magika=magika,
            cache=cache,
        )
    container.start()
    return container
