import sys
import importlib.metadata as md
from pathlib import Path
import click
from tqdm import tqdm


# ---------- helpers ----------
def _detect_encoding(path: Path) -> str:
    try:
        import chardet
        with path.open("rb") as f:
            raw = f.read(50000)
        return chardet.detect(raw).get("encoding") or "utf-8"
    except Exception:
        return "utf-8"

def _iter_lines(input_path: Path | None, text: str | None, encoding: str | None):
    if text is not None:
        yield text
        return
    if not input_path:
        click.echo("Provide --text or --input", err=True)
        sys.exit(2)
    enc = encoding or _detect_encoding(input_path)
    with input_path.open("r", encoding=enc, errors="replace") as f:
        for line in f:
            yield line.rstrip("\r\n")

def _open_out(output: Path | None):
    return (output.open("w", encoding="utf-8", newline="\n") if output else None)


# ---------- root ----------
@click.group(help="Shekar CLI for Persian NLP")
def cli():
    pass

@cli.command()
def version():
    """Show installed Shekar version."""
    click.echo(md.version("shekar"))

@cli.command()
def info():
    """Show brief feature list and docs link."""
    click.echo("Shekar: Persian NLP toolkit. See docs: lib.shekar.io")


# ---------- normalize ----------
@cli.command()
@click.option("-i", "--input", "i", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("-o", "--output", "o", type=click.Path(dir_okay=False, path_type=Path))
@click.option("-t", "--text", type=str, help="Inline text instead of --input")
@click.option("--encoding", type=str, help="Force input encoding")
@click.option("--progress", default=True, is_flag=True, help="Show progress bar")
def normalize(i: Path | None, o: Path | None, text: str | None, encoding: str | None, progress: bool):
    """Normalize text (line-by-line for files)."""
    try:
        from shekar import Normalizer
        norm = Normalizer()
    except Exception as e:
        click.echo(f"Cannot import Normalizer: {e}", err=True); sys.exit(2)

    fout = _open_out(o)
    try:
        lines = list(_iter_lines(i, text, encoding))
        bar = tqdm(total=len(lines), unit="line", disable=((not progress) or (text is not None)))
        for s in lines:
            try:
                out = norm(s)
            except TypeError:
                out = norm.normalize(s)
            if fout: fout.write(out + "\n")
            else: click.echo(out)
            bar.update(1)
        bar.close()
    finally:
        if fout: fout.close()

def main():
    cli()
