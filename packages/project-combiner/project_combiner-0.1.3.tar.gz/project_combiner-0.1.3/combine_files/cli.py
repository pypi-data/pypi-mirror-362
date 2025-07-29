#!/usr/bin/env python3
"""
combine_files  ─ concatenate text‑like files in a directory tree.

Highlights
──────────
• Typer‑based CLI with rich `--help` and shell completion.  
• Cross‑platform paths via `pathlib.Path`.  
• Skip / preview lists, encodings, logging level, and output location are all
  flag‑driven—no hard‑coding.  
• Respects project‐specific *.gitignore* rules if *pathspec* is installed.  
• Skips obvious binary files via `mimetypes`.  
• Optional progress bar (tqdm) and multithreaded reads for big trees.  
• Stream output to *stdout* or any file; “-” is shorthand for *stdout*.  
• Clean exit codes and keyboard‑interrupt handling.

Install optional extras for the niceties:

    pip install typer[all] pathspec tqdm

Usage examples
──────────────
    # Dump everything but big binaries to stdout, respecting .gitignore
    combine-files .

    # Combine only backend sources with previews for CSV/JSON
    combine-files . backend -o backend.txt --preview-ext .csv .json

    # Skip virtualenvs, show a progress bar, read files in 8 threads
    combine-files . --skip-dirs venv .venv --jobs 8 --progress

"""



from __future__ import annotations

import itertools
import logging
import mimetypes
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, List, Sequence, Set

import typer

# ─── Optional deps ──────────────────────────────────────────────────────────
try:
    import pathspec  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    pathspec = None  # noqa: N816

try:
    from tqdm import tqdm  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    tqdm = None  # noqa: N816

try:
    import pyperclip      # pip install pyperclip
except ModuleNotFoundError:
    pyperclip = None
# ────────────────────────────────────────────────────────────────────────────

app = typer.Typer(add_completion=False, help="See `--help` for options.")


# ── Helpers ────────────────────────────────────────────────────────────────
def _to_set(values: Sequence[str] | None) -> Set[str]:
    """Convert a list/tuple or space‑separated string into a set, ignoring empties."""
    if not values:
        return set()
    if len(values) == 1 and isinstance(values[0], str) and " " in values[0]:
        # Allow:  --skip-dirs "venv .venv .git"
        vals: Iterable[str] = values[0].split()
    else:
        vals = values
    return {v for v in vals if v}


def _build_gitignore_spec(repo_root: Path):
    if not pathspec:
        return None
    gitignore = repo_root / ".gitignore"
    if gitignore.exists():
        return pathspec.PathSpec.from_lines("gitwildmatch", gitignore.read_text().splitlines())
    return None


def _iter_paths(
    roots: Sequence[Path],
    skip_dirs: Set[str],
    skip_files: Set[str],
    skip_exts: Set[str],
    gitignore_spec=None,
    follow_symlinks: bool = False,
    skip_dot_dirs: bool = True,
) -> Iterable[Path]:
    """Yield candidate file paths under *roots* applying all skip rules."""
    stack = list(roots)
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    name = entry.name
                    path = Path(entry.path)

                    if entry.is_dir(follow_symlinks=follow_symlinks):
                        if (
                            name in skip_dirs
                            or (skip_dot_dirs and name.startswith("."))
                            or (gitignore_spec and gitignore_spec.match_file(path.relative_to(roots[0])))
                        ):
                            continue
                        stack.append(path)
                        continue

                    # files
                    if (
                        name in skip_files
                        or path.suffix in skip_exts
                        or (gitignore_spec and gitignore_spec.match_file(path.relative_to(roots[0])))
                    ):
                        continue
                    yield path
        except PermissionError:  # pragma: no cover
            logging.warning("Permission denied: %s", current)


def _read_preview(path: Path, lines: int, encoding: str, errors: str) -> str:
    with path.open("r", encoding=encoding, errors=errors) as fh:
        head = "".join(itertools.islice(fh, lines))
    return head + "\n… (truncated)\n"


def _is_binary(path: Path) -> bool:
    """Crude binary test using mimetypes (safe for Windows/MSYS paths)."""
    mime, _ = mimetypes.guess_type(path.as_posix(), strict=False)
    return mime is not None and not mime.startswith("text")


def _read_file(
    path: Path,
    preview_exts: Set[str],
    preview_lines: int,
    encoding: str,
    errors: str,
) -> str:
    if path.suffix in preview_exts:
        return _read_preview(path, preview_lines, encoding, errors)
    return path.read_text(encoding=encoding, errors=errors)


# ── CLI entrypoint ─────────────────────────────────────────────────────────
@app.command()
def main(
    src_dir: Path = typer.Argument(..., exists=True, file_okay=False, resolve_path=True),
    section: str = typer.Option(
        "all",
        "--section",
        "-s",
        help="Glob, path, or legacy shortcut ('backend' / 'frontend' / 'all').",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="File to write (default: stdout). Use '-' for stdout.",
    ),
    skip_dirs: List[str] = typer.Option(
        ["venv", ".venv", "node_modules", ".git", "alembic", "__pycache__"],
        help="Directory names to skip.",
    ),
    skip_files: List[str] = typer.Option(
        ["package-lock.json", ".gitignore", ".DS_Store", ".env", '.whl'],
        help="Exact filenames to skip.",
    ),
    skip_exts: List[str] = typer.Option(
        [".db"],
        help="File extensions to skip (dot‑prefixed).",
    ),
    preview_exts: List[str] = typer.Option(
        [".csv", ".json"],
        help="Extensions to preview only first *N* lines.",
    ),
    preview_lines: int = typer.Option(10, help="Lines to keep for preview files."),
    encoding: str = typer.Option("utf-8", help="Default encoding for reading files."),
    errors: str = typer.Option(
        "ignore", help="Error handling strategy: 'strict', 'ignore', or 'replace'."
    ),
    jobs: int = typer.Option(
        1,
        "--jobs",
        "-j",
        help="Thread pool size for concurrent reads (>=2 turns it on).",
    ),
    follow_symlinks: bool = typer.Option(False, help="Follow symlinks when walking."),
    progress: bool = typer.Option(
        False, help="Show a progress bar (requires tqdm). Ignored for stdout."
    ),
    # verbose: bool = typer.Option(False, "--verbose", "-v", help="Increase log verbosity."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Increase log verbosity."),
    clipboard: bool = typer.Option(
        False,
        "--clipboard",
        "-c",
        help="Copy combined output to the system clipboard.",
    ),
    skip_dot_dirs: bool = typer.Option(
        True,
        "--skip-dot-dirs/--include-dot-dirs",
        help="Skip directories whose names start with '.' (dot).",
    ),
):
    """
    Concatenate text files under *SRC_DIR* into one stream.

    SECTION can be:
        • 'all'         – the entire tree (default)  
        • 'backend'     – src_dir / 'backend'  
        • 'frontend'    – src_dir / 'frontend'  
        • any glob/path – e.g. '**/services/*' or 'src/utils'
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)

    # Resolve roots list
    if section == "all":
        roots = [src_dir]
    elif section in ("backend", "frontend"):
        roots = [src_dir / section]
    else:
        roots = [p for p in src_dir.glob(section) if p.is_dir()]
        if not roots:
            typer.secho(f"No matching directories for section={section!r}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    # Normalise option lists
    skip_dirs_set: Set[str] = _to_set(skip_dirs)
    skip_files_set: Set[str] = _to_set(skip_files)
    skip_exts_set: Set[str] = _to_set(skip_exts)
    preview_exts_set: Set[str] = _to_set(preview_exts)

    gitignore_spec = _build_gitignore_spec(src_dir)
    if gitignore_spec:
        logging.debug("Loaded .gitignore rules (%d patterns).", len(gitignore_spec.patterns))

    # Collect paths first so we can show progress/deterministic ordering
    paths = sorted(
        _iter_paths(
            roots,
            skip_dirs_set,
            skip_files_set,
            skip_exts_set,
            gitignore_spec,
            follow_symlinks,
            skip_dot_dirs
        )
    )
    if not paths:
        typer.secho("Nothing to do: no files matched.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    # Pick output handle
    # out_fh = sys.stdout if output in (None, Path("-")) else output.expanduser().open("w", encoding="utf-8")
    buf: list[str] = []            # collect here if --clipboard
    out_fh = (
        sys.stdout
        if (output in (None, Path("-")) and not clipboard)
        else (sys.stdout if clipboard and output in (None, Path("-")) else output.expanduser().open("w", encoding="utf-8"))
    )

    def producer(p: Path) -> str:
        if _is_binary(p):
            return ""  # skip; unlikely thanks to mimetypes, but double‑check
        try:
            content = _read_file(p, preview_exts_set, preview_lines, encoding, errors)
        except (UnicodeDecodeError, OSError) as exc:
            logging.warning("Cannot read %s: %s", p, exc)
            return ""
        header = f"{'='*80}\nFILE: {p.relative_to(src_dir)}\n{'-'*80}\n"
        return header + content + "\n\n"

    try:
        if jobs > 1:
            with ThreadPoolExecutor(max_workers=jobs) as pool:
                fut_to_path = {pool.submit(producer, p): p for p in paths}
                iterable = (
                    tqdm(as_completed(fut_to_path), total=len(paths))
                    if progress and tqdm
                    else as_completed(fut_to_path)
                )
        #         for future in iterable:
        #             out_fh.write(future.result())
        # else:
        #     iterable = tqdm(paths) if progress and tqdm else paths
        #     for p in iterable:
        #         out_fh.write(producer(p))
                for future in iterable:
                    chunk = future.result()
                    (buf.append if clipboard else out_fh.write)(chunk)
        else:
            iterable = tqdm(paths) if progress and tqdm else paths
            for p in iterable:
                chunk = producer(p)
                (buf.append if clipboard else out_fh.write)(chunk)

    except KeyboardInterrupt:  # pragma: no cover
        typer.secho("\nInterrupted by user", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=130)
    finally:
        if out_fh is not sys.stdout:
            out_fh.close()
            logging.info("Wrote %s", output or "<stdout>")
    if clipboard:
        if not pyperclip:
            typer.secho("Install pyperclip for --clipboard (`pip install pyperclip`).", fg=typer.colors.RED)
            raise typer.Exit(1)
        content = "".join(buf)
        pyperclip.copy(content)
        typer.secho(f"✔ Copied {len(content):,} characters to clipboard.", fg=typer.colors.GREEN)

    return 0


def _entrypoint() -> None:  # <─ NEW thin wrapper
    try:
        app()
    except BrokenPipeError:  # pragma: no cover
        pass
