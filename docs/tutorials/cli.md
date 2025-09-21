# Command-Line Interface (CLI)

Shekar includes a command-line interface (CLI) for quick text processing and visualization.  
You can normalize Persian text or generate wordclouds directly from files or inline strings.

**Usage**

```console
shekar [COMMAND] [OPTIONS]
```

### Commands

1. `normalize`

Normalize Persian text by standardizing spacing, characters, and diacritics.  
Works with files or inline text.

**Options**

- `-i, --input` Path to an input text file  
- `-o, --output` Path to save normalized text. If not provided, results are printed to stdout  
- `-t, --text` Inline text instead of a file  
- `--encoding` Force a specific input file encoding  
- `--progress` Show progress bar (enabled by default)  

**Examples**

<!-- termynal -->
```console
# Normalize a text file and save output
shekar normalize -i ./corpus.txt -o ./normalized_corpus.txt
```

</br>

<!-- termynal -->
```console
# Normalize inline text
shekar normalize --text "درود پرودگار بر ایران و ایرانی"
```

1. `wordcloud`

Generate a wordcloud image (PNG) from Persian text, either from a file or inline.  
Preprocessing automatically removes punctuation, diacritics, stopwords, non-Persian characters, and normalizes spacing.

---

**Options**

- `-i, --input` Input text file  
- `-t, --text` Inline text instead of a file  
- `-o, --output` **(required)** Path to output PNG file
- `--bidi` Apply **bidi reshaping** for correct rendering of Persian text (default: `False`) 
- `--mask` Shape mask (`Iran`, `Heart`, `Bulb`, `Cat`, `Cloud`, `Head`) or custom image path  
- `--font` Font to use (`sahel`, `parastoo`, or custom TTF path)  
- `--width` Image width in pixels (default: 1000)  
- `--height` Image height in pixels (default: 500)  
- `--bg-color` Background color (default: white)  
- `--contour-color` Outline color (default: black)  
- `--contour-width` Outline thickness (default: 3)  
- `--color-map` Matplotlib colormap for words (default: Set2)  
- `--min-font-size` Minimum font size (default: 5)  
- `--max-font-size` Maximum font size (default: 220)  

---

**Examples**

<!-- termynal -->
```console
# Generate a wordcloud from a text file
shekar wordcloud -i ./corpus.txt -o ./word_cloud.png
```

</br>

<!-- termynal -->
```console
# Generate a wordcloud from inline text with a custom mask

shekar wordcloud --text "درود پرودگار بر ایران و ایرانی" 
\ -o ./word_cloud.png --mask Heart
```

**Note:** If the letters in the generated wordcloud appear **separated**, use the `--bidi` option to enable proper Persian text shaping.
