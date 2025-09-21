import sys
import importlib.metadata as md
from pathlib import Path
import click
from tqdm import tqdm
from collections import Counter


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
    return output.open("w", encoding="utf-8", newline="\n") if output else None


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
@click.option(
    "-i", "--input", "i", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option("-o", "--output", "o", type=click.Path(dir_okay=False, path_type=Path))
@click.option("-t", "--text", type=str, help="Inline text instead of --input")
@click.option("--encoding", type=str, help="Force input encoding")
@click.option("--progress", default=True, is_flag=True, help="Show progress bar")
def normalize(
    i: Path | None,
    o: Path | None,
    text: str | None,
    encoding: str | None,
    progress: bool,
):
    """Normalize text (line-by-line for files)."""
    try:
        from shekar import Normalizer

        norm = Normalizer()
    except Exception as e:
        click.echo(f"Cannot import Normalizer: {e}", err=True)
        sys.exit(2)

    fout = _open_out(o)
    try:
        lines = list(_iter_lines(i, text, encoding))
        bar = tqdm(
            total=len(lines),
            unit="line",
            disable=((not progress) or (text is not None)),
        )
        for s in lines:
            try:
                out = norm(s)
            except TypeError:
                out = norm.normalize(s)
            if fout:
                fout.write(out + "\n")
            else:
                click.echo(out)
            bar.update(1)
        bar.close()
    finally:
        if fout:
            fout.close()


# ---------- wordcloud ----------
@cli.command()
@click.option(
    "-i",
    "--input",
    "i",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Input text file",
)
@click.option("-t", "--text", type=str, help="Inline text instead of --input")
@click.option(
    "-o",
    "--output",
    "o",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    required=True,
    help="Output PNG file",
)
@click.option("--bidi", is_flag=True, default=False, help="Apply bidi reshaping")
@click.option(
    "--mask",
    type=str,
    default="Iran",
    help="Shape mask (Iran, Heart, Bulb, Cat, Cloud, Head) or custom image path",
)
@click.option(
    "--font",
    type=str,
    default="sahel",
    help="Font to use (sahel, parastoo) or custom TTF font path",
)
@click.option(
    "--width",
    type=int,
    default=1000,
    help="Image width in pixels (ignored if mask provided)",
)
@click.option(
    "--height",
    type=int,
    default=500,
    help="Image height in pixels (ignored if mask provided)",
)
@click.option("--bg-color", type=str, default="white", help="Background color")
@click.option(
    "--contour-color", type=str, default="black", help="Outline color of the mask shape"
)
@click.option("--contour-width", type=int, default=3, help="Thickness of the outline")
@click.option(
    "--color-map", type=str, default="Set2", help="Matplotlib color map for words"
)
@click.option("--min-font-size", type=int, default=5, help="Minimum font size")
@click.option("--max-font-size", type=int, default=220, help="Maximum font size")
def wordcloud(
    i: Path | None,
    text: str | None,
    o: Path,
    bidi: bool,
    mask: str,
    font: str,
    width: int,
    height: int,
    bg_color: str,
    contour_color: str,
    contour_width: int,
    color_map: str,
    min_font_size: int,
    max_font_size: int,
):
    """
    Generate a wordcloud image from input text or file and save as PNG.
    """
    if not text and not i:
        click.echo("Error: provide either --text or --input", err=True)
        sys.exit(2)

    try:
        from shekar import WordCloud, WordTokenizer, Normalizer
        from shekar.preprocessing import (
            RemoveHTMLTags,
            RemoveDiacritics,
            RemovePunctuations,
            RemoveStopWords,
            RemoveNonPersianLetters,
        )

        cleaners = (
            RemoveHTMLTags()
            | RemovePunctuations()
            | RemoveDiacritics()
            | RemoveStopWords()
            | RemoveNonPersianLetters()
        )

        preprocessing_pipeline = cleaners | Normalizer()

    except Exception as e:
        click.echo(f"Could not import shekar modules: {e}", err=True)
        sys.exit(2)

    # Load input
    if text:
        raw_text = text
    else:
        raw_text = i.read_text(encoding="utf-8", errors="replace")

    clean_text = preprocessing_pipeline(raw_text)

    # Tokenize
    tokens = WordTokenizer()(clean_text)
    word_freqs = Counter(tokens)

    # Generate wordcloud
    wc = WordCloud(
        mask=mask,
        font=font,
        width=width,
        height=height,
        max_font_size=max_font_size,
        min_font_size=min_font_size,
        bg_color=bg_color,
        contour_color=contour_color,
        contour_width=contour_width,
        color_map=color_map,
    )

    image = wc.generate(word_freqs, bidi_reshape=bidi)
    image.save(o)
    click.echo(f"Wordcloud saved to {o}")


def main():
    cli()
